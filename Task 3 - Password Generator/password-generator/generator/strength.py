import math
from generator.core import CHARSET_UPPERCASE, CHARSET_LOWERCASE, CHARSET_DIGITS, CHARSET_SYMBOLS

def calculate_strength(password: str) -> dict:
    score = 0
    if len(password) >= 8:
        score += 10
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10
    if len(password) >= 20:
        score += 10
    if any(c in CHARSET_UPPERCASE for c in password):
        score += 10
    if any(c in CHARSET_LOWERCASE for c in password):
        score += 10
    if any(c in CHARSET_DIGITS for c in password):
        score += 10
    if any(c in CHARSET_SYMBOLS for c in password):
        score += 10
    if all(any(c in charset for c in password) for charset in [CHARSET_UPPERCASE, CHARSET_LOWERCASE, CHARSET_DIGITS, CHARSET_SYMBOLS]):
        score += 10
    if all(password.count(c) <= 2 for c in password):
        score += 10

    label, color = get_strength_label_and_color(score)
    entropy = _calculate_entropy(password)

    return {
        "score": score,
        "label": label,
        "color": color,
        "entropy": entropy
    }

def _calculate_entropy(password: str) -> float:
    pool_size = 0
    if any(c in CHARSET_UPPERCASE for c in password):
        pool_size += 26
    if any(c in CHARSET_LOWERCASE for c in password):
        pool_size += 26
    if any(c in CHARSET_DIGITS for c in password):
        pool_size += 10
    if any(c in CHARSET_SYMBOLS for c in password):
        pool_size += 25
    if pool_size == 0:
        return 0.0
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

def get_strength_label_and_color(score: int) -> tuple:
    if score <= 19:
        return "Very Weak", "#DC2626"
    elif score <= 39:
        return "Weak", "#EA580C"
    elif score <= 59:
        return "Fair", "#D97706"
    elif score <= 79:
        return "Strong", "#16A34A"
    else:
        return "Very Strong", "#15803D"