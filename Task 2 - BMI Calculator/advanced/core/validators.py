"""Input validation module for BMI Calculator.

Provides the InputValidator class with static methods for validating
weight and height inputs, returning ValidationResult objects with
clear error messages.
"""

from dataclasses import dataclass


# ── Validation Range Constants ──────────────────────────────────────────────

WEIGHT_MIN: float = 20.0
WEIGHT_MAX: float = 300.0
HEIGHT_MIN: float = 0.5
HEIGHT_MAX: float = 3.0


# ── Data Structures ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ValidationResult:
    """Immutable result of an input validation check.

    Attributes:
        is_valid: Whether the input passed validation.
        value: The validated and converted float value (0.0 if invalid).
        error_message: Human-readable error description (empty string if valid).
    """
    is_valid: bool
    value: float
    error_message: str


# ── Input Validator ──────────────────────────────────────────────────────────

class InputValidator:
    """Static utility class for validating user inputs.

    Centralizes all input validation rules and error message generation.
    No instance state is maintained.
    """

    @staticmethod
    def validate_weight(input_str: str) -> ValidationResult:
        """Validate a weight input string.

        Parses the string to a float and checks that it falls within
        the acceptable weight range (20–300 kg).

        Args:
            input_str: Raw user input string representing weight in kg.

        Returns:
            A ValidationResult indicating success or failure with an
            appropriate error message.
        """
        if not input_str or not input_str.strip():
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message="Weight cannot be empty. Please enter a value.",
            )

        try:
            value = float(input_str.strip())
        except ValueError:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message=(
                    f"Invalid weight: '{input_str.strip()}'. "
                    "Please enter a numeric value."
                ),
            )

        if value < 0:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message="Weight cannot be negative. Please enter a positive value.",
            )

        if value < WEIGHT_MIN:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message=(
                    f"Weight {value} kg is too low. "
                    f"Please enter a value of at least {WEIGHT_MIN} kg."
                ),
            )

        if value > WEIGHT_MAX:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message=(
                    f"Weight {value} kg is too high. "
                    f"Please enter a value of at most {WEIGHT_MAX} kg."
                ),
            )

        return ValidationResult(is_valid=True, value=value, error_message="")

    @staticmethod
    def validate_height(input_str: str) -> ValidationResult:
        """Validate a height input string.

        Parses the string to a float and checks that it falls within
        the acceptable height range (0.5–3.0 m).

        Args:
            input_str: Raw user input string representing height in meters.

        Returns:
            A ValidationResult indicating success or failure with an
            appropriate error message.
        """
        if not input_str or not input_str.strip():
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message="Height cannot be empty. Please enter a value.",
            )

        try:
            value = float(input_str.strip())
        except ValueError:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message=(
                    f"Invalid height: '{input_str.strip()}'. "
                    "Please enter a numeric value."
                ),
            )

        if value < 0:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message="Height cannot be negative. Please enter a positive value.",
            )

        if value < HEIGHT_MIN:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message=(
                    f"Height {value} m is too low. "
                    f"Please enter a value of at least {HEIGHT_MIN} m."
                ),
            )

        if value > HEIGHT_MAX:
            return ValidationResult(
                is_valid=False,
                value=0.0,
                error_message=(
                    f"Height {value} m is too high. "
                    f"Please enter a value of at most {HEIGHT_MAX} m."
                ),
            )

        return ValidationResult(is_valid=True, value=value, error_message="")