"""Exact, known-intervention-time two-hypothesis filtering diagnostic.

Assume x[t]=A x[t-1]+w[t], y[t]=x[t]+v[t], except for exactly one event
at the supplied time tau. Its type is observation/state with prior (1/2,1/2)
and its amplitude is N(0, scale**2 I). All arms know tau, scale, A, Q and R,
but never the realized amplitude, true category, or latent state. There are no
later events. Innovation covariances must be positive definite; this module
does not silently jitter singular models. These privileges define a mechanism
diagnostic, not an operational event detector or a realistic market model.

The retained arm preserves both conditional Gaussian posteriors and Bayesian
type weights. The frozen ablation updates the identical component filters but
keeps weights at 1/2. The projected arm matches the mixture's first two moments
ONCE at tau, then evolves independently. With branch means m[j], covariances
P[j], and weights p[j], the projection is m=sum(p[j]m[j]) and
P=sum(p[j](P[j]+(m[j]-m)(m[j]-m).T)). Recopying retained moments later would
make the point-forecast comparator tautological and is not done here.

Forecast row t predicts latent x[t+1] using only y[:t+1]. Category logs are
normalized log probabilities, columns [observation, state], and remain in log
space for proper scoring without probability clipping. Arrays before tau are
NaN because this diagnostic does not estimate pre-event category probabilities.
No random draws occur in filtering; reproducibility comes from input data.

The additional risk instrumentation is model-conditional and exploratory. For
t >= tau it decomposes latent next-return squared-error Bayes risk into future
process noise, within-type state uncertainty, and unresolved-type uncertainty,
each normalized by the number of assets. Future measurement noise R is absent
because the target is the latent state, not the next recorded observation.
Risk calculations do not feed back into any forecast or log-weight update.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real

import numpy as np

from .benchmark import initial_covariance
from .simulation import Array, Config, Observations


@dataclass(frozen=True)
class HistoryResult:
    """Read-only result arrays; oracle keys are conditional branch forecasts.

    Evaluation chooses the matching oracle output using its private true type.
    This function itself never receives that true type.
    """

    forecasts: dict[str, Array]
    state_probability: Array
    log_type_probabilities: Array
    future_innovation_risk: Array
    within_type_state_risk: Array
    type_information_risk: Array
    bayes_risk: Array


def _normalized_logs(log_weights: Array) -> Array:
    """Normalize finite log weights without exponentiating their full scale."""
    if not np.isfinite(log_weights).all():
        raise ValueError("Nonfinite type log weights")
    maximum = np.max(log_weights)
    shifted = log_weights - maximum
    return shifted - np.log(np.exp(shifted).sum())


def _weighted_moments(means: Array, covariances: Array, weights: Array) -> tuple[Array, Array]:
    """Project a normalized mixture; include its between-component covariance."""
    mean = np.sum(weights[:, None] * means, axis=0)
    offsets = means - mean
    covariance = np.sum(
        weights[:, None, None]
        * (covariances + offsets[:, :, None] * offsets[:, None, :]), axis=0,
    )
    return mean, (covariance + covariance.T) / 2


def _step(
    mean: Array, covariance: Array, observation: Array,
    transition: Array, process_covariance: Array, measurement_covariance: Array,
) -> tuple[Array, Array, float]:
    """One Gaussian update and log p(y[t] | y[:t], branch).

    Gain is computed by Cholesky solves. Joseph's update preserves covariance
    symmetry/PSD more reliably than subtracting nearly equal matrices.
    """
    predicted_mean = transition @ mean
    predicted_covariance = transition @ covariance @ transition.T + process_covariance
    innovation = observation - predicted_mean
    innovation_covariance = predicted_covariance + measurement_covariance
    try:
        root = np.linalg.cholesky(innovation_covariance)
    except np.linalg.LinAlgError as exc:
        raise ValueError("Positive definite innovation covariance required") from exc
    whitened = np.linalg.solve(root, innovation)
    gain = np.linalg.solve(root.T, np.linalg.solve(root, predicted_covariance.T)).T
    updated_mean = predicted_mean + gain @ innovation
    complement = np.eye(len(mean)) - gain
    updated_covariance = (
        complement @ predicted_covariance @ complement.T
        + gain @ measurement_covariance @ gain.T
    )
    updated_covariance = (updated_covariance + updated_covariance.T) / 2
    log_likelihood = -.5 * (
        len(mean) * np.log(2 * np.pi)
        + 2 * np.log(np.diag(root)).sum() + whitened @ whitened
    )
    if not (np.isfinite(updated_mean).all() and np.isfinite(updated_covariance).all()
            and np.isfinite(log_likelihood)):
        raise ValueError("Nonfinite Gaussian filter calculation")
    return updated_mean, updated_covariance, float(log_likelihood)


def known_time_forecasts(
    observed: Observations, config: Config, event_time: int, scale: float = .5,
) -> HistoryResult:
    """Compare exact history retention, independent projection and fixed weights.

    ``event_time`` indexes an observation and must leave at least one target
    observation afterward. Input length need not equal ``config.n_steps``;
    prefixes can therefore be evaluated without access to future observations.
    The observation/state branches have the same innovation law at the event,
    so equal posterior weights are set exactly there. Subsequent data update
    log weights; branch-conditional trajectories are shared with the frozen
    ablation and the two category-oracle outputs.
    """
    values = np.asarray(observed.values, dtype=np.float64)
    if (values.ndim != 2 or values.shape[1] != config.n_assets
            or len(values) < 2 or not np.isfinite(values).all()):
        raise ValueError("Observations must be a finite (T, n_assets) array, T >= 2")
    if (isinstance(event_time, bool) or not isinstance(event_time, (int, np.integer))
            or not 0 <= event_time < len(values) - 1):
        raise ValueError("event_time must be an integer with a subsequent target")
    if (isinstance(scale, bool) or not isinstance(scale, Real)
            or not np.isfinite(scale) or scale < 0
            or scale > np.sqrt(np.finfo(np.float64).max)):
        raise ValueError("scale must be a finite nonnegative standard deviation")

    a, q, r = config.transition, config.process_cov, config.observation_cov
    extra = float(scale)**2 * np.eye(config.n_assets)
    count = len(values) - 1
    names = ("retained", "projected", "frozen", "oracle_observation", "oracle_state")
    forecasts = {name: np.empty((count, config.n_assets)) for name in names}
    state_probability = np.full(count, np.nan)
    log_probabilities = np.full((count, 2), np.nan)
    future_innovation_risk = np.full(count, np.nan)
    within_type_state_risk = np.full(count, np.nan)
    type_information_risk = np.full(count, np.nan)
    bayes_risk = np.full(count, np.nan)
    mean, covariance = np.zeros(config.n_assets), initial_covariance(config)
    means = np.empty((2, config.n_assets))
    covariances = np.empty((2, config.n_assets, config.n_assets))
    log_weights = np.full(2, -np.log(2.))
    projected_mean, projected_covariance = mean.copy(), covariance.copy()

    for time in range(count):
        observation = values[time]
        if time < event_time:
            mean, covariance, _ = _step(mean, covariance, observation, a, q, r)
            forecast = a @ mean
            for output in forecasts.values():
                output[time] = forecast
            continue
        if time == event_time:
            means[0], covariances[0], _ = _step(mean, covariance, observation, a, q, r + extra)
            means[1], covariances[1], _ = _step(mean, covariance, observation, a, q + extra, r)
            projected_mean, projected_covariance = _weighted_moments(
                means, covariances, np.full(2, .5),
            )
        else:
            likelihoods = np.empty(2)
            for branch in range(2):
                means[branch], covariances[branch], likelihoods[branch] = _step(
                    means[branch], covariances[branch], observation, a, q, r,
                )
            log_weights = _normalized_logs(log_weights + likelihoods)
            projected_mean, projected_covariance, _ = _step(
                projected_mean, projected_covariance, observation, a, q, r,
            )
        weights = np.exp(log_weights)
        retained_mean = np.sum(weights[:, None] * means, axis=0)
        forecasts["retained"][time] = a @ retained_mean
        forecasts["projected"][time] = a @ projected_mean
        forecasts["frozen"][time] = a @ means.mean(axis=0)
        forecasts["oracle_observation"][time] = a @ means[0]
        forecasts["oracle_state"][time] = a @ means[1]
        state_probability[time] = weights[1]
        log_probabilities[time] = log_weights

        # Diagnostic only: these operations never mutate the filtering state.
        future_innovation_risk[time] = np.trace(q) / config.n_assets
        within_type_state_risk[time] = sum(
            weight * np.trace(a @ branch_covariance @ a.T)
            for weight, branch_covariance in zip(weights, covariances)
        ) / config.n_assets
        type_difference = a @ (means[1] - means[0])
        type_information_risk[time] = (
            weights[0] * weights[1] * (type_difference @ type_difference)
            / config.n_assets
        )
        bayes_risk[time] = (
            future_innovation_risk[time] + within_type_state_risk[time]
            + type_information_risk[time]
        )

    for output in (
        *forecasts.values(), state_probability, log_probabilities,
        future_innovation_risk, within_type_state_risk, type_information_risk, bayes_risk,
    ):
        output.setflags(write=False)
    return HistoryResult(
        forecasts, state_probability, log_probabilities,
        future_innovation_risk, within_type_state_risk, type_information_risk, bayes_risk,
    )
