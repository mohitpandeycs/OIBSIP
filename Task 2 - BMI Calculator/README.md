# BMI Calculator

A two-version Body Mass Index (BMI) Calculator application built in Python as part of the **Oasis Infobyte Internship Program (OIBSIP)** — Task 2.

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Beginner Version (CLI)](#beginner-version-cli)
  - [Advanced Version (GUI)](#advanced-version-gui)
- [BMI Classification](#bmi-classification)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [License](#license)

---

## About

This project provides two versions of a BMI Calculator:

| Version | Interface | Persistence | Multi-User | Visualization |
|---------|-----------|-------------|------------|---------------|
| **Beginner** | Command-line (CLI) | None | No | None |
| **Advanced** | Tkinter GUI | SQLite | Yes | Matplotlib |

Both versions use the same core BMI engine and input validation logic, following the WHO (World Health Organization) BMI classification standards.

**BMI Formula:** `BMI = weight(kg) / height(m)²`

---

## Features

### Beginner Version
- 🖥️ Simple CLI interface
- ✅ Input validation (weight: 20–300 kg, height: 0.5–3.0 m)
- 📊 BMI calculation with WHO category classification
- 🔄 Option to recalculate without restarting
- 🚫 No external dependencies

### Advanced Version
- 🎨 Polished dark/light themed Tkinter GUI
- 👥 Multi-user support with user management
- 💾 SQLite database for persistent storage
- 📈 BMI trend visualization with Matplotlib
- 📋 Historical record viewing with date filtering
- 📁 CSV export functionality
- 🗑️ Record and user deletion
- 📊 Statistics dashboard (avg, min, max, trend direction)

---

## Project Structure

```
Task 2 - BMI Calculator/
├── README.md
├── requirements.txt
├── beginner/
│   └── bmi_calculator.py        # Single-file CLI application
│
├── advanced/
│   ├── __init__.py
│   ├── main.py                  # GUI entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── bmi_engine.py        # BMI calculation & classification
│   │   └── validators.py        # Input validation logic
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # UserRecord & BMIRecord dataclasses
│   │   └── db_manager.py        # SQLite database operations
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py               # Main application window & navigation
│   │   ├── dashboard.py         # BMI calculation form & result display
│   │   ├── history.py           # Historical records table
│   │   ├── trends.py            # Matplotlib trend chart & statistics
│   │   ├── settings.py          # Theme switching & user management
│   │   └── styles.py            # Theme palettes, fonts, spacing
│   └── utils/
│       ├── __init__.py
│       └── export.py            # CSV export utility
│
└── tests/
    ├── __init__.py
    ├── test_bmi_engine.py       # 33 tests for BMI engine
    ├── test_validators.py       # 31 tests for input validators
    └── test_db_manager.py       # 30 tests for database operations
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohitpandeycs/OIBSIP.git
   cd "Task 2 - BMI Calculator"
   ```

2. **Install dependencies** (for the advanced version):
   ```bash
   pip install -r requirements.txt
   ```

   > The beginner version requires **no external dependencies** — it uses only Python's standard library.

---

## Usage

### Beginner Version (CLI)

Run the CLI calculator directly:

```bash
python beginner/bmi_calculator.py
```

**Example session:**
```
╔══════════════════════════════════════╗
║       BMI CALCULATOR (CLI)           ║
╚══════════════════════════════════════╝

Enter your weight in kg (20-300): 70
Enter your height in meters (0.5-3.0): 1.75

────────────────────────────────────────
  Your BMI: 22.86
  Category: Normal
  Your BMI is within the normal range.
  Maintain a balanced diet and regular
  physical activity to stay in this
  healthy range.
────────────────────────────────────────

Calculate another BMI? (y/n): n
Thank you for using the BMI Calculator!
```

### Advanced Version (GUI)

Run the GUI application:

```bash
python advanced/main.py
```

**Workflow:**
1. **Dashboard** — Select or create a user, enter weight & height, click "Calculate BMI"
2. **Save** — Click "Save Result" to store the record in the database
3. **History** — View, filter by date, delete, or export records to CSV
4. **Trends** — View BMI trend chart with statistics cards
5. **Settings** — Switch dark/light theme, manage users

---

## BMI Classification

Based on WHO (World Health Organization) standards:

| Category      | BMI Range      | Color Code  |
|---------------|----------------|-------------|
| Underweight   | BMI < 18.5     | 🔵 Blue     |
| Normal        | 18.5 ≤ BMI < 25| 🟢 Green    |
| Overweight    | 25 ≤ BMI < 30  | 🟡 Amber    |
| Obese         | BMI ≥ 30       | 🔴 Red      |

**Input Validation Ranges:**
- Weight: 20 – 300 kg
- Height: 0.5 – 3.0 m

---

## Testing

Run the full test suite (94 tests):

```bash
python -m unittest discover -s tests -v
```

Run individual test modules:

```bash
python -m unittest tests.test_bmi_engine -v
python -m unittest tests.test_validators -v
python -m unittest tests.test_db_manager -v
```

**Test Coverage:**
- `test_bmi_engine.py` — 33 tests covering BMI calculation, classification, boundary values, rounding, and error handling
- `test_validators.py` — 31 tests covering weight/height validation, boundary values, error messages, and edge cases
- `test_db_manager.py` — 30 tests covering database initialization, user CRUD, record CRUD, date filtering, statistics, and cascade deletion

---

## Dependencies

| Package       | Version   | Required For        |
|---------------|-----------|---------------------|
| Python        | ≥ 3.10    | Both versions       |
| matplotlib    | ≥ 3.5     | Advanced (charts)    |
| seaborn       | ≥ 0.12    | Advanced (optional)  |

> **Note:** Tkinter and SQLite are included with Python's standard library.

---
