"""Mathematical and causal invariants, rather than implementation-mirroring tests."""

import unittest
from dataclasses import replace

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import Config, Event, Observations, paired_worlds, simulate
from ripplenet.filtering import causal_forecasts


def config() -> Config:
    return Config(
        np.array([[0.6, 0.1], [0.0, 0.4]]), np.eye(2) * 0.01,
        np.eye(2) * 0.0025, n_steps=60, burn_in=64,
    )


class SimulatorTests(unittest.TestCase):
    def test_seed_reproducibility(self) -> None:
        a, b = simulate(config(), 17), simulate(config(), 17)
        assert_array_equal(a.observed.values, b.observed.values)
        assert_array_equal(a.truth.latent, b.truth.latent)

    def test_distinct_seeds(self) -> None:
        self.assertFalse(np.array_equal(simulate(config(), 17).truth.latent, simulate(config(), 18).truth.latent))

    def test_observation_error_never_changes_latent_state(self) -> None:
        clean = simulate(config(), 17)
        bad = simulate(config(), 17, [Event(20, "observation", (2.0, 0.0))])
        assert_array_equal(clean.truth.latent, bad.truth.latent)
        expected = np.zeros_like(clean.observed.values)
        expected[20, 0] = 2
        assert_allclose(bad.observed.values - clean.observed.values, expected, atol=1e-14)

    def test_state_impulse_propagates_once(self) -> None:
        cfg = config()
        clean = simulate(cfg, 17)
        shock = simulate(cfg, 17, [Event(20, "state", (0.0, 2.0))])
        assert_array_equal(shock.truth.latent[:20], clean.truth.latent[:20])
        effect = np.array([0.0, 2.0])
        for time in range(20, cfg.n_steps):
            assert_allclose(shock.truth.latent[time] - clean.truth.latent[time], effect, atol=1e-13)
            effect = cfg.transition @ effect

    def test_counterfactual_observed_prefix_matches(self) -> None:
        obs, state = paired_worlds(config(), 17, 20, (2.0, 0.0))
        assert_allclose(obs.observed.values[:21], state.observed.values[:21], atol=1e-14)
        self.assertGreater(np.linalg.norm(obs.observed.values[21] - state.observed.values[21]), 0.1)

    def test_zero_persistence_erases_state_effect_after_event(self) -> None:
        cfg = replace(config(), transition=np.zeros((2, 2)))
        obs, state = paired_worlds(cfg, 17, 20, (2.0, 0.0))
        assert_allclose(obs.observed.values, state.observed.values, atol=1e-14)
        assert_array_equal(obs.truth.latent[21:], state.truth.latent[21:])

    def test_zero_noise_is_supported(self) -> None:
        cfg = replace(config(), process_cov=np.zeros((2, 2)), observation_cov=np.zeros((2, 2)))
        assert_array_equal(simulate(cfg, 3).observed.values, np.zeros((60, 2)))

    def test_invalid_matrices(self) -> None:
        cfg = config()
        for kwargs in (
            {"transition": np.eye(2)}, {"transition": np.ones((2, 3))},
            {"process_cov": -np.eye(2)}, {"observation_cov": np.array([[1., 1.], [0., 1.]])},
            {"transition": np.array([[np.nan, 0], [0, 0]])},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                replace(cfg, **kwargs)

    def test_invalid_events_and_scoring_boundaries(self) -> None:
        for events in (
            [Event(55, "state", (1., 0.))],
            [Event(20, "state", (1., 0.)), Event(25, "observation", (1., 0.))],
            [Event(20, "state", (1.,))],
        ):
            with self.subTest(events=events), self.assertRaises(ValueError):
                simulate(config(), 3, events)
        simulate(config(), 3, [Event(54, "state", (1., 0.))])
        with self.assertRaises(ValueError):
            Event(-1, "state", (1., 0.))
        with self.assertRaises(ValueError):
            Event(1, "unknown", (1., 0.))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            simulate(config(), -1)

    def test_public_interface_has_no_labels(self) -> None:
        sim = simulate(config(), 3, [Event(20, "state", (1., 0.))])
        self.assertEqual(set(vars(sim.observed)), {"values"})
        self.assertFalse(sim.observed.values.flags.writeable)


class CausalityTests(unittest.TestCase):
    def test_matched_prefix_gives_same_event_origin_forecast(self) -> None:
        cfg = config()
        obs, state = paired_worlds(cfg, 17, 20, (2.0, 0.0))
        a = causal_forecasts(obs.observed, cfg)
        b = causal_forecasts(state.observed, cfg)
        assert_allclose(a[:21], b[:21], atol=1e-13)

    def test_future_observations_cannot_change_earlier_forecasts(self) -> None:
        cfg = config()
        original = simulate(cfg, 17).observed
        modified = original.values.copy()
        modified[21:] += 1000
        assert_array_equal(causal_forecasts(original, cfg)[:21], causal_forecasts(Observations(modified), cfg)[:21])

    def test_scalar_first_update_matches_hand_calculation(self) -> None:
        cfg = Config(np.array([[0.5]]), np.array([[0.1]]), np.array([[0.2]]), n_steps=10)
        y = Observations(np.array([[2.0], [0.0]]))
        # prior P=.5^2 * 1 + .1 = .35; K=.35/.55; forecast=.5*K*2.
        assert_allclose(causal_forecasts(y, cfg)[0, 0], 0.5 * (0.35 / 0.55) * 2.0)

    def test_singular_filter_covariance_fails_explicitly(self) -> None:
        cfg = replace(config(), transition=np.zeros((2, 2)), process_cov=np.zeros((2, 2)), observation_cov=np.zeros((2, 2)))
        with self.assertRaisesRegex(ValueError, "Singular"):
            causal_forecasts(simulate(cfg, 3).observed, cfg)


if __name__ == "__main__":
    unittest.main()
