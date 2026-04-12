"""Data model definitions for the BMI Calculator database.

Contains dataclass definitions for UserRecord and BMIRecord
used throughout the application.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserRecord:
    """Represents a user in the database.

    Attributes:
        user_id: Primary key from SQLite.
        name: Display name, max 100 characters.
        created_at: ISO 8601 timestamp of user creation.
    """
    user_id: int
    name: str
    created_at: str


@dataclass(frozen=True)
class BMIRecord:
    """Represents a BMI calculation record in the database.

    Attributes:
        record_id: Primary key from SQLite.
        user_id: Foreign key to Users table.
        weight_kg: Weight in kilograms at time of calculation.
        height_m: Height in meters at time of calculation.
        bmi: Calculated BMI value.
        category: WHO category string.
        timestamp: ISO 8601 timestamp of record creation.
    """
    record_id: int
    user_id: int
    weight_kg: float
    height_m: float
    bmi: float
    category: str
    timestamp: str