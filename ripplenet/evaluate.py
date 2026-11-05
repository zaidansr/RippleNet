"""Evaluate frozen methods once on prespecified final seeds; never tune here."""

from __future__ import annotations

import csv
import argparse
import json
import platform
import subprocess
from pathlib import Path

import numpy as np

from .benchmark import configuration, losses, predictions, worlds
from .mixture import mixture_forecasts
from .statistics import paired_comparison


def evaluate(output: Path = Path("results/experiment-v1")) -> dict[str, object]:
    development = json.loads(Path("results/development-v1.json").read_text(encoding="utf-8"))
    if not development["gate_passed"]:
        raise ValueError("Oracle development gate did not pass")
    if output.exists():
        raise FileExistsError("Refusing to reopen/overwrite a final evaluation directory")
    output.mkdir(parents=True)
    seeds = list(range(30000, 30030))
    summary: dict[str, object] = {
        "stage": "held_out_synthetic_exploratory", "seeds": seeds,
        "python": platform.python_version(), "numpy": np.__version__,
        "source_tree_at_run": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], text=True).strip(),
        "scenarios": {},
    }
    for shift, scale, price_error in (("nominal", .5, False), ("magnitude_shift", .75, False), ("price_error_shift", .5, True)):
        for persistence in ("moderate", "weak", "zero"):
            name = f"{shift}_{persistence}"
            cfg = configuration(persistence)
            setting = development["settings"][persistence]
            baseline = setting["selected_baseline"]
            coefficients = np.array(setting["linear_coefficients"])
            methods = list(dict.fromkeys(["zero", "linear", "kalman", baseline, "dual", "observation_only", "pooled"] + ([] if price_error else ["oracle"])))
            categories = ("observation", "state", "clean")
            data = {m: {c: [] for c in categories} for m in methods}
            whole = {m: {c: [] for c in categories} for m in methods}
            delays = {m: {c: [] for c in categories[:2]} for m in methods}
            max_prefix_gap = 0.
            for seed in seeds:
                run = worlds(cfg, seed, scale, price_error)
                for method in methods:
                    forecasts = {}
                    for category in categories:
                        sim = run[category]
                        if method in ("dual", "observation_only", "pooled"):
                            pred = mixture_forecasts(sim.observed, cfg, method)
                        else:
                            event = sim.truth.events[0] if method == "oracle" and sim.truth.events else None
                            pred = predictions(method, sim.observed, cfg, coefficients, event, scale)
                        forecasts[category] = pred
                        score, overall, by_delay = losses(pred, sim.truth)
                        data[method][category].append(score)
                        whole[method][category].append(overall)
                        if by_delay:
                            delays[method][category].append(by_delay)
                    if method != "oracle":
                        time = run["state"].truth.events[0].time
                        gap = np.max(np.abs(forecasts["state"][:time+1] - forecasts["observation"][:time+1]))
                        max_prefix_gap = max(max_prefix_gap, float(gap))
            if max_prefix_gap > 1e-12:
                raise AssertionError("Ordinary method violated matched-prefix causality")
            with (output / f"{name}.csv").open("w", newline="", encoding="utf-8") as stream:
                writer = csv.writer(stream)
                writer.writerow(["seed", "category"] + methods)
                for i, seed in enumerate(seeds):
                    for category in categories:
                        writer.writerow([seed, category] + [format(data[m][category][i], ".17g") for m in methods])
            contrasts = {}
            for reference in (baseline, "observation_only", "pooled"):
                for category in categories:
                    primary = shift == "nominal" and persistence == "moderate"
                    contrasts[f"dual_vs_{reference}_{category}"] = paired_comparison(
                        np.array(data["dual"][category]), np.array(data[reference][category]), 9 if primary else 1
                    )
            if "oracle" in methods:
                for category in categories[:2]:
                    contrasts[f"oracle_vs_{baseline}_{category}"] = paired_comparison(np.array(data["oracle"][category]), np.array(data[baseline][category]))
            result = {
                "selected_baseline": baseline, "scale": scale, "price_error": price_error,
                "max_ordinary_prefix_forecast_gap": max_prefix_gap,
                "mse": {m: {c: float(np.mean(v)) for c, v in cats.items()} for m, cats in data.items()},
                "whole_path_mse": {m: {c: float(np.mean(v)) for c, v in cats.items()} for m, cats in whole.items()},
                "mse_by_origin_delay": {m: {c: np.mean(v, axis=0).tolist() for c, v in cats.items()} for m, cats in delays.items()},
                "contrasts": contrasts,
            }
            summary["scenarios"][name] = result
            print(f"Finished {name}; baseline={baseline}; prefix gap={max_prefix_gap:.2g}", flush=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/experiment-v1"))
    evaluate(parser.parse_args().output)
