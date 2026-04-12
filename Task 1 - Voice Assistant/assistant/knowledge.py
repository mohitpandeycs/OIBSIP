"""
Wikipedia Knowledge Module

This module handles searching Wikipedia for general knowledge Q&A.
No API key required - uses the wikipedia library.

Author: Mohit Pandey
Version: 1.0
"""

import wikipedia

from assistant.speaker import speak


def search_wikipedia(command: str) -> None:
    """
    Search Wikipedia and speak a 2-sentence summary.

    Args:
        command (str): Voice command containing the topic to search.
    """
    topic = (
        command.replace("tell me about", "")
        .replace("who is", "")
        .replace("what is", "")
        .strip()
    )
    if not topic:
        speak("What topic would you like to know about?")
        return

    try:
        result = wikipedia.summary(topic, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("That topic is a bit ambiguous. Can you be more specific?")
        print(f"DisambiguationError: {topic}")
    except wikipedia.exceptions.PageError:
        speak(f"I couldn't find any information on {topic}.")
        print(f"PageError: {topic} not found")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        print(f"Wikipedia error: {e}")
