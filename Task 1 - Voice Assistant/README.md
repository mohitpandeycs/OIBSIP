# Voice Assistant

A Python-based voice assistant for the **Oasis Infobyte** Python internship. It listens for spoken commands, routes them with simple keyword matching, and responds with **text-to-speech** (pyttsx3) plus optional browser or API actions.

## Features

### Beginner (required)

| Feature | Example phrases |
|---------|-----------------|
| Greetings | “Hello”, “Hi”, “Good morning” |
| Time / date | “What time is it?”, “What’s today’s date?” |
| Web search | “Search for …”, “On Google search for …”, “Open Google and search …” |

### Advanced (3+)

| Feature | Notes |
|---------|--------|
| **Weather** | OpenWeatherMap — “Weather in Mumbai”, “Tell me weather of Delhi” |
| **Wikipedia** | “What is …”, “Tell me about …”, “Who is …” |
| **Reminders** | “Set a reminder”, “Remind me …” |
| **Custom commands** | JSON file `custom_commands.json` — trigger substring → spoken response |

Speech recognition uses **Google Web Speech API** (requires internet). TTS is **offline** (pyttsx3).

## Tech stack

Python 3.10+ · `SpeechRecognition` · `PyAudio` · `pyttsx3` · `requests` · `wikipedia` · `python-dotenv`

## Project structure

```
Task 1 - Voice Assistant/
├── main.py                 # Entry: listen loop + route commands
├── assistant/
│   ├── __init__.py
│   ├── __main__.py         # Alternate: python -m assistant
│   ├── listener.py         # STT (microphone → text)
│   ├── speaker.py          # TTS (pyttsx3)
│   ├── commands.py         # Command router + web search
│   ├── weather.py          # OpenWeatherMap
│   ├── knowledge.py        # Wikipedia summaries
│   └── reminder.py         # Threading-based reminders
├── requirements.txt
├── .gitignore
└── README.md

```

## Quick start

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd "Task 1 - Voice Assistant"
```

### 2. Virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

On **Windows**, if `PyAudio` fails to build, install a matching wheel from [Christoph Gohlke’s archives](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) or use `pip install pipwin` then `pipwin install pyaudio`.

### 4. Environment variables

```bash
copy .env.example .env
```

Edit `.env` and set:

| Variable | Required for | Get it from |
|----------|----------------|-------------|
| `OPENWEATHER_API_KEY` | Weather commands | [OpenWeatherMap API](https://openweathermap.org/api) (free tier available) |

### 5. Run

From the folder that contains `main.py`:

```bash
python main.py
```

Or:

```bash
python -m assistant
```

Speak after the welcome message. Say **exit**, **quit**, **bye**, or **goodbye** to stop.

## Usage tips

- **Microphone:** Allow Python/your terminal to use the mic; reduce background noise.
- **Web search:** The assistant speaks a short line (e.g. “Searching on Google for …”) then opens your default browser.
- **Weather without a city in the phrase** may prompt for the city via a second listen.
- **Stale behavior after editing code (Windows):** `main.py` clears `assistant/__pycache__` on startup; if issues persist, delete `assistant/__pycache__` manually once.

## Testing

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Covers routing order (Google vs Wikipedia), search query cleanup, and voice-meta phrases.

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| No speech recognized | Check mic permissions, internet (Google STT), speak clearly after “Listening…” |
| “Listening timed out…” | Start speaking within the listen window; speak louder or closer to the mic |
| Weather always says not configured | Add `OPENWEATHER_API_KEY` to `.env` (not `.env.example`) |
| TTS silent but text prints | Windows: check default playback device; try updating / reinstalling pyttsx3 |
| Import / old code behavior | Run from project root; use `python main.py` or `python -m assistant`; remove `assistant/__pycache__` |

## Phase status (internship)

| Phase | Scope | Status |
|-------|--------|--------|
| 1 | Setup, STT, TTS | Complete |
| 2 | Greetings, time/date, web search | Complete |
| 3 | Weather, Wikipedia, reminders, custom JSON | Complete |
| 4 | Error handling, tests, documentation | **Complete** |

## Author

Mohit Pandey

## License

MIT License
