"""
Voice Assistant - Main Entry Point

This is the main entry point for the Voice Assistant application.
It starts the continuous listen loop and routes commands to appropriate handlers.

Author: Mohit Pandey
Version: 1.0
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True

# Clear cached bytecode so edits under assistant/ always load (helps on some Windows setups).
_root = Path(__file__).resolve().parent
for _pkg in ("assistant",):
    _pyc = _root / _pkg / "__pycache__"
    if _pyc.is_dir():
        for _f in _pyc.glob("*.pyc"):
            try:
                _f.unlink()
            except OSError:
                pass

import speech_recognition as sr

from assistant.commands import route
from assistant.listener import listen
from assistant.speaker import speak


def main():
    """
    Main function that starts the voice assistant.
    """
    speak("Welcome. I'm your voice assistant. Speak whenever you're ready.")

    while True:
        try:
            print("\n" + "=" * 50)
            print("Waiting for your command...")

            try:
                command = listen()
            except sr.WaitTimeoutError:
                speak("I did not hear you start speaking in time. Please try again.")
                continue

            if not command:
                # Listener already speaks on repeated STT failure; avoid duplicate prompts.
                continue

            print(f"Got command: {command}")
            result = route(command)

            if result == "exit":
                break
            elif result:
                print("Command processed successfully.")

        except KeyboardInterrupt:
            speak("Goodbye! Have a nice day!")
            break
        except Exception as e:
            err = str(e).lower()
            if "listening timed out" in err or "waiting for phrase" in err:
                speak("I did not hear you start speaking in time. Please try again.")
                continue
            print(f"Main loop error: {e}")
            speak("An error occurred. Please try again.")


if __name__ == "__main__":
    main()
