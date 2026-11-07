"""Private-fit/public-method collector-clock trade/midpoint pilot.

No network access. Raw data, learned parameters and predictions are never
written into the repository. Aggregate publication requires source-term review.
"""
from __future__ import annotations

import argparse
from array import array
import csv
from dataclasses import dataclass
from datetime import date
import gzip
import hashlib
import io
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

DATES = tuple(f"{year}-{month:02d}-01" for year, months in ((2025, range(6, 13)), (2026, range(1, 6))) for month in months)
TARGETS = ("trade", "midpoint")
BASELINES = ("zero", "mean", "median", "gap")
ALPHAS = (0., .001, .01, .1, 1., 10., 100.)
PLAN = "6993f9a12311d759b8e5d3370fcac8dc2ade6ed7"
ROOT = Path(__file__).resolve().parent.parent
HEADERS = {
    "trades": ["exchange", "symbol", "timestamp", "local_timestamp", "id", "side", "price", "amount"],
    "quotes": ["exchange", "symbol", "timestamp", "local_timestamp", "ask_amount", "ask_price", "bid_price", "bid_amount"],
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def private_output(path: Path) -> Path:
    path = path.resolve()
    if path.is_relative_to(ROOT):
        raise ValueError("Source terms require model-bearing outputs outside the public repository")
    return path


def write_private(path: Path, value: dict) -> None:
    private_output(path)
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n", encoding="utf-8", newline="\n")


def provenance() -> dict:
    names = ("ripplenet/quote_study.py", "docs/quote-study-plan.md")
    return {"source_sha256": {n: digest(ROOT/n) for n in names},
            "source_tree_at_run": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip(),
            "runtime": {"python": platform.python_version(), "numpy": np.__version__}, "plan_public_commit": PLAN,
            "publication": "Private model-bearing artifact. Public aggregate reports only; no open-data grant.",
            "source": "https://docs.tardis.dev/historical-data-details/kraken",
            "terms": "https://docs.tardis.dev/legal/terms-of-service"}


@dataclass(frozen=True)
class Series:
    times: np.ndarray
    price: np.ndarray
    spread: np.ndarray
    valid: np.ndarray
    diagnostics: dict


class BoundedExpansion(io.RawIOBase):
    """Count/hash expanded bytes before text decoding; enforce the frozen cap."""
    def __init__(self, stream: gzip.GzipFile, cap: int) -> None:
        self.stream, self.cap, self.count = stream, cap, 0
        self.hash = hashlib.sha256()

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: bytearray) -> int:
        data = self.stream.read(min(len(buffer), self.cap-self.count+1))
        self.count += len(data)
        if self.count > self.cap:
            raise ValueError("Expanded byte cap exceeded")
        self.hash.update(data)
        buffer[:len(data)] = data
        return len(data)


def validate_manifest(manifest: dict) -> None:
    expected = {(d, k) for d in DATES for k in ("trades", "quotes")}
    files = manifest["files"]
    if len(files) != 24 or {(f["date"], f["kind"]) for f in files} != expected:
        raise ValueError("Frozen 24-file acquisition set differs")
    for f in files:
        small = f["kind"] == "trades"
        for field, limit in (("compressed_bytes", (32 if small else 128)*1024**2),
                             ("expanded_bytes", (256 if small else 1024)*1024**2)):
            size = f[field]
            if isinstance(size, bool) or not isinstance(size, int) or not 0 < size <= limit:
                raise ValueError("Manifest byte cap failure")
        for field in ("sha256", "csv_sha256"):
            if len(f[field]) != 64 or any(c not in "0123456789abcdef" for c in f[field]):
                raise ValueError("Expected pinned SHA256")
    if sum(f["compressed_bytes"] for f in files) > 1920*1024**2 or sum(f["expanded_bytes"] for f in files) > 15*1024**3:
        raise ValueError("Combined acquisition cap exceeded")


def _number(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        return float("nan")


def read_series(path: Path, kind: str, day: str, expected_sha: str, expected_csv: str | None = None) -> Series:
    if path.stat().st_size > (32 if kind == "trades" else 128)*1024**2:
        raise ValueError("Compressed byte cap exceeded")
    if digest(path) != expected_sha:
        raise ValueError("Acquisition hash mismatch")
    start = (date.fromisoformat(day)-date(1970, 1, 1)).days*86400*1_000_000
    times, prices, spreads, valid = array("q"), array("d"), array("d"), bytearray()
    cap = 2_000_000 if kind == "trades" else 5_000_000
    ties = missing_ids = invalid = 0
    previous = -1
    with gzip.open(path, "rb") as raw:
        expanded = BoundedExpansion(raw, (256 if kind == "trades" else 1024)*1024**2)
        with io.TextIOWrapper(io.BufferedReader(expanded), encoding="utf-8", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader, None)
            if header != HEADERS[kind]:
                raise ValueError("Unexpected exact CSV header")
            for row in reader:
                if len(times) >= cap or len(row) != len(header):
                    raise ValueError("Row cap or CSV width failure")
                r = dict(zip(header, row))
                if r["exchange"] != "kraken" or r["symbol"] != "XBT/USD":
                    raise ValueError("Wrong venue/product identity")
                text = r["local_timestamp"]
                if not text.isascii() or not text.isdecimal():
                    raise ValueError("Invalid collector timestamp")
                now = int(text)
                if now < previous or not start <= now < start+86400*1_000_000:
                    raise ValueError("Collector order/day failure")
                ties += int(now == previous)
                previous = now
                if kind == "trades":
                    price, amount = _number(r["price"]), _number(r["amount"])
                    ok = bool(np.isfinite([price, amount]).all() and price > 0 and amount > 0)
                    spread = float("nan")
                    missing_ids += int(r["id"] == "")
                else:
                    bid, ask, bq, aq = [_number(r[f]) for f in ("bid_price", "ask_price", "bid_amount", "ask_amount")]
                    ok = bool(np.isfinite([bid, ask, bq, aq]).all() and 0 < bid < ask and min(bq, aq) > 0)
                    price = (bid+ask)/2 if ok else float("nan")
                    spread = (ask-bid)/price if ok else float("nan")
                times.append(now)
                prices.append(price if ok else float("nan"))
                spreads.append(spread)
                valid.append(ok)
                invalid += int(not ok)
    if expected_csv is not None and expanded.hash.hexdigest() != expected_csv:
        raise ValueError("Expanded CSV hash mismatch")
    if not times:
        raise ValueError("Empty source session")
    return Series(np.asarray(times, dtype=np.int64), np.asarray(prices), np.asarray(spreads),
                  np.frombuffer(valid, dtype=np.uint8).astype(bool),
                  {"rows": len(times), "invalid_value_states": invalid, "collector_ties": ties, "missing_trade_ids": missing_ids,
                   "compressed_sha256": expected_sha, "expanded_bytes": expanded.count, "csv_sha256": expanded.hash.hexdigest()})


def snapshots(series: Series, grid: np.ndarray, age_limit: int) -> tuple[np.ndarray, np.ndarray]:
    """Strict-before join; invalid latest record cannot be bypassed by an older one."""
    if len(series.times) == 0 or np.any(np.diff(series.times) < 0):
        raise ValueError("Need a nonempty ordered source")
    idx = np.searchsorted(series.times, grid, side="left")-1
    safe = np.maximum(idx, 0)
    ok = (idx >= 0) & series.valid[safe] & ((grid-series.times[safe]) <= age_limit)
    return np.where(ok, series.price[safe], np.nan), np.where(ok, series.spread[safe], np.nan)


def snapshot_counts(series: Series, grid: np.ndarray, age_limit: int, prices: np.ndarray) -> dict:
    idx = np.searchsorted(series.times, grid, side="left")-1
    safe, present = np.maximum(idx, 0), idx >= 0
    prior_valid = series.valid[safe]
    fresh = (grid-series.times[safe]) <= age_limit
    adjacent = np.isfinite(prices[1:]) & np.isfinite(prices[:-1])
    return {"missing_predecessor": int((~present).sum()),
            "invalid_latest_state": int((present & ~prior_valid).sum()),
            "over_age_limit": int((present & prior_valid & ~fresh).sum()),
            "valid_snapshots": int(np.isfinite(prices).sum()),
            "valid_adjacent_pairs": int(adjacent.sum()),
            "unchanged_valid_adjacent_pairs": int((adjacent & (prices[1:] == prices[:-1])).sum())}


@dataclass(frozen=True)
class Session:
    day: str
    x: np.ndarray                 # All feature-eligible issued origins
    y: np.ndarray                 # Future labels may be NaN; never input features
    scorable: np.ndarray          # Retrospective paired scoring only
    coverage: dict


def construct(day: str, trade: np.ndarray, mid: np.ndarray, spread: np.ndarray, horizon: int = 10) -> Session:
    if trade.shape != mid.shape or trade.shape != spread.shape or trade.ndim != 1 or len(trade) < 6 or horizon < 1:
        raise ValueError("Reference/grid shape failure")
    lt, lm = np.log(trade), np.log(mid)
    k = np.arange(5, len(trade))
    features = np.column_stack([lt[k-j]-lt[k-j-1] for j in range(5)] +
                               [lm[k-j]-lm[k-j-1] for j in range(5)] + [spread[k], lt[k]-lm[k]])
    issued = np.isfinite(features).all(axis=1)
    k, x = k[issued], features[issued]
    end = k+horizon
    inside = end < len(trade)
    y = np.full((len(k), 2), np.nan)
    y[inside, 0] = lt[end[inside]]-lt[k[inside]]
    y[inside, 1] = lm[end[inside]]-lm[k[inside]]
    scorable = np.isfinite(y).all(axis=1)
    coverage = {"day": day, "grid_origins": len(trade), "feature_eligible_issued": len(k),
                "feature_unavailable": len(trade)-len(k), "paired_scorable": int(scorable.sum()),
                "session_end_censored": int((~inside).sum()),
                "future_reference_unavailable": int((inside & ~scorable).sum()),
                "observed_targets_on_issued_origins": {t: int(np.isfinite(y[:, i]).sum()) for i, t in enumerate(TARGETS)},
                "unchanged_target_counts_on_paired_subset": {t: int((y[scorable, i] == 0).sum()) for i, t in enumerate(TARGETS)}}
    if not scorable.any():
        raise ValueError("No common scorable origins; fixed design stops")
    for a in (x, y, scorable):
        a.setflags(write=False)
    return Session(day, x, y, scorable, coverage)


def load_session(data_dir: Path, manifest: dict, day: str) -> Session:
    records = {(f["date"], f["kind"]): f for f in manifest["files"]}
    series = {}
    for kind in ("trades", "quotes"):
        f = records[(day, kind)]
        name = f"kraken_{kind}_{day}_XBT-USD.csv.gz"
        series[kind] = read_series(data_dir/name, kind, day, f["sha256"], f["csv_sha256"])
    start = (date.fromisoformat(day)-date(1970, 1, 1)).days*86400*1_000_000
    grid = start+np.arange(86400, dtype=np.int64)*1_000_000
    trade, _ = snapshots(series["trades"], grid, 5_000_000)
    mid, spread = snapshots(series["quotes"], grid, 1_000_000)
    result = construct(day, trade, mid, spread)
    result.coverage["source_diagnostics"] = {k: v.diagnostics for k, v in series.items()}
    result.coverage["snapshot_diagnostics"] = {"trade": snapshot_counts(series["trades"], grid, 5_000_000, trade),
                                              "midpoint": snapshot_counts(series["quotes"], grid, 1_000_000, mid)}
    return result


def fit_grid(sessions: list[Session], target: int) -> list[dict]:
    x = np.concatenate([d.x[d.scorable] for d in sessions])
    y = np.concatenate([d.y[d.scorable, target] for d in sessions])
    w = np.concatenate([np.full(d.scorable.sum(), 1/(len(sessions)*d.scorable.sum())) for d in sessions])
    mean = w @ x
    scale = np.sqrt(w @ ((x-mean)**2))
    scale[scale == 0] = 1
    z, ym = (x-mean)/scale, float(w @ y)
    order = np.argsort(y, kind="stable")
    median = float(y[order[np.searchsorted(np.cumsum(w[order]), .5, side="left")]])
    models = []
    for alpha in ALPHAS:
        if alpha == 0:
            beta = np.linalg.lstsq(z*np.sqrt(w[:, None]), (y-ym)*np.sqrt(w), rcond=None)[0]
        else:
            beta = np.linalg.solve(z.T @ (w[:, None]*z)+alpha*np.eye(x.shape[1]), z.T @ (w*(y-ym)))
        models.append({"alpha": alpha, "feature_mean": mean.tolist(), "feature_scale": scale.tolist(),
                       "target_mean": ym, "target_median": median, "beta": beta.tolist()})
    return models


def score(session: Session, model: dict, target: int) -> dict:
    # Predictions are computed for all issued origins before restricting losses.
    fitted = model["target_mean"]+(session.x-np.asarray(model["feature_mean"]))/np.asarray(model["feature_scale"]) @ np.asarray(model["beta"])
    preds = {"candidate": fitted, "zero": np.zeros(len(fitted)), "mean": np.full(len(fitted), model["target_mean"]),
             "median": np.full(len(fitted), model["target_median"]),
             "gap": -session.x[:, -1] if target == 0 else np.zeros(len(fitted))}
    y, keep = session.y[:, target], session.scorable
    return {name: {"mse": float(np.mean((p[keep]-y[keep])**2)), "mae": float(np.mean(abs(p[keep]-y[keep])))} for name, p in preds.items()}


def development(data_dir: Path, manifest_path: Path, output: Path) -> str:
    output = private_output(output)
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    training = [load_session(data_dir, manifest, d) for d in DATES[:6]]
    validation = [load_session(data_dir, manifest, d) for d in DATES[6:9]]
    selected = {}
    for i, target in enumerate(TARGETS):
        models = fit_grid(training, i)
        scores = [float(np.mean([score(d, m, i)["candidate"]["mse"] for d in validation])) for m in models]
        model = models[int(np.argmin(scores))]
        refs = {b: float(np.mean([score(d, model, i)[b]["mse"] for d in validation])) for b in BASELINES}
        selected[target] = {"model": model, "baseline": min(BASELINES, key=refs.get), "validation_grid_mse": scores, "validation_baselines": refs}
    for key in ("feature_mean", "feature_scale"):
        if selected["trade"]["model"][key] != selected["midpoint"]["model"][key]:
            raise AssertionError("Paired training scalers differ")
    result = {**provenance(), "targets": selected, "manifest_sha256": digest(manifest_path), "test_dates_unopened": list(DATES[9:]),
              "training_coverage": [d.coverage for d in training], "validation_coverage": [d.coverage for d in validation], "refit": False}
    path = output/"selection.json"
    write_private(path, result)
    return digest(path)


def test(data_dir: Path, manifest_path: Path, output: Path, expected_selection: str) -> dict:
    output = private_output(output)
    if (output/"test.json").exists():
        raise FileExistsError("Refusing to overwrite protected results")
    path = output/"selection.json"
    if digest(path) != expected_selection:
        raise ValueError("Private selection differs from its public commitment")
    selected = json.loads(path.read_text(encoding="utf-8"))
    current = provenance()
    if selected["source_sha256"] != current["source_sha256"] or selected["manifest_sha256"] != digest(manifest_path) or selected["test_dates_unopened"] != list(DATES[9:]):
        raise ValueError("Frozen source, data manifest or test dates changed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    sessions = [load_session(data_dir, manifest, d) for d in DATES[9:]]
    daily = [{"day": d.day, "coverage": d.coverage,
              "losses": {t: score(d, selected["targets"][t]["model"], i) for i, t in enumerate(TARGETS)}} for d in sessions]
    summaries = {}
    absolute = {}
    for t in TARGETS:
        ref = selected["targets"][t]["baseline"]
        risk = {a: {m: float(np.mean([d["losses"][t][a][m] for d in daily])) for m in ("mse", "mae")} for a in ("candidate",)+BASELINES}
        pooled = {a: {m: float(np.average([d["losses"][t][a][m] for d in daily], weights=[d["coverage"]["paired_scorable"] for d in daily])) for m in ("mse", "mae")} for a in ("candidate",)+BASELINES}
        if risk[ref]["mse"] <= 0:
            raise ValueError("Relative gain undefined at zero reference risk")
        summaries[t] = {"selected_baseline": ref, "equal_session_risk": risk, "pooled_origin_risk_secondary": pooled,
                        "gain_fraction": 1-risk["candidate"]["mse"]/risk[ref]["mse"]}
        absolute[t] = risk["zero"]["mse"]-risk["candidate"]["mse"]
    result = {**current, "selection_sha256": expected_selection, "manifest_sha256": selected["manifest_sha256"],
              "daily": daily, "targets": summaries, "absolute_zero_relative_improvement_trade_minus_midpoint": absolute["trade"]-absolute["midpoint"],
              "uncertainty": "Descriptive only: three monthly test sessions; no CI, p-value or significance claim"}
    write_private(output/"test.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("development", "test"))
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-selection-sha256")
    args = parser.parse_args()
    if args.stage == "development":
        print(json.dumps({"stage": "development", "private_selection_sha256": development(args.data_dir, args.manifest, args.output)}))
    else:
        if not args.expected_selection_sha256:
            parser.error("Test requires the previously published selection hash")
        r = test(args.data_dir, args.manifest, args.output, args.expected_selection_sha256)
        print(json.dumps({"stage": "test", "sessions": len(r["daily"]), "private_result_sha256": digest(args.output/"test.json")}))
