"""
Command Router Module

This module routes voice commands to the appropriate handler functions.
It implements keyword matching to determine which feature to execute.

Priority Order:
1. Custom user-defined commands (loaded from custom_commands.json if exists)
2. Exit commands (goodbye, bye, quit, exit)
3. Weather (weather in, what's the weather)
4. Reminder (remind me, set a reminder, set reminder)
5. Web search / Google — before time/date/Wikipedia so phrases like
   "open Google … today's IPL …" are not captured by the date or wiki rules
6. Time query (what time, current time, tell me the time)
7. Date query (what date, today's date, what day)
8. Wikipedia Q&A (tell me about, who is, what is)
9. Greetings (hello, hi, hey, how are you, your name)
10. Unknown response

Author: Mohit Pandey
Version: 1.0
"""

import json
import os
import re
import threading
import urllib.parse
import webbrowser
from datetime import datetime

from assistant.knowledge import search_wikipedia
from assistant.reminder import set_reminder
from assistant.speaker import speak
from assistant.weather import get_weather

CUSTOM_COMMANDS_FILE = "custom_commands.json"


def load_custom_commands() -> dict:
    """
    Load custom user-defined commands from JSON file.

    Returns:
        dict: Dictionary of custom commands, or empty dict if file doesn't exist.
    """
    if os.path.exists(CUSTOM_COMMANDS_FILE):
        with open(CUSTOM_COMMANDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_custom_command(trigger: str, response: str) -> None:
    """
    Save a custom command to the JSON file.

    Args:
        trigger (str): The trigger phrase.
        response (str): The response to speak.
    """
    commands = load_custom_commands()
    commands[trigger] = response
    with open(CUSTOM_COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=4)


def _wants_web_search(command: str) -> bool:
    """
    True when the user clearly asked for a browser / Google search.

    Kept stricter than a bare word 'search' so phrases like
    'what is a search engine' still route to Wikipedia, not the browser.
    """
    c = command.lower().strip()
    if "open google" in c:
        return True
    if re.search(r"\bgoogle\b", c):
        return True
    if "search for" in c or "search on" in c:
        return True
    if c.startswith("search "):
        return True
    if re.search(r"\blook\s*up\b", c):
        return True
    if "dhoondh" in c:
        return True
    return False


def _wants_voice_explanation(cmd_lower: str) -> bool:
    """User is asking whether the assistant speaks / uses voice (not a domain command)."""
    # Any phrase that mentions *voice* plus responding / replying (covers most STT variants)
    if "voice" in cmd_lower and re.search(
        r"\b(respond|response|reply|answer|speak|say|talk)\b", cmd_lower
    ):
        return True
    if re.search(r"\b(respond|response|reply)\b.{0,80}\bvoice\b", cmd_lower) or re.search(
        r"\bvoice\b.{0,80}\b(respond|response|reply)\b", cmd_lower
    ):
        return True
    if "text to speech" in cmd_lower or re.search(r"\btts\b", cmd_lower):
        return True
    if "speak aloud" in cmd_lower or "out loud" in cmd_lower:
        return True
    # Truncated or informal STT (no word "voice")
    if "respond to my" in cmd_lower:
        return True
    if re.search(r"\b(can you|could you|will you)\s+(reply|respond)\b", cmd_lower):
        return True
    if "reply me" in cmd_lower or "respond me" in cmd_lower:
        return True
    if "read that" in cmd_lower and re.search(
        r"\b(can you|could you|will you|can not|cannot)\b", cmd_lower
    ):
        return True
    if "voice" not in cmd_lower:
        return False
    return any(
        w in cmd_lower
        for w in (
            "respond",
            "response",
            "answer",
            "speak",
            "talk",
            "read ",
            "with your",
            "use your",
            "in voice",
            "using voice",
            "use voice",
        )
    ) or bool(re.search(r"\bsay\b", cmd_lower))


def _extract_search_query(command: str) -> str:
    """Strip search / Google boilerplate and return the query for Google."""
    c = command.lower().strip()
    # Longest phrases first so shorter substrings do not win early.
    remove_phrases = sorted(
        [
            "open google and search for",
            "open google and search",
            "open google search for",
            "open google search",
            "on google search for",
            "search on google for",
            "search google for",
            "google and search for",
            "google and search",
            "on google search",
            "open google for",
            "open google",
            "google search for",
            "google search",
            "search for",
            "search",
            "look up",
            "dhoondh",
        ],
        key=len,
        reverse=True,
    )
    for phrase in remove_phrases:
        if phrase in c:
            c = c.replace(phrase, " ", 1)
    c = c.replace(",", " ")
    c = re.sub(r"\s+", " ", c).strip()
    return c


def route(command: str) -> bool | str:
    """
    Route the voice command to the appropriate handler.

    Args:
        command (str): The transcribed voice command.

    Returns:
        True if handled, False if not, or "exit" when the user quits.
    """
    print(f"Routing: {command}")

    if not command:
        return False

    cmd_lower = command.lower().strip()

    # Exit - check first
    if any(w in cmd_lower for w in ("exit", "quit", "bye", "goodbye", "stop")):
        speak("Goodbye. Have a productive day.")
        return "exit"

    # Custom commands (longest trigger first)
    custom = load_custom_commands()
    if custom:
        for trigger, response in sorted(custom.items(), key=lambda x: -len(str(x[0]))):
            trig = str(trigger).strip().lower()
            if not trig:
                continue
            if trig in cmd_lower:
                speak(str(response))
                return True

    # Voice / TTS meta — early so phrases like "respond with your voice" are not unknown
    if _wants_voice_explanation(cmd_lower):
        speak(
            "I use text-to-speech for every reply. Ask for the time, weather, "
            "a Wikipedia topic, or say search for followed by what you want to look up."
        )
        return True

    # Weather
    if any(w in cmd_lower for w in ("weather", "temperature", "mausam")):
        get_weather(command)
        return True

    # Reminder
    if any(w in cmd_lower for w in ("remind", "reminder", "yad")):
        set_reminder()
        return True

    # Web / Google search — before time/date/Wikipedia
    if _wants_web_search(cmd_lower):
        web_search(command)
        return True

    # Time
    if any(w in cmd_lower for w in ("time", "clock", "samay")):
        tell_time()
        return True

    # Date
    if any(w in cmd_lower for w in ("date", "today", "din", "taareekh")):
        tell_date()
        return True

    # Wikipedia
    if any(w in cmd_lower for w in ("about", "who is", "what is", "tell me")):
        search_wikipedia(command)
        return True

    # Small talk
    if "how are you" in cmd_lower:
        speak("I'm ready to help. What would you like to do?")
        return True
    if any(w in cmd_lower for w in ("your name", "who are you")):
        speak("I'm your voice assistant, here to handle commands and quick lookups.")
        return True

    # Greeting (word boundaries so "hi" does not match inside "this" / "ship")
    if any(x in cmd_lower for x in ("good morning", "good afternoon", "good evening")):
        greet()
        return True
    if re.search(r"\b(hello|hi|hey|namaste)\b", cmd_lower):
        greet()
        return True

    print(f"Unrecognized: {command}")
    speak(
        "I didn't recognize that command. For example, you can ask for the time, "
        "weather, a web search, or a Wikipedia topic."
    )
    return True


def greet() -> None:
    """Respond to greeting."""
    speak("Hello. I'm your voice assistant. How may I help you?")


def tell_time() -> None:
    """Tell the current time in 12-hour format."""
    now = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}.")


def tell_date() -> None:
    """Tell the current date in human-readable format."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today}.")


def web_search(command: str) -> None:
    """
    Open Google with the user's query and confirm aloud (TTS).

    Args:
        command (str): The voice command containing the search query.
    """
    query = _extract_search_query(command)
    if not query:
        speak("What would you like me to search for?")
        return

    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    # Spoken aloud in full (TTS) before opening the browser (browser in a thread
    # avoids Windows focus/CPU contention cutting off pyttsx3 audio).
    speak(f"Searching on Google for {query}.")

    def _open_browser() -> None:
        try:
            webbrowser.open(url)
        except OSError as e:
            print(f"Browser open error: {e}")

    threading.Thread(target=_open_browser, daemon=True).start()


def teach_custom_command() -> None:
    """Teach the assistant a new custom command."""
    from assistant.listener import listen

    speak("What should be the trigger phrase?")
    trigger = listen()
    if not trigger:
        speak("I didn't catch that. Please try again.")
        return

    speak(f"What should I say when you say {trigger}?")
    response = listen()
    if not response:
        speak("I didn't catch that. Please try again.")
        return

    save_custom_command(trigger, response)
    speak(f"Understood. When you say {trigger}, I'll respond with: {response}")
