"""Run v2: shared true timing, exact mixture and independent projection control."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

from .benchmark import configuration, worlds
from .history import known_time_forecasts
from .history_statistics import paired_comparison

ARMS = ("retained", "projected", "frozen", "oracle")
CATEGORIES = ("observation", "state")


def evaluate(stage: str, output: Path) -> dict[str, object]:
    """Save per-seed category losses; never use true category in ordinary updates."""
    if stage not in ("development", "final"):
        raise ValueError("Unknown experiment stage")
    if output.exists():
        raise FileExistsError("Refusing to overwrite experiment results")
    seeds = list(range(50000, 50032)) if stage == "development" else list(range(60000, 60128))
    output.mkdir(parents=True)
    summary: dict[str, object] = {
        "stage": stage, "seed_blocks": seeds, "event_scale": .5,
        "shared_privilege": "true intervention time; exactly one Gaussian intervention; known parameters",
        "primary_origins": "tau+1 through tau+4", "secondary_origins": "tau through tau+4",
        "python": platform.python_version(), "numpy": np.__version__,
        "source_tree_at_run": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], text=True).strip(),
        "settings": {},
    }
    for persistence in ("moderate", "zero"):
        config = configuration(persistence)
        data = {c: {m: [] for m in ARMS} for c in CATEGORIES}
        five = {c: {m: [] for m in ARMS} for c in CATEGORIES}
        origins = {c: {m: [] for m in ARMS} for c in CATEGORIES}
        nll = {c: {m: [] for m in ("retained", "frozen")} for c in CATEGORIES}
        brier = {c: {m: [] for m in ("retained", "frozen")} for c in CATEGORIES}
        nll_origins = {c: [] for c in CATEGORIES}
        brier_origins = {c: [] for c in CATEGORIES}
        records = []
        max_event_mean_gap, max_prefix_gap, max_initial_probability_gap = 0., 0., 0.
        max_zero_probability_gap, max_zero_forecast = 0., 0.
        for seed in seeds:
            run = worlds(config, seed, .5)
            paired_results = {}
            for category in CATEGORIES:
                sim = run[category]
                time = sim.truth.events[0].time
                result = known_time_forecasts(sim.observed, config, time, scale=.5)
                paired_results[category] = result
                record: dict[str, object] = {"seed": seed, "category": category}
                selected = dict(result.forecasts)
                selected["oracle"] = selected[f"oracle_{category}"]
                for method in ARMS:
                    squared = np.mean((selected[method] - sim.truth.latent[1:])**2, axis=1)
                    by_origin = squared[time:time+5]
                    primary = float(np.mean(by_origin[1:]))
                    data[category][method].append(primary)
                    five[category][method].append(float(by_origin.mean()))
                    origins[category][method].append(by_origin.tolist())
                    record[f"{method}_mse"] = primary
                    record[f"{method}_five_origin_mse"] = float(by_origin.mean())
                    record[f"{method}_delay0_mse"] = float(by_origin[0])
                true_index = int(category == "state")
                log_scores = -result.log_type_probabilities[time:time+5, true_index]
                probabilities = result.state_probability[time:time+5]
                brier_scores = (probabilities - true_index)**2
                nll[category]["retained"].append(float(log_scores[1:].mean()))
                nll[category]["frozen"].append(float(np.log(2.)))
                brier[category]["retained"].append(float(brier_scores[1:].mean()))
                brier[category]["frozen"].append(.25)
                nll_origins[category].append(log_scores.tolist())
                brier_origins[category].append(brier_scores.tolist())
                record.update({"retained_type_nll": nll[category]["retained"][-1], "frozen_type_nll": float(np.log(2.)),
                               "retained_type_brier": brier[category]["retained"][-1], "frozen_type_brier": .25})
                for delay, probability in enumerate(probabilities):
                    record[f"state_probability_delay{delay}"] = float(probability)
                records.append(record)
                for method in ("projected", "frozen"):
                    max_event_mean_gap = max(max_event_mean_gap, float(np.max(np.abs(selected[method][time] - selected["retained"][time]))))
                max_initial_probability_gap = max(max_initial_probability_gap, abs(float(probabilities[0])-.5))
                if persistence == "zero":
                    max_zero_probability_gap = max(max_zero_probability_gap, float(np.max(np.abs(probabilities-.5))))
                    max_zero_forecast = max(max_zero_forecast, max(float(np.max(np.abs(selected[m]))) for m in ARMS))
            time = run["state"].truth.events[0].time
            for method in ("retained", "projected", "frozen"):
                gap = np.max(np.abs(paired_results["state"].forecasts[method][:time+1] - paired_results["observation"].forecasts[method][:time+1]))
                max_prefix_gap = max(max_prefix_gap, float(gap))
        if max(max_event_mean_gap, max_prefix_gap, max_initial_probability_gap, max_zero_probability_gap, max_zero_forecast) > 1e-12:
            raise AssertionError("Causal or zero-persistence invariant failed")
        balanced = {m: .5*(np.array(data["observation"][m])+np.array(data["state"][m])) for m in ARMS}
        type_balanced = {m: .5*(np.array(nll["observation"][m])+np.array(nll["state"][m])) for m in ("retained", "frozen")}
        comparisons = {
            "forecast_vs_projection": paired_comparison(balanced["retained"], balanced["projected"]),
            "forecast_vs_frozen": paired_comparison(balanced["retained"], balanced["frozen"]),
            "type_logscore_vs_frozen": paired_comparison(type_balanced["retained"], type_balanced["frozen"], relative=False),
            "observation_harm": paired_comparison(np.array(data["observation"]["retained"]), np.array(data["observation"]["projected"])),
            "state_harm": paired_comparison(np.array(data["state"]["retained"]), np.array(data["state"]["projected"])),
        }
        with (output / f"{persistence}.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
        setting = {
            "mse": {c: {m: float(np.mean(v)) for m,v in methods.items()} for c,methods in data.items()},
            "balanced_mse": {m: float(v.mean()) for m,v in balanced.items()},
            "five_origin_mse": {c: {m: float(np.mean(v)) for m,v in methods.items()} for c,methods in five.items()},
            "mse_by_origin": {c: {m: np.mean(v,axis=0).tolist() for m,v in methods.items()} for c,methods in origins.items()},
            "type_nll": {c: {m: float(np.mean(v)) for m,v in methods.items()} for c,methods in nll.items()},
            "type_brier": {c: {m: float(np.mean(v)) for m,v in methods.items()} for c,methods in brier.items()},
            "retained_type_nll_by_origin": {c: np.mean(v,axis=0).tolist() for c,v in nll_origins.items()},
            "retained_type_brier_by_origin": {c: np.mean(v,axis=0).tolist() for c,v in brier_origins.items()},
            "contrasts": comparisons,
            "checks": {"max_event_origin_arm_gap": max_event_mean_gap, "max_matched_prefix_gap": max_prefix_gap,
                       "max_event_origin_probability_gap": max_initial_probability_gap,
                       "max_zero_probability_gap": max_zero_probability_gap, "max_zero_forecast": max_zero_forecast},
        }
        summary["settings"][persistence] = setting
        print(json.dumps({"stage": stage, "persistence": persistence, "contrasts": comparisons, "checks": setting["checks"]}), flush=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=("development", "final"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evaluate(args.stage, args.output or Path(f"results/experiment-v2-{args.stage}"))
