"""Causal standard Kalman baseline; no smoothing or event-label input."""

from __future__ import annotations

import numpy as np

from .simulation import Array, Config, Observations


def causal_forecasts(observations: Observations, config: Config) -> Array:
    """Return row t predicting x[t+1] using only observations y[0:t+1].

    Known A,Q,R and a zero-mean identity-covariance pre-observation prior are
    supplied to this diagnostic baseline. The actual burned-in prior differs;
    benchmark work must align initialization or discard an adequate warm-up.
    The covariance uses Joseph's form, and linear solves replace inversion.
    Singular predictive observation covariance raises ValueError explicitly.
    """
    y = np.asarray(observations.values, dtype=np.float64)
    if y.ndim != 2 or y.shape[1] != config.n_assets or len(y) < 2 or not np.isfinite(y).all():
        raise ValueError("Expected finite observations with shape (time>=2, assets)")
    a, q, r = config.transition, config.process_cov, config.observation_cov
    mean = np.zeros(config.n_assets)
    covariance = np.eye(config.n_assets)
    identity = np.eye(config.n_assets)
    predictions = np.empty((len(y) - 1, config.n_assets))
    for time in range(len(y) - 1):
        prior_mean = a @ mean
        prior_cov = a @ covariance @ a.T + q
        residual_cov = prior_cov + r
        try:
            gain = np.linalg.solve(residual_cov, prior_cov.T).T
        except np.linalg.LinAlgError as error:
            raise ValueError("Singular predictive observation covariance") from error
        mean = prior_mean + gain @ (y[time] - prior_mean)
        complement = identity - gain
        covariance = complement @ prior_cov @ complement.T + gain @ r @ gain.T
        predictions[time] = a @ mean
    return predictions
