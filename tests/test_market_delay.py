"""Invented paired-label fixtures; no real records or target-driven settings."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import market_delay as m
from ripplenet.market_study import Day


def pair(day: str) -> dict:
    x, a, b = m.paired_arrays(np.exp(.003*np.sin(np.arange(60))+.001*np.arange(60)))
    return {t: Day(day, x, y, {"date": day, "eligible_origins": len(y)})
            for t, y in zip(m.TARGETS, (a, b))}


class DelayTests(unittest.TestCase):
    def test_paired_indexing_same_mask_and_distinct_future_labels(self) -> None:
        logs = .0001*np.arange(40)**2
        x, a, b = m.paired_arrays(np.exp(logs))
        self.assertEqual(x.shape, (24, 5))
        self.assertEqual(len(a), len(b))
        assert_allclose(x[0], np.diff(logs)[[4, 3, 2, 1, 0]], atol=1e-15)
        self.assertAlmostEqual(a[0], logs[15]-logs[5])
        self.assertAlmostEqual(b[0], logs[16]-logs[6])
        self.assertAlmostEqual(a[-1], logs[38]-logs[28])
        self.assertAlmostEqual(b[-1], logs[39]-logs[29])
        for v in (x, a, b):
            self.assertFalse(v.flags.writeable)

    def test_future_start_never_enters_origin_features(self) -> None:
        p = np.exp(.01*np.arange(40))
        modified = p.copy()
        modified[6] *= 2
        x, a, b = m.paired_arrays(p)
        changed, ca, cb = m.paired_arrays(modified)
        assert_array_equal(x[0], changed[0])  # first origin k=5; P6 is future
        self.assertEqual(a[0], ca[0])
        self.assertNotEqual(b[0], cb[0])

    def test_invalid_or_short_day_fails_without_replacement(self) -> None:
        for p in (np.ones(16), np.zeros(40), np.full(40, np.nan)):
            with self.assertRaises(ValueError):
                m.paired_arrays(p)

    def test_development_only_first_fifteen_dates_same_scalers(self) -> None:
        opened = []
        def load(_directory: Path, name: str) -> dict:
            self.assertIn(name, m.DATES[:15])
            opened.append(name)
            return pair(name)
        with tempfile.TemporaryDirectory() as temp, patch.object(m, "load_pair", load):
            out = Path(temp)/"new"
            s = m.development(Path(temp), out)
            self.assertEqual(opened, list(m.DATES[:15]))
            self.assertEqual(s["targets"]["origin"]["model"]["mean"], s["targets"]["delayed"]["model"]["mean"])
            self.assertEqual(s["targets"]["origin"]["model"]["scale"], s["targets"]["delayed"]["model"]["scale"])
            self.assertFalse(s["refit"])
            self.assertEqual(s["test_dates_unopened"], list(m.DATES[15:]))
            self.assertEqual(s["plan_public_commit"], m.PLAN)

    def test_test_stage_no_refit_protected_dates_and_source_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp, patch.object(m, "load_pair", lambda p, d: pair(d)):
            out = Path(temp)/"new"
            m.development(Path(temp), out)
            with patch.object(m, "fit", side_effect=AssertionError("Test cannot fit")):
                t = m.test(Path(temp), out)
            self.assertEqual([r["date"] for r in t["daily"]], list(m.DATES[15:]))
            self.assertEqual(len(t["primary_contrasts"]), 3)
            with self.assertRaises(FileExistsError):
                m.test(Path(temp), out)
            (out/"test.json").unlink()
            s = json.loads((out/"selection.json").read_text(encoding="utf-8"))
            s["source_sha256"] = {}
            (out/"selection.json").write_text(json.dumps(s))
            with patch.object(m, "load_pair", side_effect=AssertionError("Must reject before test read")):
                with self.assertRaises(ValueError):
                    m.test(Path(temp), out)

    def test_primary_absolute_contrast_uses_common_zero_not_selected_reference(self) -> None:
        a = np.zeros((15, 2, 4))
        for i in range(15):
            v = i+1
            a[i, 0] = [.8*v, v, 2*v, 3*v]
            a[i, 1] = [.5*v, v, 2*v, 3*v]
        r = m.inference(a, (2, 3))
        self.assertAlmostEqual(r["origin_gain"]["estimate"], .6)
        self.assertAlmostEqual(r["delayed_gain"]["estimate"], 1-.5/3)
        self.assertAlmostEqual(r["absolute_zero_reference_attenuation"]["estimate"], -.3*8)
        self.assertEqual(r, m.inference(a, (2, 3)))
        self.assertEqual(r["absolute_zero_reference_attenuation"]["units"], "squared_log_return")

    def test_identical_targets_have_exact_zero_paired_attenuation(self) -> None:
        values = np.arange(1, 16, dtype=float)
        d = np.empty((15, 2, 4))
        d[:, 0] = np.column_stack((.9*values, values, 2*values, 3*values))
        d[:, 1] = d[:, 0]
        c = m.inference(d, (1, 1))
        self.assertEqual(c["absolute_zero_reference_attenuation"]["estimate"], 0)
        assert_array_equal(c["absolute_zero_reference_attenuation"]["adjusted_family3"], [0, 0])
        assert_allclose(c["origin_gain"]["adjusted_family3"], [.1, .1], atol=1e-14)
        with self.assertRaises(ValueError):
            m.inference(np.zeros((15, 2, 4)), (1, 1))


if __name__ == "__main__":
    unittest.main()
