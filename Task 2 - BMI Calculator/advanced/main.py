"""Entry point for the Advanced BMI Calculator GUI application.
"""

import sys
import os


def main() -> None:
    """Launch the BMI Calculator GUI application."""
    # Ensure the project root is on sys.path so relative imports work
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from advanced.gui.app import BMIApp

    # Use a database file in the same directory as the script
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_data.db")

    app = BMIApp(db_path=db_path)
    app.mainloop()


if __name__ == "__main__":
    main()
