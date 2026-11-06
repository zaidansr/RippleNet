"""Invented CSV fixtures test boundaries; no vendor trade rows are embedded."""

import contextlib
import hashlib
import io
import json
import struct
import tempfile
import unittest
import zipfile
from dataclasses import FrozenInstanceError, replace
from datetime import date
from decimal import Decimal
from math import log
from pathlib import Path
from unittest.mock import patch

from ripplenet.archive_import import (
    ArchiveSpec, ArchiveValidationError, TradeReplay, iter_spot_trades, main,
)


SPEC = ArchiveSpec("TESTUSDT", date(2024, 6, 1), "ms")
START = SPEC.day_bounds[0]


def row(trade_id: int, price: str = "100", time: int = START) -> str:
    return f"{trade_id},{price},2,199.99,{time},True,false\n"


class ArchiveTests(unittest.TestCase):
    def test_order_ids_ties_and_exact_decimal_fields(self) -> None:
        stream = io.StringIO(row(40, "100.00000001") + row(43, "101") + row(44, "99", START + 1))
        records = list(iter_spot_trades(stream, SPEC))
        self.assertEqual([x.row_ordinal for x in records], [0, 1, 2])
        self.assertEqual([x.trade_id for x in records], [40, 43, 44])
        self.assertEqual([x.id_gap_before for x in records], [0, 2, 0])
        self.assertEqual(records[0].price, Decimal("100.00000001"))
        self.assertEqual(records[0].quote_quantity, Decimal("199.99"))
        self.assertTrue(records[0].is_buyer_maker)
        self.assertFalse(records[0].is_best_match)
        self.assertFalse(stream.closed)
        with self.assertRaises(FrozenInstanceError):
            records[0].price = Decimal("1")  # type: ignore[misc]

    def test_malformed_tail_preserves_every_emitted_origin(self) -> None:
        replay = TradeReplay(SPEC, 2)
        source = iter_spot_trades(io.StringIO(row(1) + row(2) + "bad,row\n"), SPEC)
        first = replay.consume(next(source))
        replay.consume(next(source))
        with self.assertRaises(ArchiveValidationError) as failure:
            next(source)
        self.assertEqual(failure.exception.row_ordinal, 2)
        self.assertEqual(len(replay.examples()), 2)
        self.assertEqual([x.target.status for x in replay.examples()], ["pending", "pending"])
        self.assertEqual(first.snapshot.price, Decimal("100"))

    def test_raw_row_horizon_not_source_id_and_tail_censoring(self) -> None:
        replay = TradeReplay(SPEC, 2)
        for trade in iter_spot_trades(io.StringIO(row(10) + row(50, "110") + row(70, "121")), SPEC):
            replay.consume(trade)
        examples = replay.examples()
        self.assertEqual(examples[0].target.available_at, 2)
        self.assertEqual(examples[0].horizon, 2)
        self.assertAlmostEqual(examples[0].target.value, log(1.21))
        replay.seal()
        self.assertEqual([x.target.status for x in replay.examples()], ["observed", "censored", "censored"])
        self.assertTrue(all(x.correction_status == "unsupported" for x in replay.examples()))
        with self.assertRaises(NotImplementedError):
            replay.correction_label("anything", 2)

    def test_future_change_leaves_origin_identity_and_features_equal(self) -> None:
        origins = []
        for tail in (row(3, "1"), row(3, "100000")):
            replay = TradeReplay(SPEC, 1)
            saved = []
            for trade in iter_spot_trades(io.StringIO(row(1) + row(2) + tail), SPEC):
                saved.append(replay.consume(trade))
            origins.append(saved[:2])
        self.assertEqual(origins[0], origins[1])
        self.assertEqual(origins[0][0].snapshot.price_id, SPEC.namespace + ":1")

    def test_explicit_unit_and_integer_day_edges(self) -> None:
        for year, unit in ((2024, "ms"), (2025, "us")):
            spec = ArchiveSpec("TESTUSDT", date(year, 1, 1), unit)
            start, end = spec.day_bounds
            records = list(iter_spot_trades(io.StringIO(row(1, time=start) + row(2, time=end - 1)), spec))
            self.assertEqual(records[-1].event_time, end - 1)
            for bad in (start - 1, end, start // 1000):
                with self.subTest(unit=unit, bad=bad), self.assertRaises(ArchiveValidationError):
                    list(iter_spot_trades(io.StringIO(row(1, time=bad)), spec))
        with self.assertRaises(ValueError):
            ArchiveSpec("TESTUSDT", date(2025, 1, 1), "ms")

    def test_no_silent_sorting_deduplication_or_blank_skips(self) -> None:
        for text in (row(1) + row(1), row(2) + row(1), row(1, time=START + 1) + row(2), row(1) + "\n"):
            source = iter_spot_trades(io.StringIO(text), SPEC)
            next(source)
            with self.assertRaises(ArchiveValidationError):
                next(source)

    def test_numeric_and_schema_failures(self) -> None:
        valid = row(1).rstrip().split(",")
        for index, value in ((0, "1.0"), (0, "True"), (1, "NaN"), (1, "0"), (1, "1e2"),
                             (2, "0"), (3, "-1"), (4, "1.5"), (5, "1"), (6, "yes")):
            bad = valid.copy()
            bad[index] = value
            with self.subTest(index=index, value=value), self.assertRaises(ArchiveValidationError):
                list(iter_spot_trades(io.StringIO(",".join(bad)), SPEC))
        for text in ("trade_id,price,qty,quote_qty,time,maker,best\n", "1,2\n", '"unterminated'):
            with self.assertRaises(ArchiveValidationError):
                list(iter_spot_trades(io.StringIO(text), SPEC))

    def test_replay_rejects_wrong_identity_gap_and_append_after_end(self) -> None:
        record = next(iter_spot_trades(io.StringIO(row(1)), SPEC))
        replay = TradeReplay(SPEC, 1)
        with self.assertRaises(ValueError):
            replay.consume(replace(record, id_gap_before=2))
        with self.assertRaises(ValueError):
            replay.consume(replace(record, spec=replace(SPEC, symbol="OTHERUSDT")))
        self.assertEqual(replay.examples(), ())
        replay.consume(record)
        replay.seal()
        with self.assertRaises(ValueError):
            replay.consume(replace(record, row_ordinal=1, trade_id=2))
        self.assertEqual(len(replay.examples()), 1)
        with self.assertRaises(AttributeError):
            replay.horizon = 20  # type: ignore[misc]

    def test_empty_file_and_repeated_prices(self) -> None:
        self.assertEqual(list(iter_spot_trades(io.StringIO(""), SPEC)), [])
        replay = TradeReplay(SPEC, 1)
        for record in iter_spot_trades(io.StringIO(row(1) + row(2)), SPEC):
            replay.consume(record)
        replay.seal()
        self.assertEqual(replay.examples()[0].target.value, 0.0)
        self.assertEqual(replay.examples()[1].target.status, "censored")

    def run_cli(self, path: Path, expected: str) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main([str(path), "--symbol", SPEC.symbol, "--date", SPEC.session_date.isoformat(),
                           "--timestamp-unit", "ms", "--horizon", "2", "--expected-sha256", expected])
        return status, json.loads(output.getvalue())

    def test_offline_cli_zip_coverage_and_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "fixture.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("fixture.csv", row(1) + row(2) + row(3))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            status, report = self.run_cli(path, digest)
            self.assertEqual(status, 0)
            self.assertEqual(report["accepted_origins"], 3)
            self.assertEqual(report["outcome_counts"], {"observed": 1, "pending": 0, "censored": 2, "unavailable": 0})
            self.assertEqual(report["provenance"]["input_sha256"], digest)
            self.assertEqual(report["correction_status"], "unsupported")
            self.assertEqual(self.run_cli(path, "0" * 64)[0], 2)
            with patch("ripplenet.archive_import.MAX_CSV_BYTES", 1):
                self.assertEqual(self.run_cli(path, digest)[0], 2)

    def test_cli_validation_failure_reports_prefix_without_clean_eof(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "fixture.csv"
            path.write_text(row(1) + row(2) + "bad,row\n", encoding="utf-8")
            status, report = self.run_cli(path, hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(status, 2)
            self.assertEqual(report["termination"], "validation_error")
            self.assertEqual(report["accepted_origins"], 2)
            self.assertEqual(report["outcome_counts"]["pending"], 2)
            self.assertEqual(report["outcome_counts"]["censored"], 0)

    def test_cli_unsupported_zip_compression_is_a_structured_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "fixture.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("fixture.csv", row(1))
            content = bytearray(path.read_bytes())
            struct.pack_into("<H", content, content.index(b"PK\x03\x04") + 8, 99)
            struct.pack_into("<H", content, content.index(b"PK\x01\x02") + 10, 99)
            path.write_bytes(content)
            status, report = self.run_cli(path, hashlib.sha256(content).hexdigest())
            self.assertEqual(status, 2)
            self.assertEqual(report["termination"], "validation_error")
            self.assertIn("compression", report["error"])

    def test_cli_damaged_deflate_stream_is_a_structured_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "fixture.zip"
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("fixture.csv", row(1))
            content = bytearray(path.read_bytes())
            name_size, extra_size = struct.unpack_from("<HH", content, 26)
            content[30 + name_size + extra_size] = 7  # Invalid DEFLATE block type.
            path.write_bytes(content)
            status, report = self.run_cli(path, hashlib.sha256(content).hexdigest())
            self.assertEqual(status, 2)
            self.assertEqual(report["termination"], "validation_error")


if __name__ == "__main__":
    unittest.main()
