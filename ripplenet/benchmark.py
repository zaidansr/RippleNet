"""Synthetic benchmark components. Ordinary filters never receive event labels.

An oracle argument is explicitly privileged. Gaussian impulse covariances are
exact for the scheduled Gaussian-event generator, not arbitrary contamination.
"""

from __future__ import annotations

import numpy as np

from .simulation import Array, Config, Event, GroundTruth, Observations, Simulation, paired_worlds, simulate


def configuration(persistence: str) -> Config:
    a = np.array([[.55, .10, 0.], [0., .45, .10], [.05, 0., .35]])
    factors = {"moderate": 1., "weak": .2, "zero": 0.}
    if persistence not in factors:
        raise ValueError("Unknown persistence")
    return Config(a * factors[persistence], .01 * np.eye(3), .0025 * np.eye(3), n_steps=180)


def worlds(config: Config, seed: int, scale: float, price_error: bool = False) -> dict[str, Simulation]:
    """One independent run, with coupled clean/observation/state paths."""
    rng = np.random.default_rng(np.random.SeedSequence([seed, 918273]))
    time = int(rng.integers(40, 150))
    amplitude = rng.normal(0., scale, config.n_assets)
    obs, state = paired_worlds(config, seed, time, amplitude)
    if price_error:
        values = obs.observed.values.copy()
        values[time + 1] -= amplitude
        obs = Simulation(Observations(values), obs.truth)
    return {"clean": simulate(config, seed), "observation": obs, "state": state}


def initial_covariance(config: Config) -> Array:
    """Exact marginal covariance immediately before retained observation zero."""
    covariance = np.zeros_like(config.process_cov)
    for _ in range(config.burn_in):
        covariance = config.transition @ covariance @ config.transition.T + config.process_cov
    return covariance


def fit_linear(config: Config) -> Array:
    """OLS on clean training observations only; no clean latent targets used."""
    inputs, targets = [], []
    for seed in range(10000, 10020):
        y = simulate(config, seed).observed.values
        inputs.append(np.column_stack((np.ones(len(y)-1), y[:-1])))
        targets.append(y[1:])
    return np.linalg.lstsq(np.concatenate(inputs), np.concatenate(targets), rcond=None)[0]


def kalman(
    observations: Observations, config: Config, mode: str = "kalman", threshold: float = 3.,
    oracle: Event | None = None, event_scale: float = .5,
) -> Array:
    """Online KF, innovation-clipped heuristic, adaptive heuristic, or oracle.

    Row t predicts x[t+1]. Only mode='oracle' accepts privileged metadata.
    Clipping retains nominal covariance and is a heuristic, not a posterior.
    Adaptive mode splits estimated excess residual variance equally across
    process and observation covariance; it has no event identity input.
    """
    if mode not in ("kalman", "clipped", "adaptive", "oracle"):
        raise ValueError("Unknown filter mode")
    if oracle is not None and mode != "oracle":
        raise ValueError("Ordinary methods must not receive labels")
    if threshold <= 0 or event_scale < 0:
        raise ValueError("Invalid filter settings")
    y = np.asarray(observations.values)
    if y.ndim != 2 or y.shape[1] != config.n_assets or len(y) < 2 or not np.isfinite(y).all():
        raise ValueError("Invalid observations")
    a, q, r = config.transition, config.process_cov, config.observation_cov
    mean, cov = np.zeros(config.n_assets), initial_covariance(config)
    identity = np.eye(config.n_assets)
    predictions = np.empty((len(y)-1, config.n_assets))
    for t in range(len(y)-1):
        m, p, measurement = a @ mean, a @ cov @ a.T + q, r
        residual = y[t] - m
        if mode == "oracle" and oracle is not None and t == oracle.time:
            if oracle.kind == "state":
                p = p + event_scale**2 * identity
            else:
                measurement = r + event_scale**2 * identity
        if mode == "adaptive":
            excess = max(0., float((residual @ residual - np.trace(p + r)) / config.n_assets))
            p = p + .5 * excess * identity
            measurement = r + .5 * excess * identity
        s = p + measurement
        gain = np.linalg.solve(s, p.T).T
        update_residual = residual
        if mode == "clipped":
            distance = float(np.sqrt(max(0., residual @ np.linalg.solve(s, residual))))
            update_residual = residual * min(1., threshold / max(distance, 1e-15))
        mean = m + gain @ update_residual
        complement = identity - gain
        cov = complement @ p @ complement.T + gain @ measurement @ gain.T
        predictions[t] = a @ mean
    return predictions


def predictions(
    method: str, observed: Observations, config: Config, coefficients: Array,
    oracle: Event | None = None, scale: float = .5,
) -> Array:
    if method == "zero":
        return np.zeros_like(observed.values[:-1])
    if method == "linear":
        y = observed.values[:-1]
        return np.column_stack((np.ones(len(y)), y)) @ coefficients
    if method.startswith("clipped_"):
        return kalman(observed, config, "clipped", float(method.split("_")[1]))
    return kalman(observed, config, method, oracle=oracle, event_scale=scale)


def losses(forecast: Array, truth: GroundTruth) -> tuple[float, float, list[float]]:
    """Return category loss, whole-path warm-up-excluded loss, and five delays."""
    squared = np.mean((forecast - truth.latent[1:])**2, axis=1)
    whole = float(np.mean(squared[40:]))
    if not truth.events:
        return whole, whole, []
    time = truth.events[0].time
    delays = squared[time:time+5]
    if len(delays) != 5:
        raise ValueError("Incomplete scoring window")
    return float(np.mean(delays)), whole, delays.tolist()
