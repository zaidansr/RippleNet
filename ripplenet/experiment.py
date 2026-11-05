"""Run the prespecified development stage. Final evaluation is a separate command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .benchmark import configuration, fit_linear, losses, predictions, worlds

METHODS = ("zero", "linear", "kalman", "clipped_2", "clipped_3", "clipped_5", "adaptive", "oracle")


def development() -> dict[str, object]:
    settings: dict[str, object] = {}
    for persistence in ("moderate", "weak", "zero"):
        config = configuration(persistence)
        coefficients = fit_linear(config)
        rows: dict[str, dict[str, list[float]]] = {m: {c: [] for c in ("observation", "state")} for m in METHODS}
        for seed in range(20000, 20012):
            run = worlds(config, seed, .5)
            for category in ("observation", "state"):
                sim = run[category]
                for method in METHODS:
                    event = sim.truth.events[0] if method == "oracle" else None
                    pred = predictions(method, sim.observed, config, coefficients, event)
                    rows[method][category].append(losses(pred, sim.truth)[0])
        ordinary = [m for m in METHODS if m != "oracle"]
        best = min(ordinary, key=lambda m: np.mean(rows[m]["observation"] + rows[m]["state"]))
        means = {m: {c: float(np.mean(values)) for c, values in cats.items()} for m, cats in rows.items()}
        headroom = {c: 1 - means["oracle"][c] / means[best][c] for c in ("observation", "state")}
        settings[persistence] = {"selected_baseline": best, "means": means, "oracle_relative_improvement": headroom, "seed_losses": rows, "linear_coefficients": coefficients.tolist()}
    moderate = settings["moderate"]
    gate = max(moderate["oracle_relative_improvement"].values()) >= .10
    return {"stage": "development_only", "test_data_opened": False, "development_seeds": list(range(20000, 20012)), "event_scale": .5, "gate_passed": bool(gate), "settings": settings}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/development-v1.json"))
    args = parser.parse_args()
    result = development()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"gate_passed": result["gate_passed"], "test_data_opened": False,
                      "moderate": {k: v for k, v in result["settings"]["moderate"].items() if k not in ("seed_losses", "linear_coefficients")}}, indent=2))


if __name__ == "__main__":
    main()
