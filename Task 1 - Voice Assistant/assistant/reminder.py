"""
Reminder Module

This module handles setting voice-triggered reminders using threading.
Reminders fire in a background thread while the assistant stays responsive.

Author: Mohit Pandey
Version: 1.0
"""

import threading
import speech_recognition as sr

from assistant.speaker import speak
from assistant.listener import listen


_reminder_active = False


def set_reminder() -> None:
    """
    Set a voice-triggered reminder using a background thread.
    """
    global _reminder_active
    if _reminder_active:
        speak("You already have an active reminder. Please wait for it to complete.")
        return

    speak("What should I remind you about?")
    message = listen()
    if not message:
        speak("I didn't catch that. Please try again.")
        return

    speak("In how many minutes?")
    try:
        minutes_input = listen()
        minutes = int(minutes_input)
        if minutes <= 0:
            raise ValueError("Time must be positive")
    except ValueError:
        speak("Sorry, I need a valid number of minutes.")
        return
    except sr.WaitTimeoutError:
        speak("I didn't catch that. Please try again.")
        return

    speak(f"Reminder set for {minutes} minutes from now.")
    _reminder_active = True

    def reminder_callback():
        global _reminder_active
        speak(f"Reminder: {message}")
        _reminder_active = False

    timer = threading.Timer(minutes * 60, reminder_callback)
    timer.start()
