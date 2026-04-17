import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generator.validator import validate_inputs

class TestValidator(unittest.TestCase):
    def test_valid_inputs(self):
        try:
            validate_inputs(8, True, True, True, True)
        except ValueError:
            self.fail("validate_inputs raised ValueError unexpectedly!")

    def test_invalid_length_type(self):
        with self.assertRaises(ValueError) as context:
            validate_inputs("eight", True, True, True, True)
        self.assertEqual(str(context.exception), "Length must be an integer.")

    def test_length_too_short(self):
        with self.assertRaises(ValueError) as context:
            validate_inputs(3, True, True, True, True)
        self.assertEqual(str(context.exception), "Password length must be at least 4.")

    def test_length_too_long(self):
        with self.assertRaises(ValueError) as context:
            validate_inputs(129, True, True, True, True)
        self.assertEqual(str(context.exception), "Password length cannot exceed 128.")

    def test_no_character_types_selected(self):
        with self.assertRaises(ValueError) as context:
            validate_inputs(8, False, False, False, False)
        self.assertEqual(str(context.exception), "At least one character type must be selected.")

if __name__ == "__main__":
    unittest.main()