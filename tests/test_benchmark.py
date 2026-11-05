import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import Observations
from ripplenet.benchmark import configuration, initial_covariance, kalman, losses, worlds


class BenchmarkTests(unittest.TestCase):
    def test_every_ordinary_filter_respects_matched_prefix_and_future_invariance(self) -> None:
        cfg = configuration("moderate")
        run = worlds(cfg, 123, .5)
        time = run["state"].truth.events[0].time
        for mode in ("kalman", "clipped", "adaptive"):
            a = kalman(run["observation"].observed, cfg, mode)
            b = kalman(run["state"].observed, cfg, mode)
            assert_allclose(a[:time+1], b[:time+1], atol=1e-12)
            changed = run["state"].observed.values.copy()
            changed[time+1:] += 100
            assert_array_equal(b[:time+1], kalman(Observations(changed), cfg, mode)[:time+1])

    def test_label_privilege_is_rejected_for_ordinary_filter(self) -> None:
        cfg = configuration("moderate")
        sim = worlds(cfg, 123, .5)["state"]
        with self.assertRaises(ValueError):
            kalman(sim.observed, cfg, oracle=sim.truth.events[0])

    def test_oracle_does_not_use_realised_amplitude(self) -> None:
        from dataclasses import replace
        cfg = configuration("moderate")
        sim = worlds(cfg, 123, .5)["state"]
        event = sim.truth.events[0]
        a = kalman(sim.observed, cfg, "oracle", oracle=event)
        b = kalman(sim.observed, cfg, "oracle", oracle=replace(event, amplitude=(100., 100., 100.)))
        assert_array_equal(a, b)

    def test_burnin_covariance_and_zero_forecast_control(self) -> None:
        cfg = configuration("zero")
        assert_allclose(initial_covariance(cfg), cfg.process_cov)
        for sim in worlds(cfg, 123, .5).values():
            assert_array_equal(kalman(sim.observed, cfg), np.zeros((179, 3)))

    def test_price_error_creates_equal_opposite_return_errors(self) -> None:
        cfg = configuration("moderate")
        run = worlds(cfg, 123, .5, price_error=True)
        time = run["observation"].truth.events[0].time
        delta = run["observation"].observed.values - run["clean"].observed.values
        assert_allclose(delta[time], -delta[time+1], atol=1e-14)
        assert_array_equal(run["observation"].truth.latent, run["clean"].truth.latent)

    def test_window_scores_next_step_targets(self) -> None:
        cfg = configuration("moderate")
        sim = worlds(cfg, 123, .5)["state"]
        forecast = sim.truth.latent[1:].copy()
        time = sim.truth.events[0].time
        forecast[time:time+5] += 2
        score, _, delays = losses(forecast, sim.truth)
        self.assertEqual(score, 4.)
        assert_array_equal(delays, np.full(5, 4.))


if __name__ == "__main__":
    unittest.main()
