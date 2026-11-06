"""Frozen deterministic single-origin information diagnostic; no fitted model."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

from .information import InformationConfig, integrate

ORDERS = (24, 48, 96, 192)
RISK_FIELDS = (
    "primary_risk", "full_risk", "linear_risk", "quadrature_primary_risk",
    "quadrature_linear_risk", "information_gain", "approximation_gain",
)
RESIDUAL_FIELDS = (
    "primary_risk_identity_residual", "linear_risk_identity_residual",
    "primary_quadrature_residual", "quadrature_weight_residual",
)
PLAN_COMMIT = "41a72bf237848e787d497f7c929e4e69674b7eb3"


def run(output: Path) -> dict:
    """Evaluate every frozen condition/order, refusing to overwrite a directory."""
    output.mkdir(parents=True, exist_ok=False)
    nominal = InformationConfig()
    cases = (
        ("clean", nominal, "clean"),
        ("shared", nominal, "shared"),
        ("duplicate", nominal, "duplicate"),
        ("perfect", replace(nominal, auxiliary_variance=0.0), "clean"),
        ("zero_a", replace(nominal, a=0.0), "clean"),
    )
    root = Path(__file__).resolve().parent.parent
    source_names = (
        "ripplenet/information.py", "ripplenet/information_experiment.py",
        "docs/information-diagnostic-plan.md",
    )
    result = {
        "scope": "new conditional scalar synthetic information diagnostic; no market validation",
        "plan_public_commit": PLAN_COMMIT,
        "source_tree_at_run": subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True,
        ).strip(),
        "source_sha256": {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in source_names},
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "orders": list(ORDERS),
        "tolerances": {"absolute_risk_gap": 1e-6, "relative_percentage_points": .01, "identity": 1e-6},
        "cases": [],
    }
    for name, config, mode in cases:
        rows = []
        for order in ORDERS:
            values = asdict(integrate(config, mode, order))
            values["information_gain_percent"] = 100 * values["information_gain"] / values["primary_risk"]
            values["approximation_gain_percent"] = 100 * values["approximation_gain"] / values["linear_risk"]
            rows.append(values)
        before, final = rows[-2:]
        differences = {key: abs(final[key]-before[key]) for key in RISK_FIELDS}
        relative_differences = {key: abs(final[key]-before[key]) for key in (
            "information_gain_percent", "approximation_gain_percent",
        )}
        residuals = {key: abs(final[key]) for key in RESIDUAL_FIELDS}
        resolved = (
            max(differences.values()) <= 1e-6
            and max(relative_differences.values()) <= .01
            and max(residuals.values()) <= 1e-6
        )
        case = {
            "name": name, "config": asdict(config), "mode": mode, "rows": rows,
            "convergence": {
                "status": "resolved_at_declared_tolerance" if resolved else "numerically_inconclusive",
                "absolute_96_192_differences": differences,
                "percentage_point_96_192_differences": relative_differences,
                "final_absolute_residuals": residuals,
            },
        }
        result["cases"].append(case)
        print(json.dumps({"case": name, "status": case["convergence"]["status"]}), flush=True)
    (output / "summary.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/information-v1"))
    run(parser.parse_args().output)
