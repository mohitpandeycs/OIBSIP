"""Unit tests for the InputValidator class.

Tests valid weight/height strings, out-of-range values, non-numeric
inputs, empty strings, negative values, boundary values, and correct
error messages for each failure case.
"""

import unittest

from advanced.core.validators import InputValidator, ValidationResult, WEIGHT_MIN, WEIGHT_MAX, HEIGHT_MIN, HEIGHT_MAX


class TestValidateWeight(unittest.TestCase):
    """Tests for InputValidator.validate_weight()."""

    def test_valid_weight(self):
        """A normal weight string should validate successfully."""
        result = InputValidator.validate_weight("70.5")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 70.5)
        self.assertEqual(result.error_message, "")

    def test_valid_weight_integer_string(self):
        """An integer weight string should validate."""
        result = InputValidator.validate_weight("70")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 70.0)

    def test_valid_weight_with_whitespace(self):
        """Weight string with leading/trailing whitespace should validate."""
        result = InputValidator.validate_weight("  75.0  ")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 75.0)

    def test_valid_weight_min_boundary(self):
        """Weight at minimum boundary (20.0) should validate."""
        result = InputValidator.validate_weight("20.0")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, WEIGHT_MIN)

    def test_valid_weight_max_boundary(self):
        """Weight at maximum boundary (300.0) should validate."""
        result = InputValidator.validate_weight("300.0")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, WEIGHT_MAX)

    def test_empty_string(self):
        """Empty string should fail validation."""
        result = InputValidator.validate_weight("")
        self.assertFalse(result.is_valid)
        self.assertEqual(result.value, 0.0)
        self.assertIn("empty", result.error_message.lower())

    def test_whitespace_only(self):
        """Whitespace-only string should fail validation."""
        result = InputValidator.validate_weight("   ")
        self.assertFalse(result.is_valid)
        self.assertIn("empty", result.error_message.lower())

    def test_non_numeric(self):
        """Non-numeric string should fail validation."""
        result = InputValidator.validate_weight("abc")
        self.assertFalse(result.is_valid)
        self.assertIn("numeric", result.error_message.lower())

    def test_negative_weight(self):
        """Negative weight should fail validation."""
        result = InputValidator.validate_weight("-70")
        self.assertFalse(result.is_valid)
        self.assertIn("negative", result.error_message.lower())

    def test_below_minimum(self):
        """Weight below minimum should fail with 'too low' message."""
        result = InputValidator.validate_weight("19.9")
        self.assertFalse(result.is_valid)
        self.assertIn("too low", result.error_message.lower())

    def test_above_maximum(self):
        """Weight above maximum should fail with 'too high' message."""
        result = InputValidator.validate_weight("301")
        self.assertFalse(result.is_valid)
        self.assertIn("too high", result.error_message.lower())

    def test_zero_weight(self):
        """Zero weight should fail validation (below minimum)."""
        result = InputValidator.validate_weight("0")
        self.assertFalse(result.is_valid)

    def test_scientific_notation(self):
        """Scientific notation should be parsed correctly."""
        result = InputValidator.validate_weight("7e1")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 70.0)

    def test_result_is_validation_result(self):
        """validate_weight should return a ValidationResult."""
        result = InputValidator.validate_weight("70")
        self.assertIsInstance(result, ValidationResult)

    def test_result_is_frozen(self):
        """ValidationResult should be immutable."""
        result = InputValidator.validate_weight("70")
        with self.assertRaises(AttributeError):
            result.is_valid = False


class TestValidateHeight(unittest.TestCase):
    """Tests for InputValidator.validate_height()."""

    def test_valid_height(self):
        """A normal height string should validate successfully."""
        result = InputValidator.validate_height("1.75")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 1.75)
        self.assertEqual(result.error_message, "")

    def test_valid_height_integer_string(self):
        """An integer height string should validate."""
        result = InputValidator.validate_height("2")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 2.0)

    def test_valid_height_with_whitespace(self):
        """Height string with whitespace should validate."""
        result = InputValidator.validate_height("  1.80  ")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, 1.80)

    def test_valid_height_min_boundary(self):
        """Height at minimum boundary (0.5) should validate."""
        result = InputValidator.validate_height("0.5")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, HEIGHT_MIN)

    def test_valid_height_max_boundary(self):
        """Height at maximum boundary (3.0) should validate."""
        result = InputValidator.validate_height("3.0")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.value, HEIGHT_MAX)

    def test_empty_string(self):
        """Empty string should fail validation."""
        result = InputValidator.validate_height("")
        self.assertFalse(result.is_valid)
        self.assertEqual(result.value, 0.0)
        self.assertIn("empty", result.error_message.lower())

    def test_whitespace_only(self):
        """Whitespace-only string should fail validation."""
        result = InputValidator.validate_height("   ")
        self.assertFalse(result.is_valid)
        self.assertIn("empty", result.error_message.lower())

    def test_non_numeric(self):
        """Non-numeric string should fail validation."""
        result = InputValidator.validate_height("tall")
        self.assertFalse(result.is_valid)
        self.assertIn("numeric", result.error_message.lower())

    def test_negative_height(self):
        """Negative height should fail validation."""
        result = InputValidator.validate_height("-1.75")
        self.assertFalse(result.is_valid)
        self.assertIn("negative", result.error_message.lower())

    def test_below_minimum(self):
        """Height below minimum should fail with 'too low' message."""
        result = InputValidator.validate_height("0.4")
        self.assertFalse(result.is_valid)
        self.assertIn("too low", result.error_message.lower())

    def test_above_maximum(self):
        """Height above maximum should fail with 'too high' message."""
        result = InputValidator.validate_height("3.1")
        self.assertFalse(result.is_valid)
        self.assertIn("too high", result.error_message.lower())

    def test_zero_height(self):
        """Zero height should fail validation (below minimum)."""
        result = InputValidator.validate_height("0")
        self.assertFalse(result.is_valid)

    def test_result_is_validation_result(self):
        """validate_height should return a ValidationResult."""
        result = InputValidator.validate_height("1.75")
        self.assertIsInstance(result, ValidationResult)

    def test_result_is_frozen(self):
        """ValidationResult should be immutable."""
        result = InputValidator.validate_height("1.75")
        with self.assertRaises(AttributeError):
            result.is_valid = False

    def test_error_message_contains_invalid_value(self):
        """Error message for non-numeric input should include the bad value."""
        result = InputValidator.validate_height("abc")
        self.assertIn("abc", result.error_message)

    def test_error_message_contains_range_info_for_below_min(self):
        """Error message for below-min height should mention the minimum."""
        result = InputValidator.validate_height("0.1")
        self.assertIn(str(HEIGHT_MIN), result.error_message)

    def test_error_message_contains_range_info_for_above_max(self):
        """Error message for above-max height should mention the maximum."""
        result = InputValidator.validate_height("5.0")
        self.assertIn(str(HEIGHT_MAX), result.error_message)


if __name__ == "__main__":
    unittest.main()