"""Handcrafted statistical invariants, with no reserved experiment seeds."""

import unittest

import numpy as np

from ripplenet.history_statistics import paired_comparison


class HistoryStatisticsTests(unittest.TestCase):
    def test_constant_proportional_gain_has_point_interval(self) -> None:
        reference = np.array([1.0, 2.0, 8.0, 11.0])
        result = paired_comparison(0.8 * reference, reference)
        self.assertAlmostEqual(result["improvement"], 0.2)
        np.testing.assert_allclose(result["ci95"], [0.2, 0.2], atol=1e-14)
        np.testing.assert_allclose(result["adjusted_ci"], [0.2, 0.2], atol=1e-14)
        self.assertEqual(result["n_seeds"], 4)
        self.assertEqual(result["units"], "relative_fraction")

    def test_identical_variable_losses_preserve_pairing(self) -> None:
        losses = np.array([0.1, 1.0, 10.0, 100.0, 1000.0])
        for relative in (True, False):
            with self.subTest(relative=relative):
                result = paired_comparison(losses, losses, relative=relative)
                self.assertEqual(result["improvement"], 0)
                self.assertEqual(result["ci95"], [0, 0])
                self.assertEqual(result["adjusted_ci"], [0, 0])

    def test_absolute_difference_can_be_negative(self) -> None:
        reference = np.array([0.0, 1.0, 3.0, 4.0])
        result = paired_comparison(reference + 2.0, reference, relative=False)
        self.assertEqual(result["improvement"], -2)
        self.assertEqual(result["ci95"], [-2, -2])
        self.assertEqual(result["adjusted_ci"], [-2, -2])
        self.assertEqual(result["units"], "loss_units")

    def test_ratio_of_means_not_mean_of_individual_ratios(self) -> None:
        result = paired_comparison(np.array([0.0, 1.0]), np.array([1.0, 4.0]))
        self.assertAlmostEqual(result["improvement"], 0.8)
        self.assertNotAlmostEqual(result["improvement"], 0.875)

    def test_results_reproduce_and_inputs_are_unchanged(self) -> None:
        method = np.array([0.8, 1.3, 2.0, 0.5])
        reference = np.array([1.0, 1.1, 2.2, 0.8])
        method_before, reference_before = method.copy(), reference.copy()
        first = paired_comparison(method, reference)
        self.assertEqual(first, paired_comparison(method, reference))
        np.testing.assert_array_equal(method, method_before)
        np.testing.assert_array_equal(reference, reference_before)

    def test_multiplicity_interval_encloses_raw_interval(self) -> None:
        result = paired_comparison(
            np.array([1.0, 2.0, 1.0, 3.0, 0.5]),
            np.array([1.5, 1.8, 2.0, 2.8, 1.2]),
            family_size=5,
        )
        self.assertLessEqual(result["adjusted_ci"][0], result["ci95"][0])
        self.assertGreaterEqual(result["adjusted_ci"][1], result["ci95"][1])

    def test_family_one_adjustment_is_identity(self) -> None:
        result = paired_comparison(np.array([1.0, 3.0]), np.array([2.0, 4.0]), family_size=1)
        self.assertEqual(result["ci95"], result["adjusted_ci"])

    def test_absolute_zero_losses_are_valid(self) -> None:
        result = paired_comparison(np.zeros(3), np.zeros(3), relative=False)
        self.assertEqual(result["improvement"], 0)
        self.assertEqual(result["ci95"], [0, 0])

    def test_invalid_losses_fail_explicitly(self) -> None:
        cases = [
            ([], []),
            ([1.0], [1.0]),
            ([[1.0, 2.0]], [[1.0, 2.0]]),
            ([1.0, 2.0], [1.0, 2.0, 3.0]),
            ([1.0, np.nan], [1.0, 2.0]),
            ([1.0, 2.0], [1.0, np.inf]),
            ([-1.0, 2.0], [1.0, 2.0]),
            ([1.0, 2.0], [1.0, -2.0]),
            ([1.0j, 2.0], [1.0, 2.0]),
        ]
        for method, reference in cases:
            with self.subTest(method=method, reference=reference):
                with self.assertRaises(ValueError):
                    paired_comparison(np.asarray(method), np.asarray(reference))

    def test_relative_zero_reference_mean_is_invalid(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive reference mean"):
            paired_comparison(np.ones(2), np.zeros(2))

    def test_relative_undefined_bootstrap_is_not_silently_dropped(self) -> None:
        with self.assertRaisesRegex(ValueError, "zero reference mean"):
            paired_comparison(np.array([0.0, 0.5]), np.array([0.0, 1.0]))

    def test_invalid_options_fail_explicitly(self) -> None:
        for size in (0, -1, 1.5, True, "5"):
            with self.subTest(family_size=size):
                with self.assertRaises(ValueError):
                    paired_comparison(np.ones(3), np.ones(3), family_size=size)
        with self.assertRaises(ValueError):
            paired_comparison(np.ones(3), np.ones(3), relative="yes")


if __name__ == "__main__":
    unittest.main()
