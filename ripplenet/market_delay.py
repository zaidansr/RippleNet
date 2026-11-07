"""Fresh recorded-market paired origin-start/delayed-start target control.

Separate development and protected-test execution; no original-as-of guarantee.
Reuses the frozen original fitting routine without changing previous studies.
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta
import hashlib
import io
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

from .archive_import import ArchiveSpec, _read_local, iter_spot_trades
from .market_study import ALPHAS, BASELINES, Day, common_metadata, fit, losses

DATES = tuple((date(2017, 9, 16)+timedelta(days=i)).isoformat() for i in range(30))
TARGETS = ("origin", "delayed")
PLAN = "1cdfb3d0fe3eed36e1892d10c4c7c78ec84be3c6"


def paired_arrays(prices: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p = np.asarray(prices, dtype=float)
    if p.ndim != 1 or not np.isfinite(p).all() or np.any(p <= 0) or len(p) <= 16:
        raise ValueError("Need positive finite prices and at least one matched origin")
    logp = np.log(p)
    r = np.diff(logp)
    k = np.arange(5, len(p)-11)
    x = np.column_stack([r[k-j-1] for j in range(5)])
    origin = logp[k+10]-logp[k]
    delayed = logp[k+11]-logp[k+1]
    for a in (x, origin, delayed):
        a.setflags(write=False)
    return x, origin, delayed


def load_pair(data_dir: Path, day: str) -> dict[str, Day]:
    path = data_dir/f"BTCUSDT-trades-{day}.zip"
    expected, named = Path(str(path)+".CHECKSUM").read_text().strip().split()
    payload, metadata = _read_local(path)
    if named.lstrip("*") != path.name or metadata["input_sha256"] != expected.lower():
        raise ValueError("Publisher archive checksum or identity mismatch")
    with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8-sig", newline="") as stream:
        p = np.array([float(t.price) for t in iter_spot_trades(stream, ArchiveSpec("BTCUSDT", date.fromisoformat(day), "ms"))])
    x, a, b = paired_arrays(p)
    common = {"date": day, "recorded_rows": len(p), "eligible_origins": len(a),
              "feature_unavailable_origins": 5, "archive_sha256": metadata["input_sha256"],
              "csv_sha256": metadata["csv_sha256"]}
    return {name: Day(day, x, target, {**common, "target": name,
            "target_censored_origins": 10+shift, "additional_paired_alignment_exclusions": 1-shift})
            for name, target, shift in (("origin", a, 0), ("delayed", b, 1))}


def provenance() -> dict:
    root = Path(__file__).resolve().parent.parent
    names = ("ripplenet/market_delay.py", "ripplenet/market_study.py",
             "ripplenet/archive_import.py", "docs/market-delay-plan.md")
    return {"source_sha256": {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names},
            "source_tree_at_run": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True).strip(),
            "runtime": {"python": platform.python_version(), "numpy": np.__version__}}


def metadata() -> dict:
    return {**common_metadata(), "plan_public_commit": PLAN,
            "scope": "fresh-period paired retrieved-row target control; not a causal bounce identification",
            "definitions": {"origin": "logP[k+10]-logP[k]", "delayed": "logP[k+11]-logP[k+1]",
                            "inputs": "r[k] through r[k-4]", "common_eligible": "k=5..N-12"}}


def _write(path: Path, content: dict) -> None:
    path.write_text(json.dumps(content, indent=2, allow_nan=False)+"\n", encoding="utf-8", newline="\n")


def development(data_dir: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    training = [load_pair(data_dir, d) for d in DATES[:10]]
    validation = [load_pair(data_dir, d) for d in DATES[10:15]]
    selected = {}
    for target in TARGETS:
        train, val = [p[target] for p in training], [p[target] for p in validation]
        models = [fit(train, alpha) for alpha in ALPHAS]
        scores = [float(np.mean([losses(d, m)["candidate"]["mse"] for d in val])) for m in models]
        model = models[int(np.argmin(scores))]
        refs = {b: float(np.mean([losses(d, model)[b]["mse"] for d in val])) for b in BASELINES}
        selected[target] = {"model": model, "selected_baseline": min(BASELINES, key=refs.get),
                            "validation_candidates": dict(zip(map(str, ALPHAS), scores)), "validation_baselines": refs,
                            "training_coverage": [d.coverage for d in train], "validation_coverage": [d.coverage for d in val]}
    for field in ("mean", "scale"):
        if selected["origin"]["model"][field] != selected["delayed"]["model"][field]:
            raise AssertionError("Paired training features must have identical preprocessing")
    result = {**metadata(), **provenance(), "targets": selected, "test_dates_unopened": list(DATES[15:]), "refit": False}
    _write(output/"selection.json", result)
    return result


def inference(daily_mse: np.ndarray, refs: tuple[int, int]) -> dict:
    """Paired vectors: two selected-reference gains and common-zero absolute contrast."""
    d = np.asarray(daily_mse)
    if d.shape != (15, 2, 4) or not np.isfinite(d).all() or np.any(d < 0):
        raise ValueError("Need 15 paired days, two targets and four nonnegative losses")
    starts = np.random.default_rng(190012).integers(0, 13, size=(9999, 5))
    indices = (starts[:, :, None]+np.arange(3)).reshape(9999, 15)
    samples = d[indices].mean(axis=1)
    def contrasts(a: np.ndarray) -> np.ndarray:
        if np.any(a[..., 0, refs[0]] <= 0) or np.any(a[..., 1, refs[1]] <= 0):
            raise ValueError("Relative gain undefined at zero reference risk")
        return np.stack((1-a[..., 0, 0]/a[..., 0, refs[0]],
                         1-a[..., 1, 0]/a[..., 1, refs[1]],
                         (a[..., 0, 1]-a[..., 0, 0])-(a[..., 1, 1]-a[..., 1, 0])), axis=-1)
    points, draws = contrasts(d.mean(axis=0)), contrasts(samples)
    names = ("origin_gain", "delayed_gain", "absolute_zero_reference_attenuation")
    return {name: {"estimate": float(points[i]), "raw_95": np.quantile(draws[:, i], [.025, .975]).tolist(),
                   "adjusted_family3": np.quantile(draws[:, i], [.05/6, 1-.05/6]).tolist(),
                   "bootstrap_mean": float(draws[:, i].mean()),
                   "centering_shift": float(draws[:, i].mean()-points[i]),
                   "units": "squared_log_return" if i == 2 else "fraction_of_selected_baseline_risk",
                   "n_days": 15, "block_days": 3, "resamples": 9999, "seed": 190012}
            for i, name in enumerate(names)}


def test(data_dir: Path, output: Path) -> dict:
    if (output/"test.json").exists():
        raise FileExistsError("Protected test output already exists")
    selection_path = output/"selection.json"
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    source = provenance()
    if selection["source_sha256"] != source["source_sha256"] or selection["test_dates_unopened"] != list(DATES[15:]):
        raise ValueError("Frozen source or protected dates changed after selection")
    pairs = [load_pair(data_dir, d) for d in DATES[15:]]
    rows = [{"date": DATES[15+i], "targets": {t: {"coverage": p[t].coverage,
             "losses": losses(p[t], selection["targets"][t]["model"])} for t in TARGETS}} for i, p in enumerate(pairs)]
    arms = ("candidate",)+BASELINES
    daily = np.array([[[r["targets"][t]["losses"][a]["mse"] for a in arms] for t in TARGETS] for r in rows])
    refs = tuple(arms.index(selection["targets"][t]["selected_baseline"]) for t in TARGETS)
    summaries = {}
    for t in TARGETS:
        summaries[t] = {"alpha": selection["targets"][t]["model"]["alpha"],
                        "selected_baseline": selection["targets"][t]["selected_baseline"],
                        "equal_day_risk": {a: {m: float(np.mean([r["targets"][t]["losses"][a][m] for r in rows])) for m in ("mse", "mae")} for a in arms},
                        "pooled_origin_risk_secondary": {a: {m: float(np.average([r["targets"][t]["losses"][a][m] for r in rows], weights=[r["targets"][t]["coverage"]["eligible_origins"] for r in rows])) for m in ("mse", "mae")} for a in arms}}
    contrasts = inference(daily, refs)
    result = {**metadata(), **source, "selection_sha256": hashlib.sha256(selection_path.read_bytes()).hexdigest(),
              "daily": rows, "targets": summaries, "primary_contrasts": contrasts,
              "descriptive_gain_difference_fraction": contrasts["origin_gain"]["estimate"]-contrasts["delayed_gain"]["estimate"],
              "caution": "Exploratory paired noncircular blocks underweight endpoints; no causal interpretation or exact coverage"}
    _write(output/"test.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("development", "test"))
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/market-delay-v1"))
    args = parser.parse_args()
    result = development(args.data_dir, args.output) if args.stage == "development" else test(args.data_dir, args.output)
    print(json.dumps({"stage": args.stage, "targets": {t: {"alpha": (result["targets"][t].get("model", {}).get("alpha", result["targets"][t].get("alpha"))), "baseline": result["targets"][t]["selected_baseline"]} for t in TARGETS}}))
