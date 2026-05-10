# Py Voice Assistant

A modern, modular Python-based voice assistant that processes natural language commands with keyword matching, delivers intelligent responses via offline text-to-speech, and seamlessly integrates with external APIs and web services.

<p align="center">
  <a href="https://github.com/mohitpandeycs" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue" alt="MIT License" />
  </a>

  <a href="https://github.com/mohitpandeycs" target="_blank">
    <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome"/>
  </a>
</p>
<center>

 **• Voice-driven • Lightweight • Extensible**
</center>

## Overview
Voice Assistant provides a comprehensive hands-free interaction experience. Users simply speak commands, and the system intelligently routes requests to appropriate handlers—whether searching the web, fetching weather data, querying knowledge bases, or executing custom actions.

Core experience:

1. Speak a command naturally.
2. System recognizes and processes the intent.
3. Receive instant voice response with actions.

## Features

| Feature | Capability |
|---------|-----------|
| **Voice Commands** | Greetings, time/date queries, web search, custom voice triggers |
| **Weather Integration** | Real-time weather data via OpenWeatherMap API |
| **Knowledge Queries** | Instant Wikipedia summaries for "What is", "Who is" queries |
| **Smart Reminders** | Set and receive voice reminders at specified times |
| **Custom Commands** | JSON-based command mapping for extensibility |
| **Offline TTS** | Text-to-speech powered by pyttsx3 (no external dependencies) |

**Speech Recognition:** Google Web Speech API (internet required for accuracy)  
**Text-to-Speech:** pyttsx3 (completely offline)

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Speech Recognition** | SpeechRecognition + Google Web Speech API |
| **Text-to-Speech** | pyttsx3 |
| **Audio I/O** | PyAudio |
| **HTTP Requests** | requests |
| **Knowledge Base** | Wikipedia API |
| **Configuration** | python-dotenv |

## Project Structure

```
voice-assistant/
├── main.py                 # Entry point: listen loop and command routing
├── assistant/
│   ├── __init__.py
│   ├── __main__.py         # Module entry: python -m assistant
│   ├── listener.py         # Speech-to-text (microphone input)
│   ├── speaker.py          # Text-to-speech output (pyttsx3)
│   ├── commands.py         # Command router and web search handler
│   ├── weather.py          # OpenWeatherMap API integration
│   ├── knowledge.py        # Wikipedia knowledge retrieval
│   └── reminder.py         # Thread-based reminder scheduler
├── requirements.txt
├── .env.example            # Environment variable template
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Microphone input device
- Internet connection (for speech recognition and API calls)

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd voice-assistant
```

2. **Create virtual environment** (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**Note on Windows:** If `PyAudio` installation fails, download a precompiled wheel from [Christoph Gohlke's archives](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) matching your Python version, or use:

```bash
pip install pipwin
pipwin install pyaudio
```

### Configuration

1. **Create environment file**

```bash
copy .env.example .env
```

2. **Set required variables**

| Variable | Required For | Obtain From |
|----------|--------------|------------|
| `OPENWEATHER_API_KEY` | Weather commands | [OpenWeatherMap API](https://openweathermap.org/api) (free tier available) |

Example `.env`:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage

### Quick Start

Run the assistant from the project root:

```bash
python main.py
```

Or use the module entry point:

```bash
python -m assistant
```

Speak naturally after the welcome message. Exit with: **exit**, **quit**, **bye**, or **goodbye**.

### Example Commands

- "What time is it?"
- "Tell me the weather in London"
- "Search for machine learning on Google"
- "Who is Elon Musk?"
- "Set a reminder in 5 minutes"

### Tips

- **Microphone Setup:** Ensure your terminal/IDE has microphone permissions. Reduce background noise for better recognition.
- **Web Search:** After "Searching on Google...", your default browser opens with results.
- **Weather Queries:** If no city is mentioned, the system will ask for clarification.
- **Reminders:** Run in the foreground; reminders trigger via voice notification.
- **Cache Issues (Windows):** Stale imports are auto-cleared; manually delete `assistant/__pycache__` if needed.

## Testing

Run the test suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Tests cover:
- Command routing order (web search vs Wikipedia)
- Query cleanup and parsing
- Voice intent recognition

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No speech recognized | Check microphone permissions, internet connectivity, and speak clearly after "Listening…" |
| "Listening timed out" | Speak within the listen window or closer to microphone; speak louder |
| Weather not working | Verify `OPENWEATHER_API_KEY` is set in `.env` (not `.env.example`) |
| TTS silent on Windows | Check default playback device in system settings; reinstall pyttsx3 if needed |
| Stale behavior after code changes | Remove `assistant/__pycache__` directory and restart |
| Import errors | Run from project root using `python main.py` or `python -m assistant` |

## Performance Considerations

- **Offline Processing:** Text-to-speech runs entirely offline for instant responses.
- **API Calls:** Weather and Wikipedia queries are cached to minimize API usage.
- **Threading:** Reminders run on background threads without blocking the main listener loop.

## Future Enhancements

- Support for multiple languages
- Integration with smart home systems
- Advanced NLP for context-aware responses
- Voice command learning and personalization

## Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Connect With Me :)

Built and maintained by **[Mohit Pandey](https://github.com/mohitpandeycs)**

- GitHub — [@mohitpandeycs](https://github.com/mohitpandeycs)
- LinkedIn — [in/mohitpandeycs](https://linkedin.com/in/mohitpandeycs)
- Twitter / X — [@mohitpandeycs](https://x.com/mohitpandeycs)

## License

This project is released under the MIT License.


---

<p align="center">
  If you liked it, consider giving it a ⭐ — it helps other developers find the project.
</p>
