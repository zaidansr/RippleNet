"""Frozen real retrieved-archive forecast pilot; never an original-as-of claim.

Development and test are separate commands. Only training fits preprocessing;
validation selects frozen settings. Test checks source/selection provenance and
does not refit. Raw data stays in a caller-supplied private local directory.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, timedelta
import hashlib
import io
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

from .archive_import import ArchiveSpec, _read_local, iter_spot_trades

DATES = tuple((date(2017, 8, 17)+timedelta(days=i)).isoformat() for i in range(30))
ALPHAS = (0., .001, .01, .1, 1., 10., 100.)
BASELINES = ("zero", "constant", "lagmean")
PLAN_COMMIT = "ad52381d89716c20076d07333f8656c97fa415cd"
LICENSE = "https://creativecommons.org/licenses/by-nc-sa/4.0/"


@dataclass(frozen=True)
class Day:
    date: str
    x: np.ndarray
    y: np.ndarray
    coverage: dict


def arrays(prices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Origin k uses prices k-5..k; target uses k and k+10 within this day."""
    prices = np.asarray(prices, dtype=float)
    if prices.ndim != 1 or not np.isfinite(prices).all() or np.any(prices <= 0):
        raise ValueError("Expected finite positive one-dimensional prices")
    if len(prices) <= 15:
        raise ValueError("Day has no common eligible origins; fixed design stops")
    logs = np.log(prices)
    adjacent = np.diff(logs)
    origins = np.arange(5, len(prices)-10)
    x = np.column_stack([adjacent[origins-j-1] for j in range(5)])
    y = logs[origins+10]-logs[origins]
    x.setflags(write=False)
    y.setflags(write=False)
    return x, y


def load_day(data_dir: Path, day: str) -> Day:
    path = data_dir / f"BTCUSDT-trades-{day}.zip"
    expected, named = Path(str(path)+".CHECKSUM").read_text().strip().split()
    if named.lstrip("*") != path.name or len(expected) != 64:
        raise ValueError("Publisher checksum does not name this exact archive")
    payload, metadata = _read_local(path)
    if metadata["input_sha256"] != expected.lower():
        raise ValueError("Archive checksum mismatch")
    spec = ArchiveSpec("BTCUSDT", date.fromisoformat(day), "ms")
    with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8-sig", newline="") as stream:
        prices = np.array([float(t.price) for t in iter_spot_trades(stream, spec)])
    x, y = arrays(prices)
    return Day(day, x, y, {
        "date": day, "recorded_rows": len(prices), "eligible_origins": len(y),
        "feature_unavailable_origins": 5, "target_censored_origins": 10,
        "observed_targets_before_feature_restriction": len(prices)-10,
        "archive_sha256": metadata["input_sha256"], "csv_sha256": metadata["csv_sha256"],
    })


def fit(days: list[Day], alpha: float) -> dict:
    """Equal total weight per training day, unpenalised intercept, weighted scale."""
    if not days or alpha not in ALPHAS:
        raise ValueError("Expected training days and a frozen alpha")
    x = np.concatenate([d.x for d in days])
    y = np.concatenate([d.y for d in days])
    weights = np.concatenate([np.full(len(d.y), 1/(len(days)*len(d.y))) for d in days])
    mean = weights @ x
    scale = np.sqrt(weights @ ((x-mean)**2))
    scale = np.where(scale == 0, 1., scale)
    target_mean = float(weights @ y)
    z = (x-mean)/scale
    if alpha == 0:
        beta = np.linalg.lstsq(z*np.sqrt(weights[:, None]), (y-target_mean)*np.sqrt(weights), rcond=None)[0]
    else:
        beta = np.linalg.solve(z.T @ (z*weights[:, None])+alpha*np.eye(5), z.T @ (weights*(y-target_mean)))
    return {"alpha": alpha, "mean": mean.tolist(), "scale": scale.tolist(),
            "target_mean": target_mean, "beta": beta.tolist()}


def predict(day: Day, model: dict) -> np.ndarray:
    return model["target_mean"]+(day.x-np.asarray(model["mean"]))/np.asarray(model["scale"]) @ np.asarray(model["beta"])


def predictions(day: Day, model: dict) -> dict[str, np.ndarray]:
    return {"candidate": predict(day, model), "zero": np.zeros(len(day.y)),
            "constant": np.full(len(day.y), model["target_mean"]), "lagmean": 10*day.x.mean(axis=1)}


def losses(day: Day, model: dict) -> dict:
    return {name: {"mse": float(np.mean((p-day.y)**2)), "mae": float(np.mean(abs(p-day.y)))}
            for name, p in predictions(day, model).items()}


def provenance() -> dict:
    root = Path(__file__).resolve().parent.parent
    names = ("ripplenet/market_study.py", "ripplenet/archive_import.py", "docs/market-study-plan.md")
    return {"source_sha256": {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names},
            "source_tree_at_run": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True).strip(),
            "runtime": {"python": platform.python_version(), "numpy": np.__version__}}


def common_metadata() -> dict:
    return {"scope": "retrieved early-period BTCUSDT trade-price forecasting; not verified original as-of history",
            "plan_public_commit": PLAN_COMMIT, "attribution": "Binance Vision; derived research findings, no raw trades",
            "findings_license": LICENSE,
            "source": "https://data.binance.vision/",
            "changes": "Computed features, forecasts, coverage, losses and uncertainty from recorded trades",
            "data_terms": "https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md"}


def development(data_dir: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    training = [load_day(data_dir, d) for d in DATES[:10]]
    validation = [load_day(data_dir, d) for d in DATES[10:15]]
    models = [fit(training, alpha) for alpha in ALPHAS]
    validation_rows = [{"alpha": m["alpha"], "equal_day_mse": float(np.mean([losses(d, m)["candidate"]["mse"] for d in validation]))} for m in models]
    chosen = int(np.argmin([r["equal_day_mse"] for r in validation_rows]))
    model = models[chosen]
    baseline_scores = {b: float(np.mean([losses(d, model)[b]["mse"] for d in validation])) for b in BASELINES}
    baseline = min(BASELINES, key=baseline_scores.get)
    result = {**common_metadata(), **provenance(), "model": model, "selected_baseline": baseline,
              "training_coverage": [d.coverage for d in training], "validation_coverage": [d.coverage for d in validation],
              "validation_candidates": validation_rows, "validation_baselines": baseline_scores,
              "test_dates_unopened": list(DATES[15:]), "refit_on_validation": False}
    (output/"selection.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8", newline="\n")
    return result


def bootstrap(day_losses: np.ndarray, baseline_column: int) -> dict:
    """Frozen paired, noncircular three-day moving blocks; approximate only."""
    if day_losses.shape != (15, 4) or np.any(day_losses < 0) or not np.isfinite(day_losses).all():
        raise ValueError("Expected 15 days by candidate/zero/constant/lagmean MSE")
    starts = np.random.default_rng(190011).integers(0, 13, size=(9999, 5))
    indices = (starts[:, :, None]+np.arange(3)).reshape(9999, 15)
    sampled = day_losses[indices].mean(axis=1)
    if np.any(sampled[:, baseline_column] <= 0) or day_losses[:, baseline_column].mean() <= 0:
        raise ValueError("Relative reduction undefined for zero baseline risk")
    gain = 1-sampled[:, 0]/sampled[:, baseline_column]
    difference = sampled[:, baseline_column]-sampled[:, 0]
    return {"gain_fraction": float(1-day_losses[:, 0].mean()/day_losses[:, baseline_column].mean()),
            "absolute_mse_reduction": float(day_losses[:, baseline_column].mean()-day_losses[:, 0].mean()),
            "raw_95_gain": np.quantile(gain, [.025, .975]).tolist(),
            "adjusted_97_5_gain": np.quantile(gain, [.0125, .9875]).tolist(),
            "raw_95_absolute": np.quantile(difference, [.025, .975]).tolist(),
            "adjusted_97_5_absolute": np.quantile(difference, [.0125, .9875]).tolist(),
            "bootstrap_mean_gain": float(gain.mean()),
            "bootstrap_centering_shift": float(gain.mean()-(1-day_losses[:, 0].mean()/day_losses[:, baseline_column].mean())),
            "n_days": 15, "block_days": 3, "resamples": 9999, "seed": 190011,
            "caution": "Approximate exploratory intervals; few blocks; noncircular endpoints are underweighted"}


def test(data_dir: Path, output: Path) -> dict:
    path = output/"test.json"
    if path.exists():
        raise FileExistsError("Refusing to overwrite protected test output")
    selection_path = output/"selection.json"
    selected = json.loads(selection_path.read_text())
    current = provenance()
    if selected["source_sha256"] != current["source_sha256"]:
        raise ValueError("Source changed after development selection")
    if selected["test_dates_unopened"] != list(DATES[15:]):
        raise ValueError("Protected test dates differ from frozen plan")
    model = selected["model"]
    days = [load_day(data_dir, d) for d in DATES[15:]]
    rows = [{"date": d.date, "coverage": d.coverage, "losses": losses(d, model)} for d in days]
    arms = ("candidate",)+BASELINES
    daily = np.array([[r["losses"][arm]["mse"] for arm in arms] for r in rows])
    summary = {arm: {metric: float(np.mean([r["losses"][arm][metric] for r in rows])) for metric in ("mse", "mae")} for arm in arms}
    pooled = {arm: {metric: float(np.average([r["losses"][arm][metric] for r in rows], weights=[len(d.y) for d in days])) for metric in ("mse", "mae")} for arm in arms}
    baseline = selected["selected_baseline"]
    result = {**common_metadata(), **current, "selection_sha256": hashlib.sha256(selection_path.read_bytes()).hexdigest(),
              "model_alpha": model["alpha"], "selected_baseline": baseline,
              "daily": rows, "equal_day_risk": summary, "pooled_origin_risk_secondary": pooled,
              "primary_contrasts": {"versus_zero": bootstrap(daily, 1), "versus_selected_baseline": bootstrap(daily, arms.index(baseline))},
              "distinct_primary_comparisons": 1 if baseline == "zero" else 2,
              "meaningful_market_margin": None, "no_correction_or_shock_supervision": True}
    path.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("development", "test"))
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/market-v1"))
    args = parser.parse_args()
    result = development(args.data_dir, args.output) if args.stage == "development" else test(args.data_dir, args.output)
    print(json.dumps({"stage": args.stage, "alpha": result.get("model_alpha", result.get("model", {}).get("alpha")),
                      "selected_baseline": result["selected_baseline"]}))
