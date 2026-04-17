MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 128

def validate_inputs(
    length: int,
    use_uppercase: bool,
    use_lowercase: bool,
    use_digits: bool,
    use_symbols: bool
) -> None:
    if not isinstance(length, int):
        raise ValueError("Length must be an integer.")
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError("Password length must be at least 4.")
    if length > MAX_PASSWORD_LENGTH:
        raise ValueError("Password length cannot exceed 128.")
    if not (use_uppercase or use_lowercase or use_digits or use_symbols):
        raise ValueError("At least one character type must be selected.")