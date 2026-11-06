"""Fixed R-only, known-time synthetic sensitivity; no fitting or cell selection.

Only ordinary measurement variance changes: Q=.01 I, R=ratio*Q. Dynamics,
intervention variance, true timing privilege, sample lengths and priors stay
fixed. Identical seeds couple process noise, event times/amplitudes and the
standardized measurement-noise stream across every cell. Both counterfactual
worlds, assets and delayed origins are aggregated within each independent seed.

Primary retention benefit is model-conditional excess/projected total risk,
not the realized MSE difference. Every grid cell is reported. Its pointwise
95% and five-cell Bonferroni 99% percentile-bootstrap intervals use identical
seed-index draws. Other intervals are descriptive 95% only. None establishes
real-market transfer or independent evidence of methodological novelty.

R=0 is valid because Q is positive definite. After the event, the current latent
state is then observed exactly: delayed forecasts coincide and all conditional
risk is the future process-noise floor. Realized MSE still fluctuates around
that floor and must not be asserted equal to it.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import replace
import hashlib
import json
from numbers import Real
from pathlib import Path
import platform
from typing import Sequence
import subprocess

import numpy as np

from .benchmark import configuration, worlds
from .history import known_time_forecasts
from .history_risk import conditional_risks
from .simulation import Config, GroundTruth


DEFAULT_RATIOS = (0., .25, 1., 4., 16.)
DEFAULT_SEEDS = tuple(range(70000, 70128))
BOOTSTRAP_SEED = 789012
BOOTSTRAP_REPLICATES = 9999
FAMILY_SIZE = 5
RISK_FIELDS = (
    "future", "within_type", "type_information", "bayes", "projected_excess",
    "frozen_excess", "projected_total", "frozen_total", "category_oracle",
)
SCORED_FIELDS = RISK_FIELDS + ("retained_mse", "projected_mse")


def configuration_for_ratio(ratio: float) -> Config:
    """Return fixed moderate dynamics with R=.01*ratio*I; no model fitting."""
    if (isinstance(ratio, bool) or not isinstance(ratio, Real)
            or not np.isfinite(ratio) or ratio < 0):
        raise ValueError("Ratios must be finite nonnegative real numbers")
    base = configuration("moderate")
    return replace(base, observation_cov=.01 * float(ratio) * np.eye(base.n_assets))


def _inputs(seeds: Sequence[int], ratios: Sequence[float]) -> tuple[tuple[int, ...], tuple[float, ...]]:
    seeds, ratios = tuple(seeds), tuple(ratios)
    if (len(seeds) < 2 or any(isinstance(s, bool) or not isinstance(s, (int, np.integer)) or s < 0 for s in seeds)
            or len(set(seeds)) != len(seeds)):
        raise ValueError("Need at least two unique nonnegative integer seed blocks")
    if not 1 <= len(ratios) <= FAMILY_SIZE:
        raise ValueError("Need one to five variance-ratio cells for the declared family")
    for ratio in ratios:
        configuration_for_ratio(ratio)
    if len(set(ratios)) != len(ratios):
        raise ValueError("Variance ratios must be unique")
    return tuple(int(s) for s in seeds), tuple(float(r) for r in ratios)


def _provenance() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    def git(*arguments: str) -> str:
        return subprocess.check_output(["git", *arguments], cwd=root, text=True).strip()
    files = (
        "ripplenet/noise_sensitivity.py", "ripplenet/history.py", "ripplenet/history_risk.py",
        "ripplenet/benchmark.py", "ripplenet/simulation.py",
    )
    return {
        "local_source_commit": git("rev-parse", "HEAD"),
        "source_tree_at_run": git("rev-parse", "HEAD^{tree}"),
        "source_provenance_note": (
            "The published source_tree_at_run is the content authority; the local "
            "commit may not be published because the GitHub connector can create "
            "a different commit with the identical source tree."
        ),
        "working_tree_status_before_output": git("status", "--porcelain"),
        "source_sha256": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in files},
        "python": platform.python_version(), "numpy": np.__version__,
    }


def _summaries(blocks: dict[str, np.ndarray], indices: np.ndarray) -> dict[str, object]:
    """Ratios of whole-seed means, with shared paired bootstrap index draws."""
    resamples = {name: values[indices].mean(axis=1) for name, values in blocks.items()}
    summary: dict[str, object] = {
        name: {"mean": float(values.mean()),
               "descriptive_ci95": np.quantile(resamples[name], [.025, .975]).tolist()}
        for name, values in blocks.items()
    }
    for name, numerator, denominator in (
        ("projection_improvement_fraction", "projected_excess", "projected_total"),
        ("category_information_fraction", "type_information", "bayes"),
        ("future_noise_fraction", "future", "bayes"),
    ):
        if blocks[denominator].mean() <= 0 or np.any(resamples[denominator] <= 0):
            raise ValueError("Positive conditional risk denominators required")
        draws = resamples[numerator] / resamples[denominator]
        item: dict[str, object] = {
            "ratio_of_means": float(blocks[numerator].mean() / blocks[denominator].mean()),
            "descriptive_ci95": np.quantile(draws, [.025, .975]).tolist(),
        }
        if name == "projection_improvement_fraction":
            item.update({"ci95": np.quantile(draws, [.025, .975]).tolist(),
                         "adjusted_ci99": np.quantile(draws, [.005, .995]).tolist(),
                         "adjustment_family_size": FAMILY_SIZE})
        summary[name] = item
    ceiling = 1 - resamples["future"] / resamples["projected_total"]
    summary["perfect_current_state_ceiling_fraction"] = {
        "ratio_of_means": float(1 - blocks["future"].mean() / blocks["projected_total"].mean()),
        "descriptive_ci95": np.quantile(ceiling, [.025, .975]).tolist(),
    }
    return summary


def evaluate(
    output: Path, *, seeds: Sequence[int] = DEFAULT_SEEDS, ratios: Sequence[float] = DEFAULT_RATIOS,
) -> dict[str, object]:
    """Evaluate every declared cell; refuse to overwrite any output directory.

    Defaults are the frozen five-cell/128-new-seed design. Explicit alternatives
    are marked custom/fixture in the manifest; intervals retain the declared
    five-cell adjustment and are not a license to select a favorable cell.
    Only true timing and the shared Gaussian scale enter prediction functions.
    Categories and latent states enter scoring/coupling checks only.
    """
    seeds, ratios = _inputs(seeds, ratios)
    output = Path(output)
    if output.exists():
        raise FileExistsError("Refusing to overwrite sensitivity results")
    provenance = _provenance()
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    indices = rng.integers(0, len(seeds), size=(BOOTSTRAP_REPLICATES, len(seeds)))
    summary: dict[str, object] = {
        "status": ("fixed_grid_r_only_sensitivity" if seeds == DEFAULT_SEEDS and ratios == DEFAULT_RATIOS
                   else "custom_or_fixture_configuration"),
        "seed_blocks": list(seeds), "ratios": list(ratios), "event_scale": .5,
        "primary_origins": "tau+1 through tau+4", "saved_origins": "tau through tau+4",
        "shared_privilege": "true intervention time; exactly one Gaussian intervention; known parameters",
        "bootstrap_seed": BOOTSTRAP_SEED, "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "primary_family_size": FAMILY_SIZE,
        "interval_scope": "primary: pointwise95 and five-cell99; others: descriptive95; no cell selection",
        **provenance, "cells": [],
    }
    base = configuration("moderate")
    summary["fixed_settings"] = {
        "transition": base.transition.tolist(), "process_cov": base.process_cov.tolist(),
        "n_steps": base.n_steps, "burn_in": base.burn_in, "type_prior": [.5, .5],
    }
    output.mkdir(parents=True)
    # References store only scoring/check data and never enter a filter update.
    references: dict[int, tuple[dict[str, GroundTruth], np.ndarray | None]] = {}
    for cell_index, ratio in enumerate(ratios):
        config = configuration_for_ratio(ratio)
        cell_id = f"r{cell_index:02d}"
        records: list[dict[str, object]] = []
        blocks = {field: [] for field in SCORED_FIELDS}
        max_prefix_gap = max_origin_zero_gap = max_identity_error = 0.
        max_origin_zero_probability_gap = 0.
        max_zero_r_forecast_gap = max_zero_r_floor_error = max_zero_r_state_risk = 0.
        max_standardized_noise_gap = 0.
        for seed in seeds:
            run = worlds(config, seed, .5)
            if seed not in references:
                references[seed] = ({c: run[c].truth for c in ("clean", "observation", "state")}, None)
            truths, standardized_reference = references[seed]
            for category in ("clean", "observation", "state"):
                reference = truths[category]
                if (not np.array_equal(run[category].truth.latent, reference.latent)
                        or run[category].truth.events != reference.events):
                    raise AssertionError("Process path or intervention changed across R cells")
            measurement_noise = run["clean"].observed.values - run["clean"].truth.latent
            if ratio == 0:
                if np.any(measurement_noise != 0):
                    raise AssertionError("R=0 contains ordinary measurement noise")
            else:
                standardized = measurement_noise / np.sqrt(.01 * ratio)
                if standardized_reference is None:
                    references[seed] = (truths, standardized.copy())
                else:
                    gap = float(np.max(np.abs(standardized - standardized_reference)))
                    max_standardized_noise_gap = max(max_standardized_noise_gap, gap)
                    if gap > 1e-11:
                        raise AssertionError("Standardized measurement stream changed across R")
            paired = []
            results = {}
            for category in ("observation", "state"):
                sim = run[category]
                time = sim.truth.events[0].time
                result = known_time_forecasts(sim.observed, config, time, .5)
                results[category] = result
                max_origin_zero_probability_gap = max(
                    max_origin_zero_probability_gap, abs(float(result.state_probability[time])-.5),
                )
                risks = conditional_risks(result)
                values = {
                    "future": result.future_innovation_risk,
                    "within_type": result.within_type_state_risk,
                    "type_information": result.type_information_risk,
                    "bayes": result.bayes_risk,
                    "projected_excess": risks.excess_risk["projected"],
                    "frozen_excess": risks.excess_risk["frozen"],
                    "projected_total": risks.total_risk["projected"],
                    "frozen_total": risks.total_risk["frozen"],
                    "category_oracle": risks.total_risk["category_oracle"],
                    "retained_mse": np.mean((result.forecasts["retained"]-sim.truth.latent[1:])**2, axis=1),
                    "projected_mse": np.mean((result.forecasts["projected"]-sim.truth.latent[1:])**2, axis=1),
                }
                selected = {name: values5[time:time+5] for name, values5 in values.items()}
                if any(not np.isfinite(v).all() or v.min() < -1e-12 for v in selected.values()):
                    raise AssertionError("Nonfinite or materially negative score")
                identity = selected["bayes"]-selected["future"]-selected["within_type"]-selected["type_information"]
                max_identity_error = max(max_identity_error, float(np.max(np.abs(identity))))
                for arm in ("projected", "frozen"):
                    max_origin_zero_gap = max(max_origin_zero_gap, float(np.max(np.abs(
                        result.forecasts[arm][time] - result.forecasts["retained"][time]))))
                if ratio == 0:
                    max_zero_r_forecast_gap = max(max_zero_r_forecast_gap, max(float(np.max(np.abs(
                        result.forecasts[arm][time+1:time+5]-result.forecasts["retained"][time+1:time+5])))
                        for arm in ("projected", "frozen")))
                    max_zero_r_floor_error = max(max_zero_r_floor_error, float(np.max(np.abs(selected["bayes"][1:]-.01))))
                    max_zero_r_state_risk = max(max_zero_r_state_risk, max(float(np.max(np.abs(selected[f][1:])))
                        for f in ("within_type", "type_information", "projected_excess", "frozen_excess")))
                paired.append({name: float(v[1:].mean()) for name, v in selected.items()})
                for delay in range(5):
                    records.append({"seed": seed, "category": category, "delay": delay, "ratio": ratio,
                                    **{name: float(v[delay]) for name, v in selected.items()},
                                    "state_probability": float(result.state_probability[time+delay]),
                                    "log_observation_probability": float(result.log_type_probabilities[time+delay, 0]),
                                    "log_state_probability": float(result.log_type_probabilities[time+delay, 1])})
            for field in SCORED_FIELDS:
                blocks[field].append(.5 * (paired[0][field]+paired[1][field]))
            for arm in ("retained", "projected", "frozen"):
                max_prefix_gap = max(max_prefix_gap, float(np.max(np.abs(
                    results["observation"].forecasts[arm][:time+1]
                    - results["state"].forecasts[arm][:time+1]))))
        if max(max_prefix_gap, max_origin_zero_gap, max_origin_zero_probability_gap, max_identity_error,
               max_zero_r_forecast_gap, max_zero_r_floor_error, max_zero_r_state_risk) > 1e-12:
            raise AssertionError("Causal, risk identity, or R=0 control failed")
        path = output / f"{cell_id}.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
        cell = {
            "cell_id": cell_id, "ratio": ratio, "path": path.name, "per_origin_rows": len(records),
            "measurement_cov": config.observation_cov.tolist(),
            "by_origin": {str(delay): {name: float(np.mean([r[name] for r in records if r["delay"] == delay]))
                                       for name in SCORED_FIELDS} for delay in range(5)},
            "delayed_origins_1_to_4": _summaries({name: np.array(v) for name, v in blocks.items()}, indices),
            "checks": {"max_matched_prefix_gap": max_prefix_gap, "max_origin_zero_arm_gap": max_origin_zero_gap,
                       "max_origin_zero_probability_gap": max_origin_zero_probability_gap,
                       "max_risk_identity_error": max_identity_error, "max_standardized_noise_gap": max_standardized_noise_gap,
                       "latent_and_event_coupling_exact": True, "max_zero_r_forecast_gap": max_zero_r_forecast_gap,
                       "max_zero_r_floor_error": max_zero_r_floor_error, "max_zero_r_state_risk": max_zero_r_state_risk},
        }
        summary["cells"].append(cell)
        print(json.dumps({"cell_id": cell_id, "ratio": ratio, "checks": cell["checks"],
                          "projection_improvement_fraction": cell["delayed_origins_1_to_4"]["projection_improvement_fraction"]}), flush=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/noise-sensitivity-v1"))
    parser.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--ratios", nargs="+", type=float, default=DEFAULT_RATIOS)
    args = parser.parse_args()
    evaluate(args.output, seeds=args.seeds, ratios=args.ratios)
