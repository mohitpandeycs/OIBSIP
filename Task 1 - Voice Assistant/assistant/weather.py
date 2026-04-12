"""
Weather Module

This module handles fetching weather data from OpenWeatherMap API.
It provides current temperature, weather description, and humidity.

Author: Mohit Pandey
Version: 1.0
"""

import requests
import os
from dotenv import load_dotenv

from assistant.speaker import speak


load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(command: str) -> None:
    """
    Fetch and speak current weather for a city extracted from the command.

    Args:
        command (str): Full voice command string containing city name.
    """
    if not WEATHER_API_KEY:
        speak("This feature isn't configured. Check your .env file.")
        print("Missing WEATHER_API_KEY in .env")
        return

    # Try to extract city from various formats
    city = None

    # Try different patterns
    if "in " in command:
        city = command.split("in ")[-1].strip()
    elif "at " in command:
        city = command.split("at ")[-1].strip()
    elif "of " in command:
        city = command.split("of ")[-1].strip()
    else:
        # Get everything after "weather"
        parts = command.replace("weather", "").strip()
        if parts:
            city = parts.strip()

    if not city:
        # Ask user for city - try to get it from listening
        speak("Which city? Please say the city name.")
        from assistant.listener import listen

        city = listen()
        if not city:
            speak("I didn't catch that. Please try again.")
            return

    # Clean up the city name
    city = city.strip()

    try:
        params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        speak(f"In {city}, it is {temp}°C with {desc}. Humidity is {humidity}%.")
        print(f"Weather: {city} - {temp}°C, {desc}")
    except requests.exceptions.HTTPError:
        speak(f"I couldn't find weather data for {city}. Try another city.")
        print(f"Weather error: City not found - {city}")
    except requests.exceptions.ConnectionError:
        speak("I need an internet connection to check the weather.")
        print("Network error: No internet connection")
    except requests.exceptions.Timeout:
        speak("The weather request timed out. Please try again.")
        print("Timeout: Weather API request timed out")
    except Exception as e:
        speak("An error occurred while fetching weather data.")
        print(f"Weather error: {e}")
