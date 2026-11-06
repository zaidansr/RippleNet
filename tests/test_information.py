"""Deterministic analytic/negative controls, not the frozen experimental grid."""

from dataclasses import replace
import inspect
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet.information import (
    FROZEN_ORDERS, InformationConfig, _normal_grid, analytic_risks, integrate,
    linear_mean, observation_components, posterior, primary_posterior,
)


class InformationTests(unittest.TestCase):
    def test_frozen_settings_and_covariances(self) -> None:
        c = InformationConfig()
        self.assertEqual(FROZEN_ORDERS, (24, 48, 96, 192))
        self.assertEqual((c.a,c.process_variance,c.base_variance,c.measurement_variance,c.disturbance_variance,c.auxiliary_variance),
                         (.6,.01,.01/(1-.6**2),.0025,.25,.0025))
        first, second = observation_components(c)
        self.assertAlmostEqual(first.observation_covariance[0,0], second.observation_covariance[0,0])
        self.assertAlmostEqual(first.state_variance, c.base_variance)
        self.assertAlmostEqual(second.state_variance, c.base_variance+c.disturbance_variance)
        for component in (first,second):
            self.assertGreater(np.linalg.eigvalsh(component.observation_covariance).min(),0)
            self.assertFalse(component.observation_covariance.flags.writeable)

    def test_primary_mean_is_linear_with_equal_category_weights(self) -> None:
        c = InformationConfig()
        y = np.array([-.4,0.,.3])
        p = primary_posterior(y,c)
        expected=(c.base_variance+.5*c.disturbance_variance)/(c.base_variance+c.disturbance_variance+c.measurement_variance)*y
        assert_allclose(p.mean,expected,atol=1e-15)
        assert_array_equal(p.state_probability,np.full(3,.5))
        self.assertGreaterEqual(p.variance.min(),0)

    def test_zero_disturbance_matches_gaussian_precision_formula(self) -> None:
        c = InformationConfig(disturbance_variance=0.)
        yz = np.array([[.2,-.1],[-.3,.4]])
        result=posterior(yz,c)
        variance=1/(1/c.base_variance+1/c.measurement_variance+1/c.auxiliary_variance)
        expected=variance*(yz[:,0]/c.measurement_variance+yz[:,1]/c.auxiliary_variance)
        assert_allclose(result.mean,expected,atol=1e-15)
        assert_allclose(result.variance,variance,atol=1e-15)
        assert_allclose(result.mean,linear_mean(yz,c),atol=1e-15)

    def test_shared_control_is_linear_but_can_add_measurement_information(self) -> None:
        c = InformationConfig()
        yz=np.array([[.2,-.1],[-.3,.4]])
        result=posterior(yz,c,"shared")
        assert_array_equal(result.state_probability,np.full(2,.5))
        assert_allclose(result.mean,linear_mean(yz,c,"shared"),atol=1e-15)
        summary=integrate(c,"shared",8)
        self.assertGreater(summary.information_gain,0)
        self.assertLess(summary.approximation_gain,1e-28)
        self.assertAlmostEqual(summary.full_risk,summary.linear_risk,places=13)

    def test_duplicate_adds_no_information_or_approximation_gain(self) -> None:
        c=InformationConfig()
        y=np.array([-.4,0.,.3]);yz=np.column_stack((y,y))
        full=posterior(yz,c,"duplicate");primary=primary_posterior(y,c)
        assert_array_equal(full.mean,primary.mean)
        assert_array_equal(full.variance,primary.variance)
        summary=integrate(c,"duplicate",8)
        self.assertEqual(summary.information_gain,0)
        self.assertLess(summary.approximation_gain,1e-28)
        self.assertAlmostEqual(summary.full_risk,summary.primary_risk,places=14)

    def test_perfect_clean_auxiliary_reveals_current_state(self) -> None:
        c=InformationConfig(auxiliary_variance=0.)
        yz=np.array([[.2,-.1],[-.3,.4]])
        full=posterior(yz,c)
        assert_array_equal(full.mean,yz[:,1]);assert_array_equal(full.variance,np.zeros(2))
        summary=integrate(c,"clean",8)
        self.assertAlmostEqual(summary.full_risk,c.process_variance,places=15)
        self.assertEqual(summary.linear_risk,c.process_variance)
        self.assertEqual(summary.approximation_gain,0)
        self.assertAlmostEqual(summary.information_gain,summary.primary_risk-c.process_variance,places=14)

    def test_zero_transition_erases_all_target_headroom(self) -> None:
        c=InformationConfig(a=0.)
        for mode in ("clean","shared","duplicate"):
            summary=integrate(c,mode,6)
            self.assertAlmostEqual(summary.full_risk,c.process_variance,places=15)
            self.assertEqual(summary.primary_risk,c.process_variance)
            self.assertEqual(summary.linear_risk,c.process_variance)
            self.assertEqual(summary.information_gain,0)
            self.assertEqual(summary.approximation_gain,0)

    def test_deterministic_normal_moments_and_gaussian_order_refinement(self) -> None:
        c=InformationConfig(disturbance_variance=0.,measurement_variance=.02,auxiliary_variance=.02)
        previous=None
        for order in (4,8,16):
            grid,weights=_normal_grid(order)
            self.assertAlmostEqual(weights.sum(),1.,places=14)
            assert_allclose(weights@grid,np.zeros(2),atol=1e-15)
            assert_allclose(weights@(grid**2),np.ones(2),atol=1e-14)
            assert_allclose(weights@(grid**4),np.full(2,3.),atol=1e-13)
            result=integrate(c,"clean",order)
            self.assertLess(abs(result.primary_risk_identity_residual),1e-14)
            self.assertLess(abs(result.linear_risk_identity_residual),1e-14)
            if previous is not None:self.assertAlmostEqual(result.full_risk,previous,places=14)
            previous=result.full_risk
        self.assertEqual(integrate(c,"clean",8),integrate(c,"clean",8))

    def test_no_oracle_or_future_target_input_and_no_input_mutation(self) -> None:
        self.assertEqual(tuple(inspect.signature(posterior).parameters),("observations","config","mode"))
        yz=np.array([[.2,-.1],[-.3,.4]]);saved=yz.copy()
        result=posterior(yz)
        assert_array_equal(yz,saved)
        for values in (result.mean,result.variance,result.state_probability):self.assertFalse(values.flags.writeable)

    def test_invalid_inputs(self) -> None:
        for kwargs in ({"base_variance":0.},{"measurement_variance":0.},{"disturbance_variance":-.1},
                       {"a":True},{"a":np.inf},{"auxiliary_variance":np.nan}):
            with self.assertRaises(ValueError):InformationConfig(**kwargs)
        for values in (np.zeros(3),np.zeros((2,3)),np.array([[np.nan,0.]])):
            with self.assertRaises(ValueError):posterior(values)
        with self.assertRaises(ValueError):posterior([[1.,2.]],mode="duplicate")
        with self.assertRaises(ValueError):posterior([[1.,2.]],mode="unknown")
        for order in (True,1,1.5):
            with self.assertRaises(ValueError):integrate(order=order)


if __name__=="__main__":unittest.main()
