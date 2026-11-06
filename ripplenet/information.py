"""Exact scalar, single-origin Gaussian-mixture information diagnostic.

There is exactly one known intervention. With independent zero-mean Gaussian
b~N(0,P), d~N(0,T), e_y~N(0,R), e_z~N(0,U), its category has equal O/S priors.
Under O: X=b and y=b+d+e_y; under S: X=b+d and y=b+d+e_y. Clean z=X+e_z;
shared-control z=X+e_z+1{O}d; duplicate z=y. The future target is aX+w,
w~N(0,Q) independent of every observation. No future realization is an input.

Posterior means/variances are calculated from component covariance/cross-
covariance, and category weights from observation likelihoods only. Evaluators
may integrate under each generating component, but never pass its true category
to a predictor. Clean U=0 reveals X exactly; duplicate input reduces to y rather
than attempting to invert a singular two-dimensional covariance.

Deterministic tensor Gauss-Hermite quadrature reports direct posterior-variance
risk and squared conditional-mean differences. The default four orders are a
frozen diagnostic grid, not an adaptive accuracy/parameter search. Numerical
identity residuals are reported, never silently forced to zero. No data history,
fitting, detector, random sampling, market calibration or neural network exists
in this module. All conclusions are conditional on the stipulated model.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Literal

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]
Mode = Literal["clean", "shared", "duplicate"]
FROZEN_ORDERS = (24, 48, 96, 192)


@dataclass(frozen=True)
class InformationConfig:
    """Scalar variances, with P declared separately so an a=0 control keeps P."""

    a: float = .6
    process_variance: float = .01
    base_variance: float = .01 / (1-.6**2)
    measurement_variance: float = .0025
    disturbance_variance: float = .25
    auxiliary_variance: float = .0025

    def __post_init__(self) -> None:
        for name in ("a", "process_variance", "base_variance", "measurement_variance",
                     "disturbance_variance", "auxiliary_variance"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, Real) or not np.isfinite(value):
                raise ValueError(f"{name} must be a finite real scalar")
            if name != "a" and value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.base_variance <= 0 or self.measurement_variance <= 0:
            raise ValueError("Positive base and primary measurement variances required")


@dataclass(frozen=True)
class GaussianComponent:
    """Cov(observations), Cov(observations,X), and Var(X), without sample labels."""

    observation_covariance: Array
    state_cross_covariance: Array
    state_variance: float


@dataclass(frozen=True)
class Posterior:
    """Arrays follow the input batch shape; state_probability means category S."""

    mean: Array
    variance: Array
    state_probability: Array


@dataclass(frozen=True)
class InformationSummary:
    """Risks predict aX+w; gains have squared-target units, not percentages.

    Residuals use analytic_reference - direct_full - integrated_gain. The
    quadrature-linear risk is direct_full + approximation_gain, providing an
    additional comparison to its independently analytic reference.
    """

    mode: Mode
    order: int
    primary_risk: float
    full_risk: float
    linear_risk: float
    quadrature_primary_risk: float
    quadrature_linear_risk: float
    information_gain: float
    approximation_gain: float
    primary_risk_identity_residual: float
    linear_risk_identity_residual: float
    primary_quadrature_residual: float
    quadrature_weight_residual: float


def _readonly(values: object) -> Array:
    array = np.array(values, dtype=np.float64, copy=True)
    array.setflags(write=False)
    return array


def _mode(mode: str) -> None:
    if mode not in ("clean", "shared", "duplicate"):
        raise ValueError("Unknown observation mode")


def _nonnegative(value: float, reference: float) -> float:
    """Remove only tiny subtraction roundoff; no substantive PSD repair/jitter."""
    if not np.isfinite(value) or value < -1e-12 * max(1., abs(reference)):
        raise ValueError("Invalid conditional Gaussian variance")
    return max(0., float(value))


def observation_components(config: InformationConfig, mode: Mode = "clean") -> tuple[GaussianComponent, GaussianComponent]:
    """Return components in [O,S] order; their labels are not sample inputs."""
    _mode(mode)
    p, r, t, u = (config.base_variance, config.measurement_variance,
                  config.disturbance_variance, config.auxiliary_variance)
    v = p+t+r
    if mode == "duplicate":
        cov_o = cov_s = [[v, v], [v, v]]
        cross_o, cross_s = [p, p], [p+t, p+t]
    elif mode == "shared":
        cov_o = cov_s = [[v, p+t], [p+t, p+t+u]]
        cross_o, cross_s = [p, p], [p+t, p+t]
    else:
        cov_o, cov_s = [[v, p], [p, p+u]], [[v, p+t], [p+t, p+t+u]]
        cross_o, cross_s = [p, p], [p+t, p+t]
    return (
        GaussianComponent(_readonly(cov_o), _readonly(cross_o), float(p)),
        GaussianComponent(_readonly(cov_s), _readonly(cross_s), float(p+t)),
    )


def _gaussian_mixture(observations: Array, components: tuple[GaussianComponent, GaussianComponent]) -> Posterior:
    shape, dimension = observations.shape[:-1], observations.shape[-1]
    values = observations.reshape(-1, dimension)
    means, variances, likelihoods = [], [], []
    for component in components:
        covariance, cross = component.observation_covariance, component.state_cross_covariance
        try:
            root = np.linalg.cholesky(covariance)
        except np.linalg.LinAlgError as exc:
            raise ValueError("Positive definite component observation covariance required") from exc
        gain = np.linalg.solve(root.T, np.linalg.solve(root, cross))
        means.append(values @ gain)
        variances.append(_nonnegative(component.state_variance-cross @ gain, component.state_variance))
        whitened = np.linalg.solve(root, values.T)
        likelihoods.append(-.5*(dimension*np.log(2*np.pi)+2*np.log(np.diag(root)).sum()
                                 +np.sum(whitened**2, axis=0)))
    log_likelihood = np.stack(likelihoods, axis=1)
    log_likelihood -= np.max(log_likelihood, axis=1, keepdims=True)
    weights = np.exp(log_likelihood)
    weights /= weights.sum(axis=1, keepdims=True)
    branch_means = np.stack(means, axis=1)
    mean = np.sum(weights*branch_means, axis=1)
    variance = np.sum(weights*(np.array(variances)[None, :]+(branch_means-mean[:, None])**2), axis=1)
    if not (np.isfinite(mean).all() and np.isfinite(variance).all()):
        raise ValueError("Nonfinite posterior calculation")
    return Posterior(_readonly(mean.reshape(shape)), _readonly(variance.reshape(shape)),
                     _readonly(weights[:, 1].reshape(shape)))


def primary_posterior(y: object, config: InformationConfig = InformationConfig()) -> Posterior:
    """Exact X|y mixture; category likelihoods match and the mean is linear."""
    values = np.asarray(y, dtype=np.float64)
    if not np.isfinite(values).all():
        raise ValueError("Observations must be finite")
    p, t, r = config.base_variance, config.disturbance_variance, config.measurement_variance
    covariance = _readonly([[p+t+r]])
    components = (
        GaussianComponent(covariance, _readonly([p]), float(p)),
        GaussianComponent(covariance, _readonly([p+t]), float(p+t)),
    )
    return _gaussian_mixture(values[..., None], components)


def posterior(
    observations: object, config: InformationConfig = InformationConfig(), mode: Mode = "clean",
) -> Posterior:
    """Exact X|(y,z), without realized category, disturbance or future target."""
    _mode(mode)
    values = np.asarray(observations, dtype=np.float64)
    if values.ndim < 1 or values.shape[-1] != 2 or not np.isfinite(values).all():
        raise ValueError("Observations must be finite with last dimension (y,z)")
    if mode == "duplicate":
        if not np.array_equal(values[..., 0], values[..., 1]):
            raise ValueError("Duplicate control requires z exactly equal to y")
        return primary_posterior(values[..., 0], config)
    result = _gaussian_mixture(values, observation_components(config, mode))
    if mode == "clean" and config.auxiliary_variance == 0:
        # z=X exactly; avoid subtraction roundoff pretending residual uncertainty.
        return Posterior(_readonly(values[..., 1]), _readonly(np.zeros(values.shape[:-1])), result.state_probability)
    return result


def linear_mean(
    observations: object, config: InformationConfig = InformationConfig(), mode: Mode = "clean",
) -> Array:
    """Best affine (here zero-intercept linear) X estimate from identical inputs."""
    _mode(mode)
    values = np.asarray(observations, dtype=np.float64)
    if values.ndim < 1 or values.shape[-1] != 2 or not np.isfinite(values).all():
        raise ValueError("Observations must be finite with last dimension (y,z)")
    if mode == "duplicate":
        if not np.array_equal(values[..., 0], values[..., 1]):
            raise ValueError("Duplicate control requires z exactly equal to y")
        p, t, r = config.base_variance, config.disturbance_variance, config.measurement_variance
        return _readonly((p+.5*t)/(p+t+r)*values[..., 0])
    if mode == "clean" and config.auxiliary_variance == 0:
        return _readonly(values[..., 1])
    components = observation_components(config, mode)
    covariance = .5*(components[0].observation_covariance+components[1].observation_covariance)
    cross = .5*(components[0].state_cross_covariance+components[1].state_cross_covariance)
    gain = np.linalg.solve(covariance, cross)
    return _readonly(values @ gain)


def analytic_risks(config: InformationConfig = InformationConfig(), mode: Mode = "clean") -> tuple[float, float]:
    """Return analytic primary Bayes risk and same-input LMMSE future risk."""
    _mode(mode)
    p, t, r = config.base_variance, config.disturbance_variance, config.measurement_variance
    state_variance = p+.5*t
    primary = config.process_variance+config.a**2*(state_variance-state_variance**2/(p+t+r))
    if mode == "duplicate":
        return float(primary), float(primary)
    if mode == "clean" and config.auxiliary_variance == 0:
        return float(primary), float(config.process_variance)
    components = observation_components(config, mode)
    covariance = .5*(components[0].observation_covariance+components[1].observation_covariance)
    cross = .5*(components[0].state_cross_covariance+components[1].state_cross_covariance)
    variance = _nonnegative(state_variance-cross @ np.linalg.solve(covariance, cross), state_variance)
    return float(primary), float(config.process_variance+config.a**2*variance)


def _normal_grid(order: int) -> tuple[Array, Array]:
    """Tensor 2-D standard-normal expectation from physicists' Hermite rule."""
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)) or order < 2:
        raise ValueError("Quadrature order must be an integer >= 2")
    nodes, weights = np.polynomial.hermite.hermgauss(order)
    first, second = np.meshgrid(np.sqrt(2)*nodes, np.sqrt(2)*nodes, indexing="ij")
    grid = np.column_stack((first.ravel(), second.ravel()))
    probabilities = np.outer(weights, weights).ravel()/np.pi
    if not np.isfinite(grid).all() or not np.isfinite(probabilities).all() or np.any(probabilities < 0):
        raise ValueError("Invalid Gauss-Hermite rule")
    return grid, probabilities


def integrate(
    config: InformationConfig = InformationConfig(), mode: Mode = "clean", order: int = 24,
) -> InformationSummary:
    """Integrate each true component with prior .5, using no future draws.

    The generating component is used only to create deterministic integration
    coordinates; the exact same label-free posterior receives both components'
    points. Duplicate coordinates use the first normal axis and integrate out
    the unused second axis, retaining the common two-dimensional rule.
    """
    _mode(mode)
    grid, weights = _normal_grid(order)
    components = observation_components(config, mode)
    full_risk = quadrature_primary = information_gain = approximation_gain = 0.
    for component in components:
        if mode == "duplicate":
            y = np.sqrt(component.observation_covariance[0, 0])*grid[:, 0]
            observations = np.column_stack((y, y))
        else:
            observations = grid @ np.linalg.cholesky(component.observation_covariance).T
        full = posterior(observations, config, mode)
        primary = primary_posterior(observations[:, 0], config)
        linear = linear_mean(observations, config, mode)
        full_risk += .5*float(weights @ (config.process_variance+config.a**2*full.variance))
        quadrature_primary += .5*float(weights @ (config.process_variance+config.a**2*primary.variance))
        information_gain += .5*float(weights @ ((config.a*full.mean-config.a*primary.mean)**2))
        approximation_gain += .5*float(weights @ ((config.a*full.mean-config.a*linear)**2))
    primary_risk, linear_risk = analytic_risks(config, mode)
    return InformationSummary(
        mode, int(order), primary_risk, full_risk, linear_risk, quadrature_primary,
        full_risk+approximation_gain, information_gain, approximation_gain,
        primary_risk-full_risk-information_gain, linear_risk-full_risk-approximation_gain,
        primary_risk-quadrature_primary, float(weights.sum()-1),
    )
