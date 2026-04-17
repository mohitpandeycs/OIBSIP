# Password Generator

A cryptographically secure password generator built with Python and Tkinter.

## Features
- Generate random, secure passwords based on user-defined criteria.
- Customize password length (4-128 characters).
- Include/exclude uppercase letters, lowercase letters, digits, and symbols.
- Exclude specific characters from the password.
- Display password strength with entropy calculation.
- Copy generated passwords to the clipboard.

## Tech Stack
- Python 3.10+
- Tkinter (built-in)
- secrets module (built-in)
- pyperclip

## Setup
```bash
git clone <repository-url>
cd password-generator
pip install -r requirements.txt
python main.py
```

## How to Use
1. Launch the application using `python main.py`.
2. Set the desired password length using the slider.
3. Select the character types to include (uppercase, lowercase, digits, symbols).
4. Optionally exclude specific characters.
5. Click "Generate Password" to create a password.
6. Copy the password to the clipboard using the "Copy" button.

## Security Notes
Passwords are generated using Python's `secrets` module, which uses the operating system's cryptographically secure random number generator. Generated passwords are never stored or logged.

## Author
**Mohit Pandey**