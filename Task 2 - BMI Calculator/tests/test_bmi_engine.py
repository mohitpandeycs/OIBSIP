"""Unit tests for the BMIEngine class.

Tests correct BMI calculation for known weight/height pairs,
classification accuracy for all four WHO categories, boundary
values at category thresholds, edge cases, and rounding.
"""

import unittest

from advanced.core.bmi_engine import BMIEngine, BMIResult, BMICategory


class TestCalculateBMI(unittest.TestCase):
    """Tests for BMIEngine.calculate_bmi()."""

    def test_normal_bmi(self):
        """Typical weight/height should produce expected BMI."""
        # 70 kg, 1.75 m → BMI = 70 / 1.75² = 22.857... → 22.86
        result = BMIEngine.calculate_bmi(70.0, 1.75)
        self.assertAlmostEqual(result, 22.86, places=2)

    def test_underweight_bmi(self):
        """Low weight / tall height should produce a low BMI."""
        # 45 kg, 1.80 m → BMI = 45 / 3.24 = 13.89
        result = BMIEngine.calculate_bmi(45.0, 1.80)
        self.assertAlmostEqual(result, 13.89, places=2)

    def test_obese_bmi(self):
        """High weight / short height should produce a high BMI."""
        # 120 kg, 1.60 m → BMI = 120 / 2.56 = 46.875 → 46.87 (banker's rounding)
        result = BMIEngine.calculate_bmi(120.0, 1.60)
        self.assertAlmostEqual(result, 46.87, places=2)

    def test_rounding_to_two_decimals(self):
        """BMI should be rounded to exactly 2 decimal places."""
        # 68 kg, 1.72 m → BMI = 68 / 2.9584 = 22.985... → 22.99
        result = BMIEngine.calculate_bmi(68.0, 1.72)
        self.assertEqual(result, 22.99)

    def test_exact_whole_bmi(self):
        """Values that produce a whole-number BMI."""
        # 25 kg, 1.0 m → BMI = 25.0
        result = BMIEngine.calculate_bmi(25.0, 1.0)
        self.assertEqual(result, 25.0)

    def test_integer_inputs(self):
        """Integer inputs should be accepted (not just floats)."""
        result = BMIEngine.calculate_bmi(70, 175)
        self.assertIsInstance(result, float)

    def test_zero_height_raises_value_error(self):
        """Height of zero should raise ValueError."""
        with self.assertRaises(ValueError):
            BMIEngine.calculate_bmi(70.0, 0.0)

    def test_negative_height_raises_value_error(self):
        """Negative height should raise ValueError."""
        with self.assertRaises(ValueError):
            BMIEngine.calculate_bmi(70.0, -1.75)

    def test_negative_weight_raises_value_error(self):
        """Negative weight should raise ValueError."""
        with self.assertRaises(ValueError):
            BMIEngine.calculate_bmi(-70.0, 1.75)

    def test_non_numeric_weight_raises_type_error(self):
        """Non-numeric weight should raise TypeError."""
        with self.assertRaises(TypeError):
            BMIEngine.calculate_bmi("seventy", 1.75)

    def test_non_numeric_height_raises_type_error(self):
        """Non-numeric height should raise TypeError."""
        with self.assertRaises(TypeError):
            BMIEngine.calculate_bmi(70.0, "one point seven five")

    def test_very_small_height(self):
        """Very small positive height should still compute."""
        result = BMIEngine.calculate_bmi(70.0, 0.01)
        self.assertGreater(result, 0)

    def test_boundary_weight_min(self):
        """Minimum valid weight should compute correctly."""
        result = BMIEngine.calculate_bmi(20.0, 1.70)
        self.assertAlmostEqual(result, 6.92, places=2)

    def test_boundary_weight_max(self):
        """Maximum valid weight should compute correctly."""
        result = BMIEngine.calculate_bmi(300.0, 1.70)
        self.assertAlmostEqual(result, 103.81, places=2)


class TestClassifyBMI(unittest.TestCase):
    """Tests for BMIEngine.classify_bmi()."""

    def test_underweight_category(self):
        """BMI below 18.5 should classify as Underweight."""
        result = BMIEngine.classify_bmi(17.0)
        self.assertEqual(result.category, BMICategory.UNDERWEIGHT)
        self.assertEqual(result.bmi, 17.0)

    def test_normal_category(self):
        """BMI between 18.5 and 24.9 should classify as Normal."""
        result = BMIEngine.classify_bmi(22.0)
        self.assertEqual(result.category, BMICategory.NORMAL)
        self.assertEqual(result.bmi, 22.0)

    def test_overweight_category(self):
        """BMI between 25.0 and 29.9 should classify as Overweight."""
        result = BMIEngine.classify_bmi(27.5)
        self.assertEqual(result.category, BMICategory.OVERWEIGHT)
        self.assertEqual(result.bmi, 27.5)

    def test_obese_category(self):
        """BMI of 30.0 or above should classify as Obese."""
        result = BMIEngine.classify_bmi(35.0)
        self.assertEqual(result.category, BMICategory.OBESE)
        self.assertEqual(result.bmi, 35.0)

    def test_boundary_underweight_normal(self):
        """BMI of 18.499... should still be Underweight."""
        result = BMIEngine.classify_bmi(18.49)
        self.assertEqual(result.category, BMICategory.UNDERWEIGHT)

    def test_boundary_normal_lower(self):
        """BMI of exactly 18.5 should be Normal."""
        result = BMIEngine.classify_bmi(18.5)
        self.assertEqual(result.category, BMICategory.NORMAL)

    def test_boundary_normal_upper(self):
        """BMI of 24.9 should still be Normal."""
        result = BMIEngine.classify_bmi(24.9)
        self.assertEqual(result.category, BMICategory.NORMAL)

    def test_boundary_overweight_lower(self):
        """BMI of exactly 25.0 should be Overweight."""
        result = BMIEngine.classify_bmi(25.0)
        self.assertEqual(result.category, BMICategory.OVERWEIGHT)

    def test_boundary_overweight_upper(self):
        """BMI of 29.9 should still be Overweight."""
        result = BMIEngine.classify_bmi(29.9)
        self.assertEqual(result.category, BMICategory.OVERWEIGHT)

    def test_boundary_obese_lower(self):
        """BMI of exactly 30.0 should be Obese."""
        result = BMIEngine.classify_bmi(30.0)
        self.assertEqual(result.category, BMICategory.OBESE)

    def test_very_high_bmi(self):
        """Very high BMI should classify as Obese."""
        result = BMIEngine.classify_bmi(100.0)
        self.assertEqual(result.category, BMICategory.OBESE)

    def test_very_low_bmi(self):
        """Very low BMI should classify as Underweight."""
        result = BMIEngine.classify_bmi(5.0)
        self.assertEqual(result.category, BMICategory.UNDERWEIGHT)

    def test_result_is_bmi_result_instance(self):
        """classify_bmi should return a BMIResult dataclass."""
        result = BMIEngine.classify_bmi(22.0)
        self.assertIsInstance(result, BMIResult)

    def test_result_has_explanation(self):
        """BMIResult should contain a non-empty explanation."""
        result = BMIEngine.classify_bmi(22.0)
        self.assertTrue(len(result.explanation) > 0)

    def test_result_is_frozen(self):
        """BMIResult should be immutable (frozen dataclass)."""
        result = BMIEngine.classify_bmi(22.0)
        with self.assertRaises(AttributeError):
            result.bmi = 30.0

    def test_non_numeric_bmi_raises_type_error(self):
        """Non-numeric BMI should raise TypeError."""
        with self.assertRaises(TypeError):
            BMIEngine.classify_bmi("twenty-two")

    def test_bmi_rounding_in_classify(self):
        """BMI value in result should be rounded to 2 decimal places."""
        result = BMIEngine.classify_bmi(22.8567)
        self.assertEqual(result.bmi, 22.86)

    def test_all_categories_have_explanations(self):
        """All four categories should have non-empty explanations."""
        test_bmis = [17.0, 22.0, 27.0, 35.0]
        for bmi in test_bmis:
            result = BMIEngine.classify_bmi(bmi)
            self.assertTrue(len(result.explanation) > 0,
                            f"Category {result.category} has no explanation")


if __name__ == "__main__":
    unittest.main()