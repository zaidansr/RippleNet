"""Invariant tests for the known-time mechanism diagnostic, without final seeds."""

import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import Config, Observations, paired_worlds
from ripplenet.benchmark import configuration, kalman
from ripplenet.history import _normalized_logs, _weighted_moments, known_time_forecasts


class HistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = configuration("moderate")
        self.time = 40
        self.observation, self.state = paired_worlds(self.config, 123, self.time, (.5, -.4, .2))

    def test_causal_prefix_and_future_invariance(self) -> None:
        left = known_time_forecasts(self.observation.observed, self.config, self.time)
        right = known_time_forecasts(self.state.observed, self.config, self.time)
        changed = self.state.observed.values.copy()
        changed[self.time + 2:] += 100
        perturbed = known_time_forecasts(Observations(changed), self.config, self.time)
        prefix = known_time_forecasts(
            Observations(self.state.observed.values[:self.time + 3]), self.config, self.time,
        )
        for name in right.forecasts:
            assert_allclose(left.forecasts[name][:self.time+1], right.forecasts[name][:self.time+1], atol=1e-13)
            assert_array_equal(right.forecasts[name][:self.time+2], perturbed.forecasts[name][:self.time+2])
            assert_array_equal(prefix.forecasts[name], right.forecasts[name][:self.time+2])
        assert_array_equal(prefix.log_type_probabilities, right.log_type_probabilities[:self.time+2])
        assert_array_equal(right.state_probability[:self.time+2], perturbed.state_probability[:self.time+2])

    def test_event_has_equal_weights_and_identical_ordinary_forecasts(self) -> None:
        result = known_time_forecasts(self.state.observed, self.config, self.time)
        self.assertTrue(np.isnan(result.state_probability[:self.time]).all())
        self.assertTrue(np.isnan(result.log_type_probabilities[:self.time]).all())
        self.assertEqual(result.state_probability[self.time], .5)
        assert_array_equal(result.log_type_probabilities[self.time], np.full(2, -np.log(2.)))
        for name in ("projected", "frozen"):
            assert_array_equal(result.forecasts["retained"][:self.time+1], result.forecasts[name][:self.time+1])
        # The frozen ablation shares the component trajectories exactly.
        assert_allclose(result.forecasts["frozen"], .5 * (
            result.forecasts["oracle_observation"] + result.forecasts["oracle_state"]), atol=1e-15)
        self.assertGreater(np.linalg.norm(result.forecasts["retained"] - result.forecasts["frozen"]), 1e-5)

    def test_zero_persistence_erases_information_and_forecasts(self) -> None:
        cfg = configuration("zero")
        _, state = paired_worlds(cfg, 123, self.time, (.5, -.4, .2))
        result = known_time_forecasts(state.observed, cfg, self.time)
        for output in result.forecasts.values():
            assert_array_equal(output, np.zeros((cfg.n_steps - 1, cfg.n_assets)))
        assert_array_equal(result.state_probability[self.time:], np.full(cfg.n_steps-1-self.time, .5))

    def test_zero_scale_recovers_ordinary_filter(self) -> None:
        result = known_time_forecasts(self.state.observed, self.config, self.time, scale=0.)
        ordinary = kalman(self.state.observed, self.config)
        for output in result.forecasts.values():
            assert_allclose(output, ordinary, rtol=1e-12, atol=1e-14)
        assert_array_equal(result.state_probability[self.time:], np.full(len(ordinary)-self.time, .5))

    def test_projection_includes_between_component_variance_and_is_label_invariant(self) -> None:
        means = np.array([[1., 2.], [-3., 1.]])
        covariances = np.array([np.eye(2), 2*np.eye(2)])
        weights = np.array([.25, .75])
        mean, covariance = _weighted_moments(means, covariances, weights)
        permuted = _weighted_moments(means[::-1], covariances[::-1], weights[::-1])
        assert_array_equal(mean, permuted[0])
        assert_array_equal(covariance, permuted[1])
        assert_allclose(mean, [-2., 1.25])
        assert_allclose(covariance, [[4.75, .75], [.75, 1.9375]])
        self.assertGreater(np.linalg.eigvalsh(covariance).min(), 0)

    def test_log_weights_remain_finite_when_probabilities_underflow(self) -> None:
        logs = _normalized_logs(np.array([-10000., 0.]))
        assert_array_equal(logs, [-10000., 0.])
        self.assertEqual(float(np.exp(logs[0])), 0.)
        self.assertTrue(np.isfinite(logs).all())

    def test_scalar_two_step_posterior_matches_direct_calculation(self) -> None:
        cfg = Config(np.array([[.5]]), np.array([[.1]]), np.array([[.2]]), n_steps=8, burn_in=0)
        observations = Observations(np.array([[.6], [-.1], [.3]]))
        result = known_time_forecasts(observations, cfg, 0, scale=.4)
        p, r, variance = .1, .2, .16
        observation_mean = p / (p+r+variance) * .6
        state_mean = (p+variance) / (p+r+variance) * .6
        observation_covariance = p * (r+variance) / (p+r+variance)
        state_covariance = (p+variance) * r / (p+r+variance)
        predicted_means = .5 * np.array([observation_mean, state_mean])
        predicted_variances = .25 * np.array([observation_covariance, state_covariance]) + .1
        residuals = -.1 - predicted_means
        innovation_variances = predicted_variances + .2
        likelihoods = np.exp(-.5 * residuals**2 / innovation_variances) / np.sqrt(innovation_variances)
        probability = likelihoods[1] / likelihoods.sum()
        self.assertAlmostEqual(result.state_probability[1], probability, places=14)
        branch_means = predicted_means + predicted_variances / innovation_variances * residuals
        self.assertAlmostEqual(result.forecasts["retained"][1, 0], .5 * np.dot(likelihoods / likelihoods.sum(), branch_means), places=14)

    def test_inputs_are_unchanged_and_results_readonly(self) -> None:
        original = self.state.observed.values.copy()
        result = known_time_forecasts(self.state.observed, self.config, self.time)
        assert_array_equal(self.state.observed.values, original)
        for output in (*result.forecasts.values(), result.state_probability, result.log_type_probabilities):
            self.assertFalse(output.flags.writeable)

    def test_invalid_inputs_and_singular_innovations(self) -> None:
        for time in (-1, True, 1.5, self.config.n_steps-1):
            with self.subTest(time=time), self.assertRaises(ValueError):
                known_time_forecasts(self.state.observed, self.config, time)
        for scale in (-.1, np.nan, np.inf, 1e308, .5j, True, "bad", np.array([.5])):
            with self.subTest(scale=scale), self.assertRaises(ValueError):
                known_time_forecasts(self.state.observed, self.config, self.time, scale)
        for values in (np.zeros((2, 2)), np.zeros(3), np.zeros((1, 3)), np.full((3, 3), np.nan)):
            with self.assertRaises(ValueError):
                known_time_forecasts(Observations(values), self.config, 0)
        cfg = Config(np.array([[.5]]), np.zeros((1, 1)), np.zeros((1, 1)), n_steps=8)
        with self.assertRaisesRegex(ValueError, "Positive definite"):
            known_time_forecasts(Observations(np.zeros((8, 1))), cfg, 1)


if __name__ == "__main__":
    unittest.main()
