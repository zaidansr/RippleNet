"""Invented observations test market-study leakage boundaries and estimands."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import market_study as m


def day(name: str, n: int = 40) -> m.Day:
    k = np.arange(n)
    x, y = m.arrays(np.exp(.01*np.sin(k)+.001*k))
    return m.Day(name, x, y, {"date": name, "recorded_rows": n})


class MarketTests(unittest.TestCase):
    def test_exact_features_targets_and_coverage(self) -> None:
        logs = np.arange(31, dtype=float)**2 * .0001
        x, y = m.arrays(np.exp(logs))
        self.assertEqual(x.shape, (16, 5))
        assert_allclose(x[0], np.diff(logs)[[4, 3, 2, 1, 0]], atol=1e-15)
        self.assertAlmostEqual(y[0], logs[15]-logs[5])
        self.assertAlmostEqual(y[-1], logs[30]-logs[20])
        self.assertFalse(x.flags.writeable)
        self.assertFalse(y.flags.writeable)

    def test_future_tail_changes_no_earlier_feature(self) -> None:
        prices = np.exp(np.arange(40)*.001)
        changed = prices.copy()
        changed[21:] *= 2
        a, ya = m.arrays(prices)
        b, yb = m.arrays(changed)
        assert_array_equal(a[:16], b[:16])  # origins 5..20, inclusive
        assert_array_equal(ya[:6], yb[:6])  # completed endpoints <=20
        self.assertFalse(np.array_equal(ya, yb))

    def test_day_without_eligible_origin_fails_not_silently_dropped(self) -> None:
        for prices in (np.ones(15), np.array([1., np.nan]*20), np.zeros(40)):
            with self.assertRaises(ValueError):
                m.arrays(prices)

    def test_equal_day_weights_and_unpenalised_intercept(self) -> None:
        a = m.Day("a", np.zeros((2, 5)), np.array([1., 1.]), {})
        b = m.Day("b", np.zeros((10, 5)), np.full(10, 3.), {})
        model = m.fit([a, b], 100.)
        self.assertAlmostEqual(model["target_mean"], 2.)
        assert_allclose(model["scale"], np.ones(5))
        assert_allclose(m.predict(a, model), [2., 2.])
        assert_allclose(model["beta"], np.zeros(5))

    def test_ols_recovers_known_coefficients_and_scaler_uses_training_only(self) -> None:
        rng = np.random.default_rng(5)
        x = rng.normal(size=(100, 5))
        beta = np.arange(1, 6)*.01
        train = m.Day("train", x, .3+x@beta, {})
        model = m.fit([train], 0.)
        held = m.Day("test", x+100, .3+(x+100)@beta, {})
        assert_allclose(m.predict(held, model), held.y, atol=1e-12)
        assert_allclose(model["mean"], x.mean(axis=0))
        saved = json.dumps(model)
        m.losses(held, model)
        self.assertEqual(json.dumps(model), saved)

    def test_lag_mean_has_ten_row_scale(self) -> None:
        sample = m.Day("d", np.full((4, 5), .001), np.zeros(4), {})
        model = m.fit([sample], 1.)
        assert_allclose(m.predictions(sample, model)["lagmean"], .01)

    def test_development_never_opens_test_dates(self) -> None:
        seen = []
        def load(_directory: Path, name: str) -> m.Day:
            self.assertIn(name, m.DATES[:15])
            seen.append(name)
            return day(name)
        with tempfile.TemporaryDirectory() as temp, patch.object(m, "load_day", load):
            output = Path(temp)/"new"
            result = m.development(Path(temp), output)
            self.assertEqual(seen, list(m.DATES[:15]))
            self.assertEqual(result["test_dates_unopened"], list(m.DATES[15:]))
            self.assertFalse(result["refit_on_validation"])
            with self.assertRaises(FileExistsError):
                m.development(Path(temp), output)

    def test_test_stage_no_refit_and_selection_source_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp, patch.object(m, "load_day", lambda p, n: day(n)):
            output = Path(temp)/"new"
            m.development(Path(temp), output)
            with patch.object(m, "fit", side_effect=AssertionError("Must not refit")):
                result = m.test(Path(temp), output)
            self.assertEqual(len(result["daily"]), 15)
            self.assertEqual([r["date"] for r in result["daily"]], list(m.DATES[15:]))
            with self.assertRaises(FileExistsError):
                m.test(Path(temp), output)
            (output/"test.json").unlink()
            selection = json.loads((output/"selection.json").read_text())
            selection["source_sha256"] = {}
            (output/"selection.json").write_text(json.dumps(selection))
            with self.assertRaises(ValueError):
                m.test(Path(temp), output)

    def test_bootstrap_pairing_ratio_and_reproducibility(self) -> None:
        baseline = np.arange(1, 16, dtype=float)
        values = np.column_stack((.8*baseline, baseline, 2*baseline, 3*baseline))
        first = m.bootstrap(values, 1)
        self.assertEqual(first, m.bootstrap(values, 1))
        self.assertAlmostEqual(first["gain_fraction"], .2)
        assert_allclose(first["adjusted_97_5_gain"], [.2, .2], atol=1e-14)
        self.assertEqual(first["n_days"], 15)
        with self.assertRaises(ValueError):
            m.bootstrap(np.zeros((15, 4)), 1)


if __name__ == "__main__":
    unittest.main()
