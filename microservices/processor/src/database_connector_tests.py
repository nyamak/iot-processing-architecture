import unittest
from datetime import datetime

from database_connector import _get_connection, get_averages, save_payload_to_db


class DatabaseConnectorTests(unittest.TestCase):
    def setUp(self):
        self._clear_db()

    def tearDown(self):
        self._clear_db()

    def _clear_db(self):
        """
        Clear every table.
        """
        with _get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM units;")
                cursor.execute("DELETE FROM measurements;")
                cursor.execute("DELETE FROM machines;")
                cursor.close()
                conn.commit()
            except:
                conn.rollback()

    def test_save_payload_to_db(self):
        payload = {
            "unit_id": 456,
            "created_at": datetime.fromisoformat("2022-05-18T11:40:22.519222"),
            "is_defective": True,
            "machine_id": 123,
            "machine_temperature": 110.0,
            "machine_pressure": 1.2,
        }
        save_payload_to_db(**payload)

        with _get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT
                        machine_id, unit_id, is_defective, created_at
                    FROM
                        units;
                    """
                )
                res = cursor.fetchone()
                self.assertEqual(
                    res,
                    (
                        123,
                        456,
                        True,
                        datetime.fromisoformat("2022-05-18T11:40:22.519222"),
                    ),
                )

                cursor.execute(
                    """
                    SELECT
                        machine_id
                    FROM
                        machines;
                    """
                )
                res = cursor.fetchone()
                self.assertEqual(res, (123,))

                cursor.execute(
                    """
                    SELECT
                        machine_id, temperature, pressure, created_at
                    FROM
                        measurements;
                    """
                )
                res = cursor.fetchone()
                self.assertEqual(
                    res,
                    (
                        123,
                        110.0,
                        1.2,
                        datetime.fromisoformat("2022-05-18T11:40:22.519222"),
                    ),
                )

                cursor.close()
                conn.commit()
            except:
                conn.rollback()
                self.fail()

    def test_get_averages(self):
        machine_id = 123
        timestamp = datetime.fromisoformat("2022-05-18T11:39:25.519222")
        save_payload_to_db(
            **{
                "unit_id": 456,
                "created_at": datetime.fromisoformat("2022-05-18T11:40:22.519222"),
                "is_defective": False,
                "machine_id": 123,
                "machine_temperature": 0.0,
                "machine_pressure": 0.0,
            }
        )
        save_payload_to_db(
            **{
                "unit_id": 789,
                "created_at": datetime.fromisoformat("2022-05-18T11:40:22.519222"),
                "is_defective": True,
                "machine_id": 123,
                "machine_temperature": 100.0,
                "machine_pressure": 1.0,
            }
        )
        # created_at outside scope
        save_payload_to_db(
            **{
                "unit_id": 101112,
                "created_at": datetime.fromisoformat("2022-05-18T11:37:22.519222"),
                "is_defective": True,
                "machine_id": 123,
                "machine_temperature": 100.0,
                "machine_pressure": 1.0,
            }
        )

        res = get_averages(machine_id, timestamp)

        self.assertEqual(res, (50.0, 0.5, 0.5))

    def test_get_averages_no_records(self):
        machine_id = 123
        timestamp = datetime.fromisoformat("2022-05-18T11:39:25.519222")

        res = get_averages(machine_id, timestamp)

        self.assertEqual(res, (None, None, None))


if __name__ == "__main__":
    unittest.main()
