import secrets
from string import ascii_uppercase as CHARSET_UPPERCASE, ascii_lowercase as CHARSET_LOWERCASE, digits as CHARSET_DIGITS
CHARSET_SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
from generator.validator import validate_inputs

def generate_password(
    length: int,
    use_uppercase: bool,
    use_lowercase: bool,
    use_digits: bool,
    use_symbols: bool,
    excluded_chars: str = ""
) -> str:
    validate_inputs(length, use_uppercase, use_lowercase, use_digits, use_symbols)

    pool = ""
    if use_uppercase:
        pool += CHARSET_UPPERCASE
    if use_lowercase:
        pool += CHARSET_LOWERCASE
    if use_digits:
        pool += CHARSET_DIGITS
    if use_symbols:
        pool += CHARSET_SYMBOLS

    for char in excluded_chars:
        pool = pool.replace(char, "")

    if not pool:
        raise ValueError("No characters available after applying exclusions.")

    guaranteed = []
    if use_uppercase and any(c in CHARSET_UPPERCASE for c in pool):
        guaranteed.append(secrets.choice([c for c in CHARSET_UPPERCASE if c not in excluded_chars]))
    if use_lowercase and any(c in CHARSET_LOWERCASE for c in pool):
        guaranteed.append(secrets.choice([c for c in CHARSET_LOWERCASE if c not in excluded_chars]))
    if use_digits and any(c in CHARSET_DIGITS for c in pool):
        guaranteed.append(secrets.choice([c for c in CHARSET_DIGITS if c not in excluded_chars]))
    if use_symbols and any(c in CHARSET_SYMBOLS for c in pool):
        guaranteed.append(secrets.choice([c for c in CHARSET_SYMBOLS if c not in excluded_chars]))

    remainder = [secrets.choice(pool) for _ in range(length - len(guaranteed))]
    combined = guaranteed + remainder
    secrets.SystemRandom().shuffle(combined)

    return "".join(combined)

def generate_multiple(
    count: int,
    length: int,
    use_uppercase: bool,
    use_lowercase: bool,
    use_digits: bool,
    use_symbols: bool,
    excluded_chars: str = ""
) -> list[str]:
    if count < 1 or count > 10:
        raise ValueError("Count must be between 1 and 10.")
    return [generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols, excluded_chars) for _ in range(count)]