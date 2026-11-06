"""Fixture-only tests; no reserved sensitivity seeds are evaluated."""

import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet.benchmark import configuration, worlds
from ripplenet.noise_sensitivity import (
    BOOTSTRAP_REPLICATES, DEFAULT_RATIOS, DEFAULT_SEEDS, _inputs, _summaries,
    configuration_for_ratio, evaluate,
)


class NoiseSensitivityTests(unittest.TestCase):
    def test_frozen_defaults_and_only_R_changes(self) -> None:
        self.assertEqual(DEFAULT_RATIOS, (0., .25, 1., 4., 16.))
        self.assertEqual(DEFAULT_SEEDS, tuple(range(70000, 70128)))
        base = configuration("moderate")
        for ratio in DEFAULT_RATIOS:
            cfg = configuration_for_ratio(ratio)
            assert_array_equal(cfg.transition, base.transition)
            assert_array_equal(cfg.process_cov, base.process_cov)
            assert_array_equal(cfg.observation_cov, .01*ratio*np.eye(3))
            self.assertEqual((cfg.n_steps, cfg.burn_in), (180, 128))

    def test_coupled_latent_events_and_standardized_measurement_stream(self) -> None:
        low = worlds(configuration_for_ratio(.25), 123, .5)
        high = worlds(configuration_for_ratio(4.), 123, .5)
        for category in ("clean", "observation", "state"):
            assert_array_equal(low[category].truth.latent, high[category].truth.latent)
            self.assertEqual(low[category].truth.events, high[category].truth.events)
        low_noise = low["clean"].observed.values-low["clean"].truth.latent
        high_noise = high["clean"].observed.values-high["clean"].truth.latent
        assert_allclose(low_noise/.05, high_noise/.2, atol=1e-14)

    def test_bootstrap_uses_ratio_of_means_and_declared_adjustment(self) -> None:
        indices = np.tile(np.array([[0, 1], [1, 1], [0, 0]]), (3333, 1))
        blocks = {name: np.array([1., 2.]) for name in (
            "future", "within_type", "type_information", "bayes", "frozen_excess", "frozen_total", "category_oracle", "retained_mse", "projected_mse")}
        blocks["projected_excess"] = np.array([.1, 1.])
        blocks["projected_total"] = np.array([1., 4.])
        summary = _summaries(blocks, indices)
        primary = summary["projection_improvement_fraction"]
        self.assertAlmostEqual(primary["ratio_of_means"], 1.1/5.)
        self.assertNotAlmostEqual(primary["ratio_of_means"], np.mean([.1, .25]))
        self.assertEqual(primary["adjustment_family_size"], 5)
        self.assertLessEqual(primary["adjusted_ci99"][0], primary["ci95"][0])
        self.assertGreaterEqual(primary["adjusted_ci99"][1], primary["ci95"][1])

    def test_fixture_runner_outputs_reconcile_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"fixture"
            with contextlib.redirect_stdout(io.StringIO()):
                summary = evaluate(output, seeds=[123, 124], ratios=[0., .25])
            self.assertEqual(summary["status"], "custom_or_fixture_configuration")
            self.assertEqual(summary["bootstrap_replicates"], BOOTSTRAP_REPLICATES)
            self.assertEqual(len(summary["cells"]), 2)
            self.assertIn("ripplenet/noise_sensitivity.py", summary["source_sha256"])
            self.assertEqual(json.loads((output/"summary.json").read_text())["ratios"], [0., .25])
            for cell in summary["cells"]:
                with (output/cell["path"]).open(newline="", encoding="utf-8") as stream:
                    rows = list(csv.DictReader(stream))
                self.assertEqual(len(rows), 20)
                self.assertEqual({int(r["seed"]) for r in rows}, {123, 124})
                delayed = [r for r in rows if int(r["delay"]) > 0]
                for field in ("bayes", "projected_total", "retained_mse", "projected_mse"):
                    self.assertAlmostEqual(np.mean([float(r[field]) for r in delayed]), cell["delayed_origins_1_to_4"][field]["mean"], places=15)
                self.assertLessEqual(cell["checks"]["max_matched_prefix_gap"], 1e-12)
                if cell["ratio"] == 0:
                    for row in delayed:
                        self.assertAlmostEqual(float(row["bayes"]), .01, places=14)
                        self.assertLess(float(row["projected_excess"]), 1e-25)
                        self.assertAlmostEqual(float(row["retained_mse"]), float(row["projected_mse"]), places=14)
                    self.assertNotAlmostEqual(cell["delayed_origins_1_to_4"]["retained_mse"]["mean"], .01, places=6)
            with self.assertRaises(FileExistsError):
                evaluate(output, seeds=[123, 124], ratios=[0.])

    def test_invalid_settings_fail_before_creating_output(self) -> None:
        for seeds, ratios in (([123], [0.]), ([123, 123], [0.]), ([True, 124], [0.]),
                              ([123, -1], [0.]), ([123, 124], []), ([123, 124], [0., 0.]),
                              ([123, 124], [-1.]), ([123, 124], [np.nan]),
                              ([123, 124], list(range(6)))):
            with self.subTest(seeds=seeds, ratios=ratios), self.assertRaises(ValueError):
                _inputs(seeds, ratios)
        for ratio in (True, "0", np.inf, -.1):
            with self.assertRaises(ValueError):
                configuration_for_ratio(ratio)


if __name__ == "__main__":
    unittest.main()
