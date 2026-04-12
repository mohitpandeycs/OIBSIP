"""Core BMI calculation and classification engine.

Provides the BMIEngine class with static methods for computing BMI
and classifying results into WHO categories.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


# ── BMI Category Constants ──────────────────────────────────────────────────

class BMICategory:
    """WHO BMI category constants."""
    UNDERWEIGHT: str = "Underweight"
    NORMAL: str = "Normal"
    OVERWEIGHT: str = "Overweight"
    OBESE: str = "Obese"


# ── Category Explanations ───────────────────────────────────────────────────

_CATEGORY_EXPLANATIONS: dict[str, str] = {
    BMICategory.UNDERWEIGHT: (
        "Your BMI indicates that you are underweight. "
        "Consider consulting a healthcare professional about "
        "achieving a healthier weight."
    ),
    BMICategory.NORMAL: (
        "Your BMI is within the normal range. "
        "Maintain a balanced diet and regular physical activity "
        "to stay in this healthy range."
    ),
    BMICategory.OVERWEIGHT: (
        "Your BMI indicates that you are overweight. "
        "Consider adopting healthier eating habits and increasing "
        "physical activity."
    ),
    BMICategory.OBESE: (
        "Your BMI indicates obesity. "
        "It is recommended to consult a healthcare professional "
        "for guidance on weight management."
    ),
}


# ── Data Structures ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class BMIResult:
    """Immutable result of a BMI calculation.

    Attributes:
        bmi: Calculated BMI value rounded to 2 decimal places.
        category: WHO category string (Underweight, Normal, Overweight, Obese).
        explanation: Brief interpretation of the category.
    """
    bmi: float
    category: str
    explanation: str


# ── BMI Engine ──────────────────────────────────────────────────────────────

class BMIEngine:
    """Static utility class for BMI calculation and classification.

    Provides the shared calculation logic used by both the CLI and GUI
    versions of the application. No instance state is maintained.
    """

    @staticmethod
    def calculate_bmi(weight_kg: float, height_m: float) -> float:
        """Compute BMI using the formula weight(kg) / height(m)².

        Args:
            weight_kg: Weight in kilograms.
            height_m: Height in meters.

        Returns:
            BMI value rounded to 2 decimal places.

        Raises:
            ValueError: If height_m is zero or negative.
            TypeError: If inputs are not numeric.
        """
        if not isinstance(weight_kg, (int, float)):
            raise TypeError(f"Weight must be a number, got {type(weight_kg).__name__}")
        if not isinstance(height_m, (int, float)):
            raise TypeError(f"Height must be a number, got {type(height_m).__name__}")
        if height_m <= 0:
            raise ValueError("Height must be greater than zero for BMI calculation.")
        if weight_kg < 0:
            raise ValueError("Weight cannot be negative.")

        bmi = weight_kg / (height_m ** 2)
        return float(Decimal(str(bmi)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    @staticmethod
    def classify_bmi(bmi: float) -> BMIResult:
        """Classify a BMI value into a WHO category.

        Args:
            bmi: The calculated BMI value.

        Returns:
            A BMIResult dataclass with the BMI, category, and explanation.

        Raises:
            TypeError: If bmi is not numeric.
        """
        if not isinstance(bmi, (int, float)):
            raise TypeError(f"BMI must be a number, got {type(bmi).__name__}")

        if bmi < 18.5:
            category = BMICategory.UNDERWEIGHT
        elif bmi < 25.0:
            category = BMICategory.NORMAL
        elif bmi < 30.0:
            category = BMICategory.OVERWEIGHT
        else:
            category = BMICategory.OBESE

        explanation = _CATEGORY_EXPLANATIONS[category]
        return BMIResult(
            bmi=float(Decimal(str(bmi)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            category=category,
            explanation=explanation,
        )
