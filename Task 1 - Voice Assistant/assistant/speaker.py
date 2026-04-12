"""
Text-to-Speech Module (TTS)

This module handles converting text to speech using pyttsx3.
pyttsx3 is fully offline, free, and requires no API keys.

Author: Mohit Pandey
Version: 1.0
"""

import sys

import pyttsx3

_RATE = 175
_VOLUME = 1.0


def _configure_engine(eng: pyttsx3.Engine) -> None:
    eng.setProperty("rate", _RATE)
    eng.setProperty("volume", _VOLUME)
    voices = eng.getProperty("voices") or []
    for v in voices:
        _name = getattr(v, "name", "") or ""
        if "english" in _name.lower() or "en-" in str(getattr(v, "id", "")).lower():
            eng.setProperty("voice", v.id)
            break


# Non-Windows: reuse one engine (stable on many platforms).
engine = None
if sys.platform != "win32":
    engine = pyttsx3.init()
    _configure_engine(engine)


def speak(text: str) -> None:
    """
    Convert text to speech using pyttsx3 offline engine.
    Every user-facing assistant reply should go through this function
    so it is both printed and spoken aloud.

    On Windows, a new engine is created per utterance — avoids stuck COM/SAPI
    state where runAndWait returns but nothing is heard (terminal still prints).

    Args:
        text (str): The response string to speak aloud.
    """
    utterance = (text or "").strip()
    if not utterance:
        return
    print(f"Assistant: {utterance}")
    try:
        if sys.platform == "win32":
            # SpeechRecognition / SAPI often share COM; re-init per utterance after STT.
            try:
                import pythoncom  # type: ignore[import-not-found]

                try:
                    pythoncom.CoInitialize()
                except Exception:
                    pass
            except ImportError:
                pass
            eng = pyttsx3.init()
            _configure_engine(eng)
            eng.say(utterance)
            eng.runAndWait()
        else:
            assert engine is not None
            engine.say(utterance)
            engine.runAndWait()
    except Exception as e:
        print(f"TTS error (text was shown above): {e}")

