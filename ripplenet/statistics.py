"""Paired run-level bootstrap; intervals are approximate, conditional on generator."""

from __future__ import annotations

import numpy as np

from .simulation import Array


def paired_comparison(method: Array, reference: Array, family_size: int = 1) -> dict[str, object]:
    """Resample entire paired runs; use ratio of means, not mean of ratios."""
    method, reference = np.asarray(method, float), np.asarray(reference, float)
    if method.ndim != 1 or method.shape != reference.shape or len(method) < 2:
        raise ValueError("Need >=2 paired one-dimensional run losses")
    if not np.isfinite(method).all() or not np.isfinite(reference).all() or np.any(method < 0) or np.any(reference <= 0):
        raise ValueError("Need finite nonnegative losses and positive reference losses")
    if not isinstance(family_size, int) or family_size < 1:
        raise ValueError("family_size must be a positive integer")
    rng = np.random.default_rng(456789)
    indices = rng.integers(0, len(method), size=(9999, len(method)))
    gain = 1 - method[indices].mean(axis=1) / reference[indices].mean(axis=1)
    alpha = .05 / family_size
    return {
        "method_mse": float(method.mean()), "reference_mse": float(reference.mean()),
        "absolute_mse_reduction": float(np.mean(reference-method)),
        "relative_improvement": float(1-method.mean()/reference.mean()),
        "ci95": np.quantile(gain, [.025, .975]).tolist(),
        "adjusted_ci": np.quantile(gain, [alpha/2, 1-alpha/2]).tolist(),
        "family_size": family_size, "n_independent_seeds": len(method),
    }
