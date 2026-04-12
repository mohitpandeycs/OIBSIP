"""SQLite database management module for BMI Calculator.

Contains the DatabaseManager class handling connection lifecycle,
table creation, CRUD operations for users and BMI records, and
query methods for history and trend data.
"""

import sqlite3
from datetime import datetime
from typing import Optional

from .models import UserRecord, BMIRecord


class DatabaseManager:
    """Manages SQLite connection lifecycle and all database operations.

    Attributes:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path: str = "bmi_data.db") -> None:
        """Initialize the DatabaseManager.

        Args:
            db_path: Path to the SQLite database file. Use ':memory:' for
                     in-memory databases (useful for testing).
        """
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> "DatabaseManager":
        """Context manager entry: open connection and initialize tables."""
        self.initialize_database()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit: close the connection."""
        self.close()

    def initialize_database(self) -> sqlite3.Connection:
        """Create the SQLite database file and tables if they don't exist.

        Returns:
            The active sqlite3.Connection object.
        """
        self._connection = sqlite3.connect(self._db_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        cursor = self._connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL CHECK(length(name) <= 100),
                created_at TEXT    NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BMI_Records (
                record_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                weight_kg  REAL    NOT NULL,
                height_m   REAL    NOT NULL,
                bmi        REAL    NOT NULL,
                category   TEXT    NOT NULL,
                timestamp  TEXT    NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
        """)

        self._connection.commit()
        return self._connection

    def close(self) -> None:
        """Close the database connection if it is open."""
        if self._connection:
            self._connection.close()
            self._connection = None

    # ── User Operations ───────────────────────────────────────────────────

    def add_user(self, name: str) -> int:
        """Insert a new user into the Users table.

        Args:
            name: Display name for the user (max 100 characters).

        Returns:
            The user_id of the newly created user.

        Raises:
            ValueError: If name is empty or exceeds 100 characters.
        """
        if not name or not name.strip():
            raise ValueError("User name cannot be empty.")
        if len(name.strip()) > 100:
            raise ValueError("User name cannot exceed 100 characters.")

        created_at = datetime.now().isoformat()
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO Users (name, created_at) VALUES (?, ?)",
            (name.strip(), created_at),
        )
        self._connection.commit()
        return cursor.lastrowid

    def get_all_users(self) -> list[UserRecord]:
        """Query all users from the Users table.

        Returns:
            A list of UserRecord objects.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT user_id, name, created_at FROM Users ORDER BY name")
        rows = cursor.fetchall()
        return [
            UserRecord(user_id=row[0], name=row[1], created_at=row[2])
            for row in rows
        ]

    def delete_user(self, user_id: int) -> bool:
        """Delete a user and all their associated BMI records.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            True if the user was deleted, False if not found.
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
        self._connection.commit()
        return cursor.rowcount > 0

    # ── BMI Record Operations ────────────────────────────────────────────

    def save_bmi_record(
        self,
        user_id: int,
        weight_kg: float,
        height_m: float,
        bmi: float,
        category: str,
    ) -> int:
        """Insert a BMI record with the current timestamp.

        Args:
            user_id: The ID of the user this record belongs to.
            weight_kg: Weight in kilograms.
            height_m: Height in meters.
            bmi: Calculated BMI value.
            category: WHO category string.

        Returns:
            The record_id of the newly created record.
        """
        timestamp = datetime.now().isoformat()
        cursor = self._connection.cursor()
        cursor.execute(
            """INSERT INTO BMI_Records (user_id, weight_kg, height_m, bmi, category, timestamp)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, weight_kg, height_m, bmi, category, timestamp),
        )
        self._connection.commit()
        return cursor.lastrowid

    def get_user_records(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[BMIRecord]:
        """Query BMI records for a specific user with optional date range filter.

        Args:
            user_id: The ID of the user whose records to retrieve.
            start_date: Optional ISO 8601 start date string for filtering.
            end_date: Optional ISO 8601 end date string for filtering.

        Returns:
            A list of BMIRecord objects ordered by timestamp descending.
        """
        query = """
            SELECT record_id, user_id, weight_kg, height_m, bmi, category, timestamp
            FROM BMI_Records
            WHERE user_id = ?
        """
        params: list = [user_id]

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        query += " ORDER BY timestamp DESC"

        cursor = self._connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [
            BMIRecord(
                record_id=row[0],
                user_id=row[1],
                weight_kg=row[2],
                height_m=row[3],
                bmi=row[4],
                category=row[5],
                timestamp=row[6],
            )
            for row in rows
        ]

    def delete_record(self, record_id: int) -> bool:
        """Delete a specific BMI record by ID.

        Args:
            record_id: The ID of the record to delete.

        Returns:
            True if the record was deleted, False if not found.
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM BMI_Records WHERE record_id = ?", (record_id,))
        self._connection.commit()
        return cursor.rowcount > 0

    # ── Statistics ───────────────────────────────────────────────────────

    def get_bmi_statistics(self, user_id: int) -> dict:
        """Calculate summary statistics for a user's BMI records.

        Args:
            user_id: The ID of the user to analyze.

        Returns:
            A dict with keys: average_bmi, min_bmi, max_bmi, total_records,
            trend_direction. Returns zeros and 'stable' if no records exist.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """SELECT bmi, timestamp FROM BMI_Records
               WHERE user_id = ? ORDER BY timestamp ASC""",
            (user_id,),
        )
        rows = cursor.fetchall()

        if not rows:
            return {
                "average_bmi": 0.0,
                "min_bmi": 0.0,
                "max_bmi": 0.0,
                "total_records": 0,
                "trend_direction": "stable",
            }

        bmis = [row[0] for row in rows]
        total = len(bmis)

        avg_bmi = round(sum(bmis) / total, 2)
        min_bmi = round(min(bmis), 2)
        max_bmi = round(max(bmis), 2)

        # Determine trend: compare average of first half vs second half
        if total >= 2:
            mid = total // 2
            first_half_avg = sum(bmis[:mid]) / mid
            second_half_avg = sum(bmis[mid:]) / (total - mid)
            diff = second_half_avg - first_half_avg

            if diff < -0.5:
                trend = "improving"
            elif diff > 0.5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"

        return {
            "average_bmi": avg_bmi,
            "min_bmi": min_bmi,
            "max_bmi": max_bmi,
            "total_records": total,
            "trend_direction": trend,
        }