"""Causal three-hypothesis filter and matched-branch-count ablations.

The posterior is collapsed to a single Gaussian after every update. This loses
event-history multimodality and is not CE-BASS. Equal total current-event noise
means the observation/process branches have equal instantaneous likelihoods;
any gain cannot by itself demonstrate successful event-type identification.
"""

from __future__ import annotations

import numpy as np

from .benchmark import initial_covariance
from .simulation import Array, Config, Observations


def update(
    mean: Array, covariance: Array, observation: Array, config: Config,
    mode: str = "dual", scale: float = .5, event_probability: float = .01,
) -> tuple[Array, Array]:
    """One online update; no time, event labels or realised amplitudes supplied."""
    if mode not in ("dual", "observation_only", "pooled"):
        raise ValueError("Unknown mixture mode")
    if scale < 0 or not 0 < event_probability < 1:
        raise ValueError("Invalid mixture settings")
    a, q, r = config.transition, config.process_cov, config.observation_cov
    identity = np.eye(config.n_assets)
    extra = scale**2 * identity
    # Entries are (extra process covariance, extra measurement covariance).
    branches = {
        "dual": ((0., 0.), (0., extra), (extra, 0.)),
        "observation_only": ((0., 0.), (0., extra), (0., extra)),
        "pooled": ((0., 0.), (.5*extra, .5*extra), (.5*extra, .5*extra)),
    }[mode]
    priors = np.array([1-event_probability, event_probability/2, event_probability/2])
    prior_mean = a @ mean
    prior_cov = a @ covariance @ a.T + q
    residual = observation - prior_mean
    means, covariances, logweights = [], [], []
    for probability, (process_extra, measurement_extra) in zip(priors, branches):
        p, measurement = prior_cov + process_extra, r + measurement_extra
        s = p + measurement
        sign, logdet = np.linalg.slogdet(s)
        if sign <= 0:
            raise ValueError("Mixture requires positive definite residual covariance")
        gain = np.linalg.solve(s, p.T).T
        branch_mean = prior_mean + gain @ residual
        complement = identity - gain
        branch_cov = complement @ p @ complement.T + gain @ measurement @ gain.T
        loglikelihood = -.5 * (logdet + residual @ np.linalg.solve(s, residual))
        means.append(branch_mean)
        covariances.append(branch_cov)
        logweights.append(float(np.log(probability) + loglikelihood))
    weights = np.exp(np.array(logweights) - np.max(logweights))
    weights /= weights.sum()
    collapsed_mean = np.sum(weights[:, None] * np.array(means), axis=0)
    collapsed_cov = np.zeros_like(covariance)
    for weight, branch_mean, branch_cov in zip(weights, means, covariances):
        delta = branch_mean - collapsed_mean
        collapsed_cov += weight * (branch_cov + np.outer(delta, delta))
    return collapsed_mean, (collapsed_cov + collapsed_cov.T) / 2


def mixture_forecasts(observed: Observations, config: Config, mode: str = "dual") -> Array:
    """Forecast x[t+1] from y[:t+1] with frozen scale .5 and event prior .01."""
    y = np.asarray(observed.values)
    if y.ndim != 2 or y.shape[1] != config.n_assets or len(y) < 2 or not np.isfinite(y).all():
        raise ValueError("Invalid observations")
    mean, covariance = np.zeros(config.n_assets), initial_covariance(config)
    result = np.empty((len(y)-1, config.n_assets))
    for time in range(len(y)-1):
        mean, covariance = update(mean, covariance, y[time], config, mode)
        result[time] = config.transition @ mean
    return result
