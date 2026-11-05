"""Run causal-timing checks; this is not a model-performance experiment."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
import subprocess

import numpy as np

from .filtering import causal_forecasts
from .simulation import Config, paired_worlds


def run() -> dict[str, object]:
    seed, event_time = 20261105, 40
    a = np.array([[0.55, 0.10, 0.0], [0.0, 0.45, 0.1], [0.05, 0.0, 0.35]])
    q, r = np.eye(3) * 0.01, np.eye(3) * 0.0025
    amplitude = np.array([0.5, 0., 0.])
    scenarios: dict[str, object] = {}
    for name, transition in (("moderate_persistence", a), ("zero_persistence", np.zeros((3, 3)))):
        cfg = Config(transition, q, r, n_steps=120)
        obs, state = paired_worlds(cfg, seed, event_time, amplitude)
        obs_predictions = causal_forecasts(obs.observed, cfg)
        state_predictions = causal_forecasts(state.observed, cfg)
        prefix_error = float(np.max(np.abs(obs.observed.values[:event_time+1] - state.observed.values[:event_time+1])))
        forecast_error = float(np.max(np.abs(obs_predictions[:event_time+1] - state_predictions[:event_time+1])))
        effect, propagation_error = amplitude.copy(), 0.0
        for time in range(event_time, cfg.n_steps):
            delta = state.truth.latent[time] - obs.truth.latent[time]
            propagation_error = max(propagation_error, float(np.max(np.abs(delta - effect))))
            effect = transition @ effect
        if max(prefix_error, forecast_error, propagation_error) > 1e-12:
            raise AssertionError("Paired-world invariant failed")
        scenarios[name] = {
            "transition": transition.tolist(),
            "max_observed_prefix_difference": prefix_error,
            "max_causal_forecast_prefix_difference": forecast_error,
            "max_state_propagation_identity_error": propagation_error,
            "forecast_difference_norms_by_origin_delay": np.linalg.norm(
                state_predictions[event_time:event_time+5] - obs_predictions[event_time:event_time+5], axis=1
            ).tolist(),
        }
    try:
        revision = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=Path(__file__).resolve().parent.parent, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        revision = "unavailable"
    return {
        "status": "diagnostic_only_not_performance_evidence", "seed": seed,
        "event_time": event_time, "n_steps": 120, "burn_in": 128,
        "score_window": 5, "amplitude": amplitude.tolist(),
        "process_cov": q.tolist(), "observation_cov": r.tolist(),
        "python": platform.python_version(), "numpy": np.__version__,
        "source_tree_at_run": revision, "scenarios": scenarios,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
