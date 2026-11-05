import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import Observations
from ripplenet.benchmark import configuration, initial_covariance, kalman, worlds
from ripplenet.mixture import mixture_forecasts, update
from ripplenet.statistics import paired_comparison


class MixtureTests(unittest.TestCase):
    def test_all_ablations_are_causal_and_match_prefix(self) -> None:
        cfg = configuration("moderate")
        run = worlds(cfg, 123, .5)
        time = run["state"].truth.events[0].time
        for mode in ("dual", "observation_only", "pooled"):
            a = mixture_forecasts(run["observation"].observed, cfg, mode)
            b = mixture_forecasts(run["state"].observed, cfg, mode)
            assert_allclose(a[:time+1], b[:time+1], atol=1e-12)
            changed = run["state"].observed.values.copy()
            changed[time+1:] += 100
            assert_array_equal(b[:time+1], mixture_forecasts(Observations(changed), cfg, mode)[:time+1])

    def test_zero_anomaly_scale_recovers_kalman_update(self) -> None:
        cfg = configuration("moderate")
        sim = worlds(cfg, 123, 0.)["clean"]
        mean, cov = np.zeros(3), initial_covariance(cfg)
        pred = []
        for y in sim.observed.values[:-1]:
            mean, cov = update(mean, cov, y, cfg, scale=0.)
            pred.append(cfg.transition @ mean)
        assert_allclose(pred, kalman(sim.observed, cfg), atol=1e-13)

    def test_current_dual_and_pooled_means_coincide_but_uncertainties_differ(self) -> None:
        cfg = configuration("moderate")
        prior = initial_covariance(cfg)
        y = np.array([1., -.7, .3])
        mean_a, cov_a = update(np.zeros(3), prior, y, cfg, "dual")
        mean_b, cov_b = update(np.zeros(3), prior, y, cfg, "pooled")
        assert_allclose(mean_a, mean_b, atol=1e-13)
        self.assertGreater(np.linalg.norm(cov_a-cov_b), 1e-3)
        self.assertGreaterEqual(np.linalg.eigvalsh(cov_a).min(), -1e-12)

    def test_constant_paired_ratio_and_invalid_data(self) -> None:
        result = paired_comparison(np.ones(30), np.full(30, 2.), 9)
        self.assertEqual(result["relative_improvement"], .5)
        assert_array_equal(result["ci95"], [.5, .5])
        assert_array_equal(result["adjusted_ci"], [.5, .5])
        for method, reference in (([1.], [2.]), ([1., 2.], [0., 2.]), ([1., np.nan], [2., 2.])):
            with self.assertRaises(ValueError):
                paired_comparison(np.array(method), np.array(reference))


if __name__ == "__main__":
    unittest.main()
