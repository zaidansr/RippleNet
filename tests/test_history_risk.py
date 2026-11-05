"""Causal risk identities, using fixture seed 123 rather than evaluation seeds."""

from dataclasses import replace
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import Config, Observations, paired_worlds
from ripplenet.benchmark import configuration
from ripplenet.history import known_time_forecasts
from ripplenet.history_risk import conditional_risks


class HistoryRiskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = configuration("moderate")
        self.time = 40
        _, self.world = paired_worlds(self.config, 123, self.time, (.5, -.4, .2))
        self.result = known_time_forecasts(self.world.observed, self.config, self.time)

    def test_decomposition_excess_and_oracle_identities(self) -> None:
        r = self.result
        risks = conditional_risks(r)
        assert_array_equal(r.bayes_risk, r.future_innovation_risk + r.within_type_state_risk + r.type_information_risk)
        assert_allclose(r.bayes_risk - risks.total_risk["category_oracle"], r.type_information_risk, atol=1e-17)
        for method in ("projected", "frozen"):
            expected = np.mean((r.forecasts[method] - r.forecasts["retained"])**2, axis=1)
            assert_array_equal(risks.excess_risk[method][self.time:], expected[self.time:])
            assert_array_equal(risks.total_risk[method], r.bayes_risk + risks.excess_risk[method])
            self.assertEqual(risks.excess_risk[method][self.time], 0.)
        for values in (r.future_innovation_risk, r.within_type_state_risk, r.type_information_risk,
                       r.bayes_risk, *risks.excess_risk.values(), *risks.total_risk.values()):
            self.assertTrue(np.isnan(values[:self.time]).all())
            self.assertTrue(np.isfinite(values[self.time:]).all())
            self.assertGreaterEqual(values[self.time:].min(), -1e-12)
            self.assertFalse(values.flags.writeable)

    def test_scalar_event_risk_matches_analytic_posterior(self) -> None:
        cfg = Config(np.array([[.5]]), np.array([[.1]]), np.array([[.2]]), n_steps=8, burn_in=0)
        r = known_time_forecasts(Observations(np.array([[.6], [-.1], [.3]])), cfg, 0, scale=.4)
        p, measurement, variance = .1, .2, .16
        denominator = p + measurement + variance
        m_observation = p / denominator * .6
        m_state = (p+variance) / denominator * .6
        p_observation = p * (measurement+variance) / denominator
        p_state = (p+variance) * measurement / denominator
        within = .25 * .5 * (p_observation + p_state)
        between = .25 * (.5 * (m_state-m_observation))**2
        self.assertAlmostEqual(r.future_innovation_risk[0], .1, places=15)
        self.assertAlmostEqual(r.within_type_state_risk[0], within, places=15)
        self.assertAlmostEqual(r.type_information_risk[0], between, places=15)
        self.assertAlmostEqual(r.bayes_risk[0], .1+within+between, places=15)

    def test_frozen_excess_has_closed_form_in_type_probability(self) -> None:
        r = self.result
        difference = r.forecasts["oracle_state"] - r.forecasts["oracle_observation"]
        squared_distance = np.mean(difference**2, axis=1)
        expected_excess = (r.state_probability - .5)**2 * squared_distance
        assert_allclose(conditional_risks(r).excess_risk["frozen"], expected_excess, rtol=1e-12, atol=1e-17)
        probabilities = np.exp(r.log_type_probabilities)
        assert_allclose(r.type_information_risk, probabilities[:, 0] * probabilities[:, 1] * squared_distance, rtol=1e-12, atol=1e-17)

    def test_zero_persistence_leaves_only_future_innovation(self) -> None:
        cfg = configuration("zero")
        _, world = paired_worlds(cfg, 123, self.time, (.5, -.4, .2))
        result = known_time_forecasts(world.observed, cfg, self.time)
        risks = conditional_risks(result)
        assert_array_equal(result.within_type_state_risk[self.time:], np.zeros(cfg.n_steps-1-self.time))
        assert_array_equal(result.type_information_risk[self.time:], np.zeros(cfg.n_steps-1-self.time))
        for values in risks.total_risk.values():
            assert_allclose(values[self.time:], .01, rtol=0, atol=2e-18)
        for values in risks.excess_risk.values():
            assert_array_equal(values[self.time:], np.zeros(cfg.n_steps-1-self.time))

    def test_zero_scale_has_no_type_headroom(self) -> None:
        result = known_time_forecasts(self.world.observed, self.config, self.time, scale=0.)
        assert_array_equal(result.type_information_risk[self.time:], np.zeros(self.config.n_steps-1-self.time))
        assert_allclose(result.bayes_risk, conditional_risks(result).total_risk["category_oracle"], atol=1e-15)

    def test_future_invariance_and_prefix_replay(self) -> None:
        changed = self.world.observed.values.copy()
        changed[self.time+2:] += 100
        perturbed = known_time_forecasts(Observations(changed), self.config, self.time)
        prefix = known_time_forecasts(Observations(self.world.observed.values[:self.time+3]), self.config, self.time)
        for name in ("future_innovation_risk", "within_type_state_risk", "type_information_risk", "bayes_risk"):
            assert_array_equal(getattr(self.result, name)[:self.time+2], getattr(perturbed, name)[:self.time+2])
            assert_array_equal(getattr(prefix, name), getattr(self.result, name)[:self.time+2])
        full_risks = conditional_risks(self.result)
        changed_risks = conditional_risks(perturbed)
        for method in full_risks.total_risk:
            assert_array_equal(full_risks.total_risk[method][:self.time+2], changed_risks.total_risk[method][:self.time+2])

    def test_risk_helper_does_not_change_forecasts_or_logweights(self) -> None:
        saved_forecasts = {name: values.copy() for name, values in self.result.forecasts.items()}
        saved_probabilities = self.result.state_probability.copy()
        saved_logs = self.result.log_type_probabilities.copy()
        conditional_risks(self.result)
        for name, values in saved_forecasts.items():
            assert_array_equal(values, self.result.forecasts[name])
        assert_array_equal(saved_probabilities, self.result.state_probability)
        assert_array_equal(saved_logs, self.result.log_type_probabilities)

    def test_invalid_risk_inputs_fail_without_clipping(self) -> None:
        with self.assertRaises(ValueError):
            conditional_risks(replace(self.result, bayes_risk=np.zeros(2)))
        invalid = self.result.bayes_risk.copy()
        invalid[self.time] = -1.
        with self.assertRaises(ValueError):
            conditional_risks(replace(self.result, bayes_risk=invalid))
        invalid = self.result.bayes_risk.copy()
        invalid[self.time] += .1
        with self.assertRaises(ValueError):
            conditional_risks(replace(self.result, bayes_risk=invalid))
        invalid = self.result.bayes_risk.copy()
        invalid[self.time+1] = np.nan
        with self.assertRaises(ValueError):
            conditional_risks(replace(self.result, bayes_risk=invalid))


if __name__ == "__main__":
    unittest.main()
