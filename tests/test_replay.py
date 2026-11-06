"""Causal invariants on invented prices/notices, without any vendor records."""

import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal, localcontext
from math import log

from ripplenet.replay import (
    CorrectionNotice, Outcome, PriceRecord, Replay, training_eligible,
)


def price(ordinal: int, value: str = "100") -> PriceRecord:
    return PriceRecord(ordinal, f"p{ordinal}", Decimal(value))


class ReplayTests(unittest.TestCase):
    def test_late_notice_never_rewrites_prior_snapshot_or_reference(self) -> None:
        replay = Replay()
        original = replay.consume(price(0, "100"))
        second = replay.consume(price(1, "110"))
        noticed = replay.consume(CorrectionNotice(2, "n2", "p0"))
        self.assertEqual(original.price, Decimal("100"))
        self.assertEqual(original.correction_notices, 0)
        self.assertEqual(second.correction_notices, 0)
        self.assertEqual(noticed.price, Decimal("110"))
        self.assertEqual(noticed.correction_notices, 1)
        with self.assertRaises(FrozenInstanceError):
            original.price = Decimal("999")  # type: ignore[misc]

    def test_future_tail_changes_do_not_change_prefix_features(self) -> None:
        first, second = Replay(), Replay()
        prefix = [price(0), price(1, "101")]
        a = [first.consume(record) for record in prefix]
        b = [second.consume(record) for record in prefix]
        first.consume(price(2, "1"))
        second.consume(CorrectionNotice(2, "notice", "p0"))
        second.consume(price(3, "1000000"))
        self.assertEqual(a, b)
        self.assertEqual(a[1].correction_notices, 0)

    def test_numeric_return_and_exact_endpoint(self) -> None:
        replay = Replay()
        replay.consume(price(0, "100"))
        self.assertEqual(replay.recorded_return(0, 2).status, "pending")
        replay.consume(price(1, "110"))
        self.assertEqual(replay.recorded_return(0, 2).status, "pending")
        replay.consume(CorrectionNotice(2, "n2", "p0"))
        outcome = replay.recorded_return(0, 2)
        self.assertEqual(outcome.available_at, 2)
        self.assertAlmostEqual(outcome.value, log(1.1))
        replay.consume(price(3, "10000"))
        self.assertEqual(replay.recorded_return(0, 2), outcome)

    def test_positive_and_negative_labels_wait_for_same_maturity(self) -> None:
        replay = Replay()
        replay.consume(price(0))
        replay.consume(price(1))
        replay.consume(CorrectionNotice(2, "n2", "p0"))
        self.assertEqual(replay.correction_label("p0", 3).status, "pending")
        replay.consume(price(3))
        self.assertEqual(replay.correction_label("p0", 3), Outcome("observed", 1, 3))
        self.assertEqual(replay.correction_label("p1", 3).status, "pending")
        replay.consume(price(4))
        self.assertEqual(replay.correction_label("p1", 3), Outcome("observed", 0, 4))

    def test_notice_at_deadline_counts_later_notice_does_not(self) -> None:
        replay = Replay()
        replay.consume(price(0))
        replay.consume(price(1))
        replay.consume(CorrectionNotice(2, "n2", "p0"))
        self.assertEqual(replay.correction_label("p0", 2), Outcome("observed", 1, 2))
        self.assertEqual(replay.correction_label("p1", 1), Outcome("observed", 0, 2))
        replay.consume(CorrectionNotice(3, "n3", "p1"))
        self.assertEqual(replay.correction_label("p1", 1), Outcome("observed", 0, 2))

    def test_end_of_interval_retains_censored_outcomes_including_early_positive(self) -> None:
        replay = Replay()
        replay.consume(price(0))
        replay.consume(CorrectionNotice(1, "n1", "p0"))
        replay.seal()
        self.assertEqual(replay.correction_label("p0", 2), Outcome("censored"))
        self.assertEqual(replay.recorded_return(0, 2), Outcome("censored"))
        self.assertEqual(replay.recorded_return(0, 1), Outcome("observed", 0.0, 1))
        with self.assertRaisesRegex(ValueError, "sealed"):
            replay.consume(price(2))

    def test_fit_cutoff_requires_both_outcomes_not_just_origin(self) -> None:
        replay = Replay()
        for ordinal in range(4):
            replay.consume(price(ordinal))
        target = replay.recorded_return(0, 1)
        label = replay.correction_label("p0", 3)
        self.assertFalse(training_eligible(target, label, 2))
        self.assertTrue(training_eligible(target, label, 3))
        self.assertFalse(training_eligible(target, Outcome("censored"), 100))

    def test_rejections_leave_existing_prefix_usable(self) -> None:
        replay = Replay()
        before = replay.consume(price(0))
        for bad in (
            price(2), PriceRecord(1, "p0", Decimal("90")),
            CorrectionNotice(1, "n1", "unknown"),
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                replay.consume(bad)
            self.assertEqual(replay.snapshot, before)
        replay.consume(price(1))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            replay.consume(CorrectionNotice(2, "p0", "p1"))
        self.assertEqual(replay.snapshot.ordinal, 1)

    def test_invalid_record_values_and_queries(self) -> None:
        for value in (Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 100.0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                PriceRecord(0, "record", value)  # type: ignore[arg-type]
        for ordinal in (True, -1, 0.5):
            with self.subTest(ordinal=ordinal), self.assertRaises(ValueError):
                PriceRecord(ordinal, "record", Decimal("100"))  # type: ignore[arg-type]
        replay = Replay()
        replay.consume(price(0))
        for horizon in (0, -1, True):
            with self.subTest(horizon=horizon), self.assertRaises(ValueError):
                replay.recorded_return(0, horizon)
        with self.assertRaises(ValueError):
            replay.recorded_return(1, 1)
        with self.assertRaises(ValueError):
            replay.correction_label("unknown", 1)

    def test_deterministic_numeric_context(self) -> None:
        with localcontext() as context:
            context.prec = 3
            replay = Replay()
            replay.consume(price(0, "100"))
            replay.consume(price(1, "100.01"))
            self.assertAlmostEqual(replay.snapshot.last_recorded_return, log(1.0001), places=14)

    def test_outcome_cannot_expose_values_before_observation(self) -> None:
        for status in ("pending", "censored", "unavailable"):
            with self.subTest(status=status), self.assertRaises(ValueError):
                Outcome(status, 1, 5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            Outcome("observed", float("nan"), 2)


if __name__ == "__main__":
    unittest.main()
