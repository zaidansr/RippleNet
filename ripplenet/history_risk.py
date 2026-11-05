"""Causal conditional-risk diagnostics for the stipulated known-time model.

Let H_t contain observations available at time t and the shared intervention
timing/parameter information. If m_t is the retained Bayesian forecast, squared
loss obeys E[||x[t+1]-g||^2/n | H_t] = BayesRisk_t + ||g-m_t||^2/n. The added
term is an exact conditional expected excess under this specified generator,
not a realized forecast error or fresh confirmatory evidence.

BayesRisk = tr(Q)/n + sum_z pi_z tr(A P_z A.T)/n
            + pi_O pi_S ||A(m_S-m_O)||^2/n.

The category-oracle risk below averages its conditional risks over the current
posterior category weights. It equals future plus within-type risk and never
selects an oracle output using the realized category. The type-information
term is therefore its conditional expected advantage over retained inference.
No latent targets, true categories, event amplitudes, or future data are inputs.
All reported arrays are NaN before the known event, and no risk is clipped.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .history import HistoryResult
from .simulation import Array


@dataclass(frozen=True)
class ConditionalRisks:
    """Read-only per-origin conditional losses normalized by asset count.

    ``excess_risk`` keys are ``projected`` and ``frozen``. ``total_risk`` keys
    are ``retained``, ``projected``, ``frozen`` and ``category_oracle``.
    Dictionaries contain diagnostic arrays, not filter update instructions.
    """

    excess_risk: dict[str, Array]
    total_risk: dict[str, Array]


def conditional_risks(result: HistoryResult) -> ConditionalRisks:
    """Compute exact conditional excess for already-produced causal forecasts.

    Inputs must have consistent output shapes and the common pre-event NaN
    mask supplied by ``known_time_forecasts``. Tiny negative covariance traces
    from floating-point arithmetic are tolerated to -1e-12; values are retained
    rather than silently clipped or substituted. Materially invalid risks fail.
    """
    retained = np.asarray(result.forecasts["retained"])
    if retained.ndim != 2 or retained.shape[0] < 1 or retained.shape[1] < 1:
        raise ValueError("Retained forecasts must have nonempty (origins, assets) shape")
    if not np.isfinite(retained).all():
        raise ValueError("Forecasts must be finite")
    count = len(retained)
    fields = (
        result.future_innovation_risk, result.within_type_state_risk,
        result.type_information_risk, result.bayes_risk,
    )
    if any(np.shape(values) != (count,) for values in fields):
        raise ValueError("Risk arrays must have one value per forecast origin")
    mask = np.isfinite(result.bayes_risk)
    if (not mask.any() or np.any(mask[:-1] & ~mask[1:])
            or any(not np.array_equal(np.isfinite(values), mask) for values in fields)
            or any(not np.isnan(values[~mask]).all() for values in fields)):
        raise ValueError("Risks must share one contiguous post-event finite suffix")
    if any(np.min(values[mask]) < -1e-12 for values in fields):
        raise ValueError("Conditional risks must be nonnegative within numerical tolerance")
    if not np.allclose(
        result.bayes_risk[mask], sum(values[mask] for values in fields[:3]),
        rtol=1e-12, atol=1e-14,
    ):
        raise ValueError("Bayes risk must equal the three risk components")

    excess: dict[str, Array] = {}
    totals: dict[str, Array] = {"retained": np.array(result.bayes_risk, copy=True)}
    for method in ("projected", "frozen"):
        forecast = np.asarray(result.forecasts[method])
        if forecast.shape != retained.shape or not np.isfinite(forecast).all():
            raise ValueError("Comparator forecasts must be finite and match retained shape")
        values = np.full(count, np.nan)
        values[mask] = np.mean((forecast[mask] - retained[mask])**2, axis=1)
        if not np.isfinite(values[mask]).all():
            raise ValueError("Nonfinite conditional excess risk")
        excess[method] = values
        totals[method] = result.bayes_risk + values
    totals["category_oracle"] = result.future_innovation_risk + result.within_type_state_risk
    for values in (*excess.values(), *totals.values()):
        values.setflags(write=False)
    return ConditionalRisks(excess, totals)
