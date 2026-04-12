#!/usr/bin/env python3
"""BMI Calculator — Beginner Version (CLI)

A simple command-line BMI calculator that prompts for weight and height,
validates inputs, computes BMI using the WHO formula, classifies the
result into standard categories, and displays a formatted output with
an option to recalculate.

No external dependencies — standard library only.
"""

# ── Constants ───────────────────────────────────────────────────────────────

WEIGHT_MIN = 20.0
WEIGHT_MAX = 300.0
HEIGHT_MIN = 0.5
HEIGHT_MAX = 3.0

CATEGORY_UNDERWEIGHT = "Underweight"
CATEGORY_NORMAL = "Normal"
CATEGORY_OVERWEIGHT = "Overweight"
CATEGORY_OBESE = "Obese"

CATEGORY_EXPLANATIONS = {
    CATEGORY_UNDERWEIGHT: (
        "Your BMI indicates that you are underweight. "
        "Consider consulting a healthcare professional about "
        "achieving a healthier weight."
    ),
    CATEGORY_NORMAL: (
        "Your BMI is within the normal range. "
        "Maintain a balanced diet and regular physical activity "
        "to stay in this healthy range."
    ),
    CATEGORY_OVERWEIGHT: (
        "Your BMI indicates that you are overweight. "
        "Consider adopting healthier eating habits and increasing "
        "physical activity."
    ),
    CATEGORY_OBESE: (
        "Your BMI indicates obesity. "
        "It is recommended to consult a healthcare professional "
        "for guidance on weight management."
    ),
}


# ── Core Logic ──────────────────────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Compute BMI using the formula weight(kg) / height(m)².

    Args:
        weight_kg: Weight in kilograms.
        height_m: Height in meters.

    Returns:
        BMI value rounded to 2 decimal places.

    Raises:
        ValueError: If height_m is zero or negative.
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero for BMI calculation.")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> tuple[str, str]:
    """Classify a BMI value into a WHO category.

    Args:
        bmi: The calculated BMI value.

    Returns:
        A tuple of (category, explanation).
    """
    if bmi < 18.5:
        category = CATEGORY_UNDERWEIGHT
    elif bmi < 25.0:
        category = CATEGORY_NORMAL
    elif bmi < 30.0:
        category = CATEGORY_OVERWEIGHT
    else:
        category = CATEGORY_OBESE

    return category, CATEGORY_EXPLANATIONS[category]


# ── Input Validation ────────────────────────────────────────────────────────

def validate_weight(input_str: str) -> tuple[bool, float, str]:
    """Validate a weight input string.

    Args:
        input_str: Raw user input string.

    Returns:
        A tuple of (is_valid, value, error_message).
    """
    if not input_str or not input_str.strip():
        return False, 0.0, "Weight cannot be empty. Please enter a value."

    try:
        value = float(input_str.strip())
    except ValueError:
        return False, 0.0, f"Invalid weight: '{input_str.strip()}'. Please enter a numeric value."

    if value < 0:
        return False, 0.0, "Weight cannot be negative. Please enter a positive value."
    if value < WEIGHT_MIN:
        return False, 0.0, f"Weight {value} kg is too low. Please enter at least {WEIGHT_MIN} kg."
    if value > WEIGHT_MAX:
        return False, 0.0, f"Weight {value} kg is too high. Please enter at most {WEIGHT_MAX} kg."

    return True, value, ""


def validate_height(input_str: str) -> tuple[bool, float, str]:
    """Validate a height input string.

    Args:
        input_str: Raw user input string.

    Returns:
        A tuple of (is_valid, value, error_message).
    """
    if not input_str or not input_str.strip():
        return False, 0.0, "Height cannot be empty. Please enter a value."

    try:
        value = float(input_str.strip())
    except ValueError:
        return False, 0.0, f"Invalid height: '{input_str.strip()}'. Please enter a numeric value."

    if value < 0:
        return False, 0.0, "Height cannot be negative. Please enter a positive value."
    if value < HEIGHT_MIN:
        return False, 0.0, f"Height {value} m is too low. Please enter at least {HEIGHT_MIN} m."
    if value > HEIGHT_MAX:
        return False, 0.0, f"Height {value} m is too high. Please enter at most {HEIGHT_MAX} m."

    return True, value, ""


# ── Display Helpers ──────────────────────────────────────────────────────────

def display_welcome() -> None:
    """Print the welcome message."""
    print()
    print("=" * 55)
    print("       BMI CALCULATOR — Body Mass Index Tool")
    print("=" * 55)
    print()
    print("  Calculate your BMI and find out your weight category")
    print("  based on World Health Organization (WHO) standards.")
    print()
    print("  Valid ranges:")
    print(f"    • Weight: {WEIGHT_MIN}–{WEIGHT_MAX} kg")
    print(f"    • Height: {HEIGHT_MIN}–{HEIGHT_MAX} m")
    print()
    print("-" * 55)


def display_result(bmi: float, category: str, explanation: str) -> None:
    """Print the BMI result in a formatted display.

    Args:
        bmi: Calculated BMI value.
        category: WHO category string.
        explanation: Brief interpretation of the category.
    """
    print()
    print("─" * 45)
    print("  RESULT")
    print("─" * 45)
    print(f"    BMI:       {bmi}")
    print(f"    Category:  {category}")
    print()
    print(f"  {explanation}")
    print("─" * 45)


def display_category_chart() -> None:
    """Print a quick-reference BMI category chart."""
    print()
    print("  BMI Category Reference (WHO):")
    print("  ┌─────────────┬───────────────────┐")
    print("  │ Category     │ BMI Range         │")
    print("  ├─────────────┼───────────────────┤")
    print("  │ Underweight  │ Less than 18.5    │")
    print("  │ Normal       │ 18.5 – 24.9       │")
    print("  │ Overweight   │ 25.0 – 29.9       │")
    print("  │ Obese        │ 30.0 or greater   │")
    print("  └─────────────┴───────────────────┘")


# ── Main Application ────────────────────────────────────────────────────────

def run_cli() -> None:
    """Main function for the CLI BMI Calculator.

    Contains the full workflow: welcome, input loop with validation,
    BMI calculation, result display, and recalculate prompt.
    """
    display_welcome()

    while True:
        # ── Get Weight ───────────────────────────────────────────────────
        while True:
            print()
            weight_input = input("  Enter your weight (kg): ").strip()
            is_valid, weight, error = validate_weight(weight_input)
            if is_valid:
                break
            print(f"  ✗ {error}")

        # ── Get Height ───────────────────────────────────────────────────
        while True:
            height_input = input("  Enter your height (m): ").strip()
            is_valid, height, error = validate_height(height_input)
            if is_valid:
                break
            print(f"  ✗ {error}")

        # ── Calculate & Display ──────────────────────────────────────────
        bmi = calculate_bmi(weight, height)
        category, explanation = classify_bmi(bmi)
        display_result(bmi, category, explanation)
        display_category_chart()

        # ── Recalculate Prompt ───────────────────────────────────────────
        print()
        another = input("  Calculate again? (y/n): ").strip().lower()
        if another not in ("y", "yes"):
            print()
            print("  Thank you for using the BMI Calculator. Stay healthy!")
            print()
            break

    print("=" * 55)


# ── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_cli()