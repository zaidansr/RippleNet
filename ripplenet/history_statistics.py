"""Seed-block paired bootstrap for the predeclared history-retention experiment.

Each element is one independent simulation seed's already aggregated loss. Worlds,
assets and forecast origins coupled within a seed are not independent replicates.
Intervals are percentile-bootstrap approximations conditional on the generator;
Bonferroni adjustment does not make their finite-sample coverage exact.
"""

from __future__ import annotations

import numpy as np

from .simulation import Array


def paired_comparison(
    method: Array,
    reference: Array,
    *,
    relative: bool = True,
    family_size: int = 5,
) -> dict[str, object]:
    """Compare paired nonnegative run losses; positive improvement favors method.

    In relative mode, improvement is ``1 - mean(method)/mean(reference)``.
    It is a ratio of means, never the average of per-seed ratios. In absolute
    mode, improvement is ``mean(reference - method)`` in the input loss units
    (for example squared-return units or nats for negative log probability).

    Exactly 9,999 bootstrap replicates resample the same seed indices for both
    methods, using a local RNG seeded 567890. ``ci95`` is unadjusted; the adjusted
    interval uses alpha ``0.05/family_size``. The caller must declare its family
    and aggregate within seeds before calling. Repeated calls deliberately use
    the same index draws for equally sized vectors without changing global RNG.

    Zero individual losses are allowed. Relative inference requires a positive
    reference mean in the sample and every bootstrap resample. If a resample has
    zero reference mean, the ratio interval is undefined; raise rather than drop
    those resamples or insert arbitrary epsilon values. Use absolute mode then.
    """
    if not isinstance(relative, (bool, np.bool_)):
        raise ValueError("relative must be a boolean")
    if (
        isinstance(family_size, (bool, np.bool_))
        or not isinstance(family_size, (int, np.integer))
        or family_size < 1
    ):
        raise ValueError("family_size must be a positive integer")
    if np.iscomplexobj(method) or np.iscomplexobj(reference):
        raise ValueError("Losses must be real-valued")
    method = np.asarray(method, dtype=np.float64)
    reference = np.asarray(reference, dtype=np.float64)
    if method.ndim != 1 or reference.ndim != 1 or method.shape != reference.shape:
        raise ValueError("Need matching one-dimensional seed-loss vectors")
    if len(method) < 2:
        raise ValueError("Need at least two independent paired seeds")
    if (
        not np.isfinite(method).all()
        or not np.isfinite(reference).all()
        or np.any(method < 0)
        or np.any(reference < 0)
    ):
        raise ValueError("Need finite nonnegative losses")

    method_mean = float(method.mean())
    reference_mean = float(reference.mean())
    if not np.isfinite(method_mean) or not np.isfinite(reference_mean):
        raise ValueError("Loss means must be finite; rescale the input losses")
    if relative and reference_mean <= 0:
        raise ValueError("Relative improvement needs a positive reference mean")

    rng = np.random.default_rng(567890)
    indices = rng.integers(0, len(method), size=(9999, len(method)))
    if relative:
        reference_resamples = reference[indices].mean(axis=1)
        if np.any(reference_resamples <= 0):
            raise ValueError(
                "Relative bootstrap has a zero reference mean; use absolute mode"
            )
        bootstrap = 1.0 - method[indices].mean(axis=1) / reference_resamples
        improvement = 1.0 - method_mean / reference_mean
    else:
        differences = reference - method
        bootstrap = differences[indices].mean(axis=1)
        improvement = float(differences.mean())
    if not np.isfinite(bootstrap).all() or not np.isfinite(improvement):
        raise ValueError("Comparison overflowed; rescale the input losses")

    alpha = 0.05 / int(family_size)
    return {
        "method_mean": method_mean,
        "reference_mean": reference_mean,
        "improvement": float(improvement),
        "ci95": np.quantile(bootstrap, [0.025, 0.975]).tolist(),
        "adjusted_ci": np.quantile(bootstrap, [alpha / 2, 1 - alpha / 2]).tolist(),
        "n_seeds": len(method),
        "units": "relative_fraction" if relative else "loss_units",
        "family_size": int(family_size),
        "bootstrap_replicates": 9999,
        "bootstrap_seed": 567890,
    }
