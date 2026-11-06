"""Strict offline Binance spot-trade import; retrieved-file order only.

No download, forecasting model or market-as-of guarantee is supplied. Source
timestamps, source IDs and consecutive replay row ordinals are distinct. Full
file hashes are provenance only and never define origin IDs or input features.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
import zlib
from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterator, Literal, TextIO

from .replay import Outcome, PriceRecord, Replay, Snapshot

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_CSV_BYTES = 20 * 1024 * 1024
_UINT = re.compile(r"[0-9]+\Z")
_DECIMAL = re.compile(r"[0-9]+(?:\.[0-9]+)?\Z")


def _integer(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


@dataclass(frozen=True)
class ArchiveSpec:
    """Caller-declared identity and units, never inferred from future rows."""

    symbol: str
    session_date: date
    timestamp_unit: Literal["ms", "us"]

    def __post_init__(self) -> None:
        if not isinstance(self.symbol, str) or not re.fullmatch(r"[A-Z0-9]{2,30}", self.symbol):
            raise ValueError("symbol must be an uppercase spot product identifier")
        if type(self.session_date) is not date or self.session_date < date(1970, 1, 1):
            raise ValueError("session_date must be a UTC date on or after 1970-01-01")
        required = "us" if self.session_date >= date(2025, 1, 1) else "ms"
        if self.timestamp_unit != required:
            raise ValueError(f"Declared unit disagrees with documented spot archive regime: {required}")

    @property
    def namespace(self) -> str:
        return f"binance.spot.trades:{self.symbol}:{self.session_date.isoformat()}"

    @property
    def day_bounds(self) -> tuple[int, int]:
        factor = 1000 if self.timestamp_unit == "ms" else 1_000_000
        start = (self.session_date - date(1970, 1, 1)).days * 86400 * factor
        return start, start + 86400 * factor


@dataclass(frozen=True)
class ArchiveTrade:
    """One validated raw trade; id_gap_before is diagnostic, not an error label."""

    spec: ArchiveSpec
    row_ordinal: int
    trade_id: int
    event_time: int
    price: Decimal
    quantity: Decimal
    quote_quantity: Decimal
    is_buyer_maker: bool
    is_best_match: bool
    id_gap_before: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.spec, ArchiveSpec):
            raise ValueError("ArchiveTrade requires an ArchiveSpec")
        for name in ("row_ordinal", "trade_id", "event_time", "id_gap_before"):
            _integer(getattr(self, name), name)
        for name in ("price", "quantity", "quote_quantity"):
            value = getattr(self, name)
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ValueError(f"{name} must be a finite nonnegative Decimal")
        if self.price == 0 or self.quantity == 0:
            raise ValueError("price and quantity must be positive")
        if type(self.is_buyer_maker) is not bool or type(self.is_best_match) is not bool:
            raise ValueError("Maker and best-match flags must be booleans")
        start, end = self.spec.day_bounds
        if not start <= self.event_time < end:
            raise ValueError("Timestamp is outside the declared UTC day/unit")

    @property
    def record_id(self) -> str:
        return f"{self.spec.namespace}:{self.trade_id}"


class ArchiveValidationError(ValueError):
    """Validation stopped at this source record; earlier emissions remain valid."""

    def __init__(self, row_ordinal: int, reason: str) -> None:
        self.row_ordinal = row_ordinal
        super().__init__(f"Archive row {row_ordinal}: {reason}")


def _uint(text: str, field: str) -> int:
    if not _UINT.fullmatch(text):
        raise ValueError(f"{field} must contain unsigned integer digits")
    return int(text)


def _decimal(text: str, field: str) -> Decimal:
    if not _DECIMAL.fullmatch(text):
        raise ValueError(f"{field} must use unsigned fixed-point decimal notation")
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid {field}") from exc


def _boolean(text: str) -> bool:
    if text not in ("True", "False", "true", "false"):
        raise ValueError("Boolean fields must be true/false, not numeric flags")
    return text.lower() == "true"


def _order(previous: ArchiveTrade | None, current: ArchiveTrade) -> int:
    if previous is None:
        return 0
    if current.trade_id <= previous.trade_id:
        raise ValueError("Trade IDs must increase; no sorting or deduplication is performed")
    if current.event_time < previous.event_time:
        raise ValueError("Event timestamps decrease; stop rather than reorder the archive")
    return current.trade_id - previous.trade_id - 1


def iter_spot_trades(stream: TextIO, spec: ArchiveSpec) -> Iterator[ArchiveTrade]:
    """Lazily validate exactly seven headerless CSV fields in supplied order.

    The caller owns the stream. Blank/malformed records fail; none are skipped.
    Equal timestamps retain file order. Quote quantity need not equal price times
    base quantity exactly: this importer assumes no universal rounding identity.
    """
    previous: ArchiveTrade | None = None
    ordinal = 0
    reader = csv.reader(stream, strict=True)
    while True:
        try:
            row = next(reader)
        except StopIteration:
            return
        except csv.Error as exc:
            raise ArchiveValidationError(ordinal, "Malformed CSV") from exc
        try:
            if len(row) != 7:
                raise ValueError("Expected exactly seven fields without a header")
            current = ArchiveTrade(
                spec, ordinal, _uint(row[0], "trade_id"), _uint(row[4], "event_time"),
                _decimal(row[1], "price"), _decimal(row[2], "quantity"),
                _decimal(row[3], "quote_quantity"), _boolean(row[5]), _boolean(row[6]),
            )
            gap = _order(previous, current)
            if gap:
                current = replace(current, id_gap_before=gap)
        except ValueError as exc:
            raise ArchiveValidationError(ordinal, str(exc)) from exc
        previous = current
        ordinal += 1
        yield current


@dataclass(frozen=True)
class TradeOrigin:
    """Immediate immutable origin; no whole-file hash or future target is a feature."""

    trade: ArchiveTrade
    snapshot: Snapshot


@dataclass(frozen=True)
class TradeExample:
    origin: TradeOrigin
    target: Outcome
    horizon: int
    correction_status: Literal["unsupported"] = "unsupported"


class TradeReplay:
    """Retain every accepted origin and attach an exact future-row price target."""

    def __init__(self, spec: ArchiveSpec, horizon: int) -> None:
        if not isinstance(spec, ArchiveSpec):
            raise ValueError("spec must be an ArchiveSpec")
        _integer(horizon, "horizon")
        if horizon == 0:
            raise ValueError("horizon must be positive")
        self._spec = spec
        self._horizon = horizon
        self._replay = Replay()
        self._origins: list[TradeOrigin] = []

    @property
    def spec(self) -> ArchiveSpec:
        return self._spec

    @property
    def horizon(self) -> int:
        return self._horizon

    def consume(self, trade: ArchiveTrade) -> TradeOrigin:
        if not isinstance(trade, ArchiveTrade):
            raise ValueError("Expected an ArchiveTrade")
        if trade.spec != self.spec or trade.row_ordinal != len(self._origins):
            raise ValueError("Trade identity or row ordinal does not match this replay")
        previous = self._origins[-1].trade if self._origins else None
        if _order(previous, trade) != trade.id_gap_before:
            raise ValueError("Trade ID gap diagnostic does not match the accepted prefix")
        snapshot = self._replay.consume(PriceRecord(trade.row_ordinal, trade.record_id, trade.price))
        origin = TradeOrigin(trade, snapshot)
        self._origins.append(origin)
        return origin

    def examples(self) -> tuple[TradeExample, ...]:
        """Include pending/censored origins; do not filter on future outcomes."""
        return tuple(
            TradeExample(origin, self._replay.recorded_return(origin.trade.row_ordinal, self.horizon), self.horizon)
            for origin in self._origins
        )

    def seal(self) -> None:
        """Declare normal end of this supplied interval, not end of market history."""
        self._replay.seal()

    def correction_label(self, *args: object, **kwargs: object) -> Outcome:
        raise NotImplementedError("This archive supplies no correction ledger; labels are unsupported")


def _read_local(path: Path) -> tuple[bytes, dict[str, object]]:
    """Bound local input/ZIP expansion without extraction or network access."""
    with path.open("rb") as stream:
        content = stream.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise ValueError("Local file exceeds the fixed 2 MiB input limit")
    metadata: dict[str, object] = {"input_sha256": hashlib.sha256(content).hexdigest()}
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            entries = archive.infolist()
            if len(entries) != 1 or not entries[0].filename.lower().endswith(".csv"):
                raise ValueError("ZIP must contain exactly one CSV member")
            if entries[0].flag_bits & 1:
                raise ValueError("Encrypted archives are unsupported")
            if entries[0].compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                raise ValueError("ZIP compression must be stored or deflated")
            if entries[0].file_size > MAX_CSV_BYTES:
                raise ValueError("CSV exceeds the fixed 20 MiB expansion limit")
            with archive.open(entries[0]) as member:
                payload = member.read(MAX_CSV_BYTES + 1)
            metadata["member"] = entries[0].filename
    else:
        payload = content
    if len(payload) > MAX_CSV_BYTES:
        raise ValueError("Expanded CSV exceeds the fixed size limit")
    metadata["csv_sha256"] = hashlib.sha256(payload).hexdigest()
    return payload, metadata


def main(argv: list[str] | None = None) -> int:
    """Inspect a caller-provided local archive; print coverage, never fit a model."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--date", required=True, type=date.fromisoformat)
    parser.add_argument("--timestamp-unit", required=True, choices=("ms", "us"))
    parser.add_argument("--horizon", required=True, type=int)
    parser.add_argument("--expected-sha256", required=True, help="Expected hash of the input CSV/ZIP")
    args = parser.parse_args(argv)
    report: dict[str, object] = {
        "scope": "retrieved-file-order engineering check, not verified market as-of history",
        "attribution": "Binance Vision; local data-derived findings, no raw trades reproduced",
        "data_terms": "https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md",
        "findings_license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "correction_status": "unsupported",
    }
    replay: TradeReplay | None = None
    try:
        spec = ArchiveSpec(args.symbol, args.date, args.timestamp_unit)
        report.update(namespace=spec.namespace, timestamp_unit=spec.timestamp_unit, horizon=args.horizon)
        if not re.fullmatch(r"[0-9a-fA-F]{64}", args.expected_sha256):
            raise ValueError("Expected SHA256 must contain exactly 64 hexadecimal digits")
        payload, metadata = _read_local(args.path)
        report["provenance"] = metadata
        if metadata["input_sha256"] != args.expected_sha256.lower():
            raise ValueError("Input SHA256 mismatch")
        replay = TradeReplay(spec, args.horizon)
        # Integrity/decompression preflight is separate from lazy row parsing.
        stream = io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8-sig", newline="")
        with stream:
            for trade in iter_spot_trades(stream, spec):
                replay.consume(trade)
        replay.seal()
        report["termination"] = "normal_eof"
    except (ValueError, OSError, UnicodeError, zipfile.BadZipFile, EOFError, zlib.error) as exc:
        report.update(termination="validation_error", error=str(exc))
    if replay is not None:
        examples = replay.examples()
        report["accepted_origins"] = len(examples)
        report["outcome_counts"] = {
            status: sum(example.target.status == status for example in examples)
            for status in ("observed", "pending", "censored", "unavailable")
        }
        report["id_gap_steps"] = sum(example.origin.trade.id_gap_before > 0 for example in examples)
    print(json.dumps(report, indent=2))
    return 0 if report["termination"] == "normal_eof" else 2


if __name__ == "__main__":
    raise SystemExit(main())
