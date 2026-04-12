"""CSV export utility for BMI Calculator.

Provides the CSVExporter class with a static method to export
BMI records to a CSV file using a file save dialog.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..database.models import BMIRecord


class CSVExporter:
    """Static utility class for exporting BMI records to CSV files."""

    @staticmethod
    def export(records: list[BMIRecord], user_name: str) -> Optional[str]:
        """Export a list of BMI records to a CSV file.

        Opens a file save dialog for the user to choose the save location.
        The CSV includes columns: Date, Weight (kg), Height (m), BMI, Category.

        Args:
            records: List of BMIRecord objects to export.
            user_name: Name of the user (used for default filename).

        Returns:
            The filepath of the saved CSV file, or None if cancelled.
        """
        try:
            from tkinter import filedialog
        except ImportError:
            return None

        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = user_name.replace(" ", "_").replace("/", "_")
        default_name = f"bmi_records_{safe_name}_{timestamp}.csv"

        # Open save dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=default_name,
            title="Export BMI Records",
        )

        if not filepath:
            return None

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Header row
                writer.writerow(["Date", "Weight (kg)", "Height (m)", "BMI", "Category"])

                # Data rows
                for rec in records:
                    # Format timestamp for readability
                    try:
                        dt = datetime.fromisoformat(rec.timestamp)
                        display_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except (ValueError, TypeError):
                        display_date = rec.timestamp

                    writer.writerow([
                        display_date,
                        f"{rec.weight_kg:.1f}",
                        f"{rec.height_m:.2f}",
                        f"{rec.bmi:.2f}",
                        rec.category,
                    ])

            return filepath

        except (OSError, IOError) as e:
            return None