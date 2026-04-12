"""
Speech Recognition Module (STT)

This module handles capturing voice input from the microphone and
transcribing it to text using Google Web Speech API.

Author: Mohit Pandey
Version: 1.0
"""

import speech_recognition as sr


def listen() -> str:
    """
    Listen to microphone input and return transcribed text.
    Uses multiple attempts with different thresholds.

    Returns:
        str: Transcribed command in lowercase, or empty string on failure.

    Outer wrapper: any phrase-start timeout that still propagates is converted
    to a spoken prompt and an empty string (never bubbles to main as an error).
    """
    from assistant.speaker import speak

    try:
        return _listen_impl()
    except sr.WaitTimeoutError:
        speak("I did not hear you start speaking in time. Please try again.")
        return ""
    except Exception as e:
        err = str(e).lower()
        if "listening timed out" in err or "waiting for phrase" in err:
            speak("I did not hear you start speaking in time. Please try again.")
            return ""
        raise


def _listen_impl() -> str:
    """Core listen loop."""
    from assistant.speaker import speak

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    for n in range(3):
        try:
            print("Listening...")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=12, phrase_time_limit=15)

            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")

            if len(command) >= 2:
                return command

        except sr.WaitTimeoutError:
            if n < 2:
                print("No speech detected, trying again...")
                continue
            speak("I didn't hear anything. Please try again.")
            return ""
        except sr.UnknownValueError:
            if n < 2:
                print("Didn't understand, trying again...")
                continue
            speak("I didn't catch that. Please try again.")
            return ""
        except sr.RequestError as e:
            speak("Speech service is unavailable.")
            print(f"STT RequestError: {e}")
            return ""
        except Exception as e:
            print(f"Listen error: {e}")
            speak("Something went wrong while listening. Please try again.")
            return ""

    return ""
