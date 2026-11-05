"""Stable VAR(1) simulator with explicit observation errors and state impulses.

Assumptions: x[t] = A @ x[t-1] + w[t] + s[t]; y[t] = x[t] + v[t] + o[t].
Ordinary noises w ~ N(0,Q), v ~ N(0,R) are independent across time and streams.
Events are explicit interventions, not a fitted stochastic arrival model. A state
impulse enters once; subsequent propagation follows A. Observation errors last
one return observation. This is not a realistic erroneous-price model: differenced
price errors instead create opposite-signed adjacent return errors.

The process starts at zero before burn-in, so initialization is approximate rather
than an exact stationary draw. Configuration and ground truth must never be passed
as event information to an ordinary prediction method. Matrices are known only
under the pilot's stated parameter-information assumption. Seeding reproduces
draws in the same NumPy environment, not necessarily across library versions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]


def _readonly(value: object) -> Array:
    array = np.array(value, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(array)):
        raise ValueError("Arrays must contain finite values")
    array.setflags(write=False)
    return array


def _integer(value: int, name: str, minimum: int) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True)
class Config:
    """Validated dynamics, covariances, length, burn-in and scoring-window size."""

    transition: Array
    process_cov: Array
    observation_cov: Array
    n_steps: int = 200
    burn_in: int = 128
    score_window: int = 5

    def __post_init__(self) -> None:
        for name in ("transition", "process_cov", "observation_cov"):
            object.__setattr__(self, name, _readonly(getattr(self, name)))
        a = self.transition
        if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] == 0:
            raise ValueError("transition must be a nonempty square matrix")
        if np.max(np.abs(np.linalg.eigvals(a))) >= 1.0:
            raise ValueError("transition must have spectral radius < 1")
        for name in ("process_cov", "observation_cov"):
            cov = getattr(self, name)
            if cov.shape != a.shape or not np.allclose(cov, cov.T, rtol=0, atol=1e-12):
                raise ValueError(f"{name} must be symmetric and match transition shape")
            if np.linalg.eigvalsh(cov).min() < -1e-12:
                raise ValueError(f"{name} must be positive semidefinite")
        _integer(self.n_steps, "n_steps", 2)
        _integer(self.burn_in, "burn_in", 0)
        _integer(self.score_window, "score_window", 1)
        if self.n_steps <= self.score_window:
            raise ValueError("n_steps must exceed score_window")

    @property
    def n_assets(self) -> int:
        return self.transition.shape[0]


@dataclass(frozen=True)
class Event:
    """One vector impulse at an observed-array index; amplitude is private truth."""

    time: int
    kind: Literal["observation", "state"]
    amplitude: tuple[float, ...]

    def __post_init__(self) -> None:
        _integer(self.time, "event time", 0)
        if self.kind not in ("observation", "state"):
            raise ValueError("Unknown event kind")
        values = _readonly(self.amplitude)
        if values.ndim != 1 or values.size == 0:
            raise ValueError("amplitude must be a nonempty vector")
        object.__setattr__(self, "amplitude", tuple(float(v) for v in values))


@dataclass(frozen=True)
class Observations:
    """Public observations only; no event timing, labels, amplitudes or latent state."""

    values: Array


@dataclass(frozen=True)
class GroundTruth:
    """Scoring-only states and event metadata; keep outside the prediction layer."""

    latent: Array
    events: tuple[Event, ...]


@dataclass(frozen=True)
class Simulation:
    observed: Observations
    truth: GroundTruth


def _gaussian(rng: np.random.Generator, cov: Array, n: int) -> Array:
    """Sample positive-semidefinite covariances without requiring Cholesky rank."""
    values, vectors = np.linalg.eigh(cov)
    root = vectors * np.sqrt(np.maximum(values, 0.0))
    return rng.standard_normal((n, len(cov))) @ root.T


def simulate(config: Config, seed: int, events: Sequence[Event] = ()) -> Simulation:
    """Generate paired-noise-compatible paths with explicit private interventions.

    Independent process/measurement streams do not depend on event construction.
    Event scoring windows cannot overlap or include a later injected event.
    """
    _integer(seed, "seed", 0)
    ordered = tuple(sorted(events, key=lambda event: event.time))
    previous = -config.score_window - 1
    for event in ordered:
        if len(event.amplitude) != config.n_assets:
            raise ValueError("Event amplitude dimension must match asset count")
        if event.time + config.score_window >= config.n_steps:
            raise ValueError("Every event needs a complete future scoring window")
        if event.time - previous <= config.score_window:
            raise ValueError("Event spacing must exceed score_window")
        previous = event.time
    streams = np.random.SeedSequence(seed).spawn(2)
    total = config.burn_in + config.n_steps
    w = _gaussian(np.random.default_rng(streams[0]), config.process_cov, total)
    v = _gaussian(np.random.default_rng(streams[1]), config.observation_cov, total)
    event_map = {event.time + config.burn_in: event for event in ordered}
    latent = np.empty((total, config.n_assets), dtype=np.float64)
    observed = np.empty_like(latent)
    state = np.zeros(config.n_assets, dtype=np.float64)
    for time in range(total):
        state = config.transition @ state + w[time]
        event = event_map.get(time)
        if event is not None and event.kind == "state":
            state = state + np.asarray(event.amplitude)
        latent[time] = state
        observed[time] = state + v[time]
        if event is not None and event.kind == "observation":
            observed[time] += np.asarray(event.amplitude)
    return Simulation(
        Observations(_readonly(observed[config.burn_in:])),
        GroundTruth(_readonly(latent[config.burn_in:]), ordered),
    )


def paired_worlds(
    config: Config, seed: int, event_time: int, amplitude: Sequence[float]
) -> tuple[Simulation, Simulation]:
    """Return (observation-error world, state-shock world) with coupled noises.

    Observations match through event_time up to floating-point rounding. States
    differ by A**k @ amplitude at event_time+k. No predictor is given the pairing.
    """
    vector = tuple(amplitude)
    return (
        simulate(config, seed, (Event(event_time, "observation", vector),)),
        simulate(config, seed, (Event(event_time, "state", vector),)),
    )
