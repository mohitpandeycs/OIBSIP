"""Integration tests for the DatabaseManager class.

Uses an in-memory SQLite database (:memory:) for testing.
Tests database initialization, user CRUD, BMI record CRUD,
date range filtering, statistics calculation, and record deletion.
"""

import unittest

from advanced.database.db_manager import DatabaseManager
from advanced.database.models import UserRecord, BMIRecord


class TestDatabaseInitialization(unittest.TestCase):
    """Tests for DatabaseManager initialization."""

    def test_initialize_creates_connection(self):
        """initialize_database should return a connection object."""
        db = DatabaseManager(":memory:")
        conn = db.initialize_database()
        self.assertIsNotNone(conn)
        db.close()

    def test_initialize_creates_tables(self):
        """initialize_database should create Users and BMI_Records tables."""
        db = DatabaseManager(":memory:")
        db.initialize_database()
        cursor = db._connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = {row[0] for row in cursor.fetchall()}
        self.assertIn("Users", tables)
        self.assertIn("BMI_Records", tables)
        db.close()

    def test_context_manager(self):
        """DatabaseManager should work as a context manager."""
        with DatabaseManager(":memory:") as db:
            self.assertIsNotNone(db._connection)
        self.assertIsNone(db._connection)


class TestUserOperations(unittest.TestCase):
    """Tests for user CRUD operations."""

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.initialize_database()

    def tearDown(self):
        self.db.close()

    def test_add_user_returns_id(self):
        """add_user should return a positive integer user_id."""
        user_id = self.db.add_user("Alice")
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)

    def test_add_user_increments_id(self):
        """Successive add_user calls should return incrementing IDs."""
        id1 = self.db.add_user("Alice")
        id2 = self.db.add_user("Bob")
        self.assertEqual(id2, id1 + 1)

    def test_add_user_strips_whitespace(self):
        """add_user should strip leading/trailing whitespace from name."""
        user_id = self.db.add_user("  Charlie  ")
        users = self.db.get_all_users()
        self.assertEqual(users[0].name, "Charlie")

    def test_add_user_empty_name_raises(self):
        """add_user should raise ValueError for empty name."""
        with self.assertRaises(ValueError):
            self.db.add_user("")

    def test_add_user_whitespace_name_raises(self):
        """add_user should raise ValueError for whitespace-only name."""
        with self.assertRaises(ValueError):
            self.db.add_user("   ")

    def test_add_user_long_name_raises(self):
        """add_user should raise ValueError for name exceeding 100 characters."""
        with self.assertRaises(ValueError):
            self.db.add_user("A" * 101)

    def test_get_all_users_empty(self):
        """get_all_users should return empty list when no users exist."""
        users = self.db.get_all_users()
        self.assertEqual(users, [])

    def test_get_all_users_returns_user_records(self):
        """get_all_users should return UserRecord instances."""
        self.db.add_user("Alice")
        users = self.db.get_all_users()
        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], UserRecord)
        self.assertEqual(users[0].name, "Alice")

    def test_get_all_users_ordered_by_name(self):
        """get_all_users should return users ordered alphabetically by name."""
        self.db.add_user("Charlie")
        self.db.add_user("Alice")
        self.db.add_user("Bob")
        users = self.db.get_all_users()
        names = [u.name for u in users]
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])

    def test_delete_user(self):
        """delete_user should remove the user from the database."""
        user_id = self.db.add_user("Alice")
        result = self.db.delete_user(user_id)
        self.assertTrue(result)
        users = self.db.get_all_users()
        self.assertEqual(len(users), 0)

    def test_delete_nonexistent_user(self):
        """delete_user should return False for non-existent user."""
        result = self.db.delete_user(999)
        self.assertFalse(result)

    def test_delete_user_cascades_records(self):
        """Deleting a user should also delete their BMI records."""
        user_id = self.db.add_user("Alice")
        self.db.save_bmi_record(user_id, 70.0, 1.75, 22.86, "Normal")
        self.db.delete_user(user_id)
        records = self.db.get_user_records(user_id)
        self.assertEqual(len(records), 0)


class TestBMIRecordOperations(unittest.TestCase):
    """Tests for BMI record CRUD operations."""

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.initialize_database()
        self.user_id = self.db.add_user("TestUser")

    def tearDown(self):
        self.db.close()

    def test_save_bmi_record_returns_id(self):
        """save_bmi_record should return a positive integer record_id."""
        record_id = self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        self.assertIsInstance(record_id, int)
        self.assertGreater(record_id, 0)

    def test_save_bmi_record_increments_id(self):
        """Successive save_bmi_record calls should return incrementing IDs."""
        id1 = self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        id2 = self.db.save_bmi_record(self.user_id, 80.0, 1.75, 26.12, "Overweight")
        self.assertEqual(id2, id1 + 1)

    def test_get_user_records_empty(self):
        """get_user_records should return empty list when no records exist."""
        records = self.db.get_user_records(self.user_id)
        self.assertEqual(records, [])

    def test_get_user_records_returns_bmi_records(self):
        """get_user_records should return BMIRecord instances."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        records = self.db.get_user_records(self.user_id)
        self.assertEqual(len(records), 1)
        self.assertIsInstance(records[0], BMIRecord)
        self.assertEqual(records[0].weight_kg, 70.0)
        self.assertEqual(records[0].height_m, 1.75)
        self.assertEqual(records[0].bmi, 22.86)
        self.assertEqual(records[0].category, "Normal")

    def test_get_user_records_returns_all(self):
        """get_user_records should return all records for a user."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        self.db.save_bmi_record(self.user_id, 80.0, 1.75, 26.12, "Overweight")
        records = self.db.get_user_records(self.user_id)
        self.assertEqual(len(records), 2)
        categories = {r.category for r in records}
        self.assertIn("Normal", categories)
        self.assertIn("Overweight", categories)

    def test_get_user_records_date_filter(self):
        """get_user_records should filter by date range."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        # Filter with a far-future end date should include the record
        records = self.db.get_user_records(self.user_id, end_date="2099-12-31")
        self.assertEqual(len(records), 1)
        # Filter with a past end date should exclude the record
        records = self.db.get_user_records(self.user_id, end_date="2000-01-01")
        self.assertEqual(len(records), 0)

    def test_get_user_records_other_user(self):
        """get_user_records should only return records for the specified user."""
        other_user_id = self.db.add_user("OtherUser")
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        self.db.save_bmi_record(other_user_id, 80.0, 1.75, 26.12, "Overweight")
        records = self.db.get_user_records(self.user_id)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].category, "Normal")

    def test_delete_record(self):
        """delete_record should remove the specified record."""
        record_id = self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        result = self.db.delete_record(record_id)
        self.assertTrue(result)
        records = self.db.get_user_records(self.user_id)
        self.assertEqual(len(records), 0)

    def test_delete_nonexistent_record(self):
        """delete_record should return False for non-existent record."""
        result = self.db.delete_record(999)
        self.assertFalse(result)


class TestBMIStatistics(unittest.TestCase):
    """Tests for BMI statistics calculation."""

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.initialize_database()
        self.user_id = self.db.add_user("TestUser")

    def tearDown(self):
        self.db.close()

    def test_statistics_no_records(self):
        """Statistics for a user with no records should return zeros."""
        stats = self.db.get_bmi_statistics(self.user_id)
        self.assertEqual(stats["average_bmi"], 0.0)
        self.assertEqual(stats["min_bmi"], 0.0)
        self.assertEqual(stats["max_bmi"], 0.0)
        self.assertEqual(stats["total_records"], 0)
        self.assertEqual(stats["trend_direction"], "stable")

    def test_statistics_single_record(self):
        """Statistics for a single record should have same min/max/avg."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        stats = self.db.get_bmi_statistics(self.user_id)
        self.assertEqual(stats["average_bmi"], 22.86)
        self.assertEqual(stats["min_bmi"], 22.86)
        self.assertEqual(stats["max_bmi"], 22.86)
        self.assertEqual(stats["total_records"], 1)
        self.assertEqual(stats["trend_direction"], "stable")

    def test_statistics_multiple_records(self):
        """Statistics should correctly compute avg, min, max for multiple records."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        self.db.save_bmi_record(self.user_id, 80.0, 1.75, 26.12, "Overweight")
        self.db.save_bmi_record(self.user_id, 90.0, 1.75, 29.39, "Overweight")
        stats = self.db.get_bmi_statistics(self.user_id)
        self.assertEqual(stats["total_records"], 3)
        self.assertEqual(stats["min_bmi"], 22.86)
        self.assertEqual(stats["max_bmi"], 29.39)
        self.assertAlmostEqual(stats["average_bmi"], 26.12, places=2)

    def test_statistics_improving_trend(self):
        """Trend should be 'improving' when BMI decreases over time."""
        self.db.save_bmi_record(self.user_id, 90.0, 1.75, 29.39, "Overweight")
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        stats = self.db.get_bmi_statistics(self.user_id)
        self.assertEqual(stats["trend_direction"], "improving")

    def test_statistics_declining_trend(self):
        """Trend should be 'declining' when BMI increases over time."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        self.db.save_bmi_record(self.user_id, 90.0, 1.75, 29.39, "Overweight")
        stats = self.db.get_bmi_statistics(self.user_id)
        self.assertEqual(stats["trend_direction"], "declining")

    def test_statistics_stable_trend(self):
        """Trend should be 'stable' when BMI doesn't change much."""
        self.db.save_bmi_record(self.user_id, 70.0, 1.75, 22.86, "Normal")
        self.db.save_bmi_record(self.user_id, 71.0, 1.75, 23.18, "Normal")
        stats = self.db.get_bmi_statistics(self.user_id)
        self.assertEqual(stats["trend_direction"], "stable")


if __name__ == "__main__":
    unittest.main()