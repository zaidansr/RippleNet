"""Exploratory replay of disclosed v2 histories, with frozen-output verification."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np

from .benchmark import configuration, worlds
from .history import known_time_forecasts
from .history_risk import conditional_risks

FROZEN_COMMIT = "06a4ced5bd5efda3ec2dbc4f752117b412427bf6"
FIELDS = ("future", "within_type", "type_information", "bayes", "projected_excess", "frozen_excess", "projected_total", "frozen_total", "category_oracle")


def original_filter():
    """Load the actual published uninstrumented implementation, not a rewrite."""
    for path in ("ripplenet/benchmark.py", "ripplenet/simulation.py"):
        check = subprocess.run(["git", "diff", "--exit-code", FROZEN_COMMIT, "--", path], capture_output=True, text=True)
        if check.returncode:
            raise RuntimeError(f"Frozen dependency changed: {path}")
    source = subprocess.check_output(["git", "show", f"{FROZEN_COMMIT}:ripplenet/history.py"], text=True)
    directory = Path("work")
    directory.mkdir(exist_ok=True)
    path = directory / "frozen-history-v2.py"
    path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("ripplenet._risk_frozen_v2", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.known_time_forecasts


def descriptive(values: dict[str, np.ndarray]) -> dict[str, object]:
    """Whole-seed descriptive intervals, never new confirmatory inference."""
    rng = np.random.default_rng(678901)
    n = len(values["bayes"])
    indices = rng.integers(0, n, size=(9999, n))
    means = {name: array[indices].mean(axis=1) for name, array in values.items()}
    output = {name: {"mean": float(array.mean()), "descriptive_ci95": np.quantile(means[name], [.025, .975]).tolist()} for name, array in values.items()}
    for name, numerator, denominator in (
        ("future_noise_fraction", "future", "bayes"),
        ("projection_improvement_fraction", "projected_excess", "projected_total"),
        ("frozen_improvement_fraction", "frozen_excess", "frozen_total"),
        ("category_information_fraction", "type_information", "bayes"),
    ):
        output[name] = {"ratio_of_means": float(values[numerator].mean()/values[denominator].mean()),
                        "descriptive_ci95": np.quantile(means[numerator]/means[denominator], [.025, .975]).tolist()}
    return output


def frozen_metrics(result, latent: np.ndarray, time: int, category: str) -> dict[str, float]:
    """Reproduce every numeric non-identifier column of the original v2 CSV."""
    metrics = {}
    forecasts = dict(result.forecasts)
    forecasts["oracle"] = forecasts[f"oracle_{category}"]
    for arm in ("retained", "projected", "frozen", "oracle"):
        score = np.mean((forecasts[arm]-latent[1:])**2, axis=1)[time:time+5]
        metrics[f"{arm}_mse"] = float(score[1:].mean())
        metrics[f"{arm}_five_origin_mse"] = float(score.mean())
        metrics[f"{arm}_delay0_mse"] = float(score[0])
    index = int(category == "state")
    probabilities = result.state_probability[time:time+5]
    metrics.update({"retained_type_nll": float(-result.log_type_probabilities[time+1:time+5,index].mean()),
                    "frozen_type_nll": float(np.log(2)), "retained_type_brier": float(np.mean((probabilities[1:]-index)**2)), "frozen_type_brier": .25})
    metrics.update({f"state_probability_delay{k}": float(p) for k,p in enumerate(probabilities)})
    return metrics


def reconstruct(output: Path) -> dict[str, object]:
    if output.exists():
        raise FileExistsError("Refusing to overwrite reconstruction or original results")
    frozen = original_filter()
    output.mkdir(parents=True)
    seeds = list(range(60000, 60128))
    summary = {"status": "exploratory_reconstruction_of_disclosed_v2_histories", "seed_blocks": seeds,
               "frozen_commit": FROZEN_COMMIT, "bootstrap_seed": 678901, "bootstrap_replicates": 9999,
               "source_tree_at_run": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], text=True).strip(),
               "python": platform.python_version(), "numpy": np.__version__, "settings": {}}
    for persistence in ("moderate", "zero"):
        config = configuration(persistence)
        source = Path(f"results/experiment-v2-final/{persistence}.csv")
        digest = hashlib.sha256(source.read_text(encoding="utf-8").encode()).hexdigest()
        with source.open(newline="", encoding="utf-8") as stream:
            frozen_rows = {(int(r["seed"]),r["category"]): r for r in csv.DictReader(stream)}
        if len(frozen_rows) != 256:
            raise AssertionError("Unexpected frozen seed/category count")
        records, blocks = [], {name: [] for name in FIELDS}
        max_metric_error, max_identity_error = 0., 0.
        for seed in seeds:
            paired = []
            run = worlds(config, seed, .5)
            for category in ("observation", "state"):
                sim = run[category]
                time = sim.truth.events[0].time
                result = known_time_forecasts(sim.observed, config, time, .5)
                original = frozen(sim.observed, config, time, .5)
                for arm in original.forecasts:
                    if not np.array_equal(result.forecasts[arm], original.forecasts[arm], equal_nan=True):
                        raise AssertionError("Instrumented forecast differs from frozen implementation")
                for field in ("state_probability", "log_type_probabilities"):
                    if not np.array_equal(getattr(result, field), getattr(original, field), equal_nan=True):
                        raise AssertionError("Instrumented type output differs from frozen implementation")
                metrics = frozen_metrics(result, sim.truth.latent, time, category)
                row = frozen_rows[(seed, category)]
                if set(metrics) != set(row)-{"seed", "category"}:
                    raise AssertionError("Frozen CSV column mismatch")
                error = max(abs(value-float(row[name])) for name,value in metrics.items())
                max_metric_error = max(max_metric_error, error)
                if error > 1e-14:
                    raise AssertionError("Reconstructed metric differs from frozen result")
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
                }
                selected = {name: v[time:time+5] for name,v in values.items()}
                for name, values5 in selected.items():
                    if not np.isfinite(values5).all() or values5.min() < -1e-12:
                        raise AssertionError("Invalid risk term")
                max_identity_error = max(max_identity_error, float(np.max(np.abs(selected["bayes"]-selected["future"]-selected["within_type"]-selected["type_information"]))))
                paired.append({name: float(v[1:].mean()) for name,v in selected.items()})
                for delay in range(5):
                    records.append({"seed": seed, "category": category, "delay": delay, **{name: float(v[delay]) for name,v in selected.items()}})
            for name in FIELDS:
                blocks[name].append(.5*(paired[0][name]+paired[1][name]))
        if hashlib.sha256(source.read_text(encoding="utf-8").encode()).hexdigest() != digest:
            raise AssertionError("Frozen CSV changed during reconstruction")
        with (output / f"{persistence}.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
        by_delay = {str(delay): {name: float(np.mean([r[name] for r in records if r["delay"]==delay])) for name in FIELDS} for delay in range(5)}
        if persistence == "zero":
            for record in records:
                if abs(record["bayes"]-.01)>1e-14 or max(record[name] for name in ("within_type", "type_information", "projected_excess", "frozen_excess"))>1e-14:
                    raise AssertionError("Zero-persistence negative control failed")
        item = {"disclosed_seed_blocks": 128, "per_origin_rows": len(records),
                "all_forecast_paths_bitwise_equal_to_frozen": True, "all_type_paths_bitwise_equal_to_frozen": True,
                "frozen_csv_sha256_canonical_text": digest, "max_frozen_metric_error": max_metric_error,
                "max_decomposition_identity_error": max_identity_error, "by_origin": by_delay,
                "delayed_origins_1_to_4": descriptive({name: np.array(v) for name,v in blocks.items()})}
        summary["settings"][persistence] = item
        print(json.dumps({"persistence": persistence, "max_frozen_metric_error": max_metric_error,
                          "delayed": item["delayed_origins_1_to_4"]}), flush=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/conditional-risk-v2"))
    reconstruct(parser.parse_args().output)
