import unittest
from unittest import mock

from processor import get_averages_for_machine, process

# Note: to run these tests, use docker-compose up metrics-db on microservices/processor
# to spin up test DB and apply migrations manually on first time.


class ProcessorTests(unittest.TestCase):
    @mock.patch("processor.get_averages_for_machine")
    @mock.patch("processor.notifier_connector")
    @mock.patch("processor.database_connector")
    def test_process(self, mock_database, mock_notifier, mock_get_averages):
        mock_get_averages.return_value = {
            "temperature": 150.0,
            "pressure": 1.5,
            "defective": 20.0,
        }
        mock_notifier.build_notification_payload.return_value = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "temperature",
                    "current_value": 150.0,
                    "target_value": 75.0,
                    "unit": "°C",
                },
                {
                    "type": "pressure",
                    "current_value": 1.5,
                    "target_value": 1.2,
                    "unit": "atm",
                },
                {
                    "type": "temperature",
                    "current_value": 20.0,
                    "target_value": 5.0,
                    "unit": "%",
                },
            ],
        }

        payload = {
            "unit_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "is_defective": True,
            "machine_id": 123,
            "machine_temperature": 110.0,
            "machine_pressure": 1.2,
        }

        process(payload)

        mock_database.save_measurement_to_db.assert_called_once_with(**payload)
        mock_get_averages.assert_called_once_with(123, "2022-05-18T11:40:22.519222")
        mock_notifier.send.assert_called_once()

    @mock.patch("processor.get_averages_for_machine")
    @mock.patch("processor.notifier_connector")
    @mock.patch("processor.database_connector")
    def test_process_no_notifications(
        self, mock_database, mock_notifier, mock_get_averages
    ):
        mock_get_averages.return_value = {
            "temperature": 15.0,
            "pressure": 1.0,
            "defective": 2.0,
        }
        mock_notifier.build_notification_payload.return_value = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [],
        }

        payload = {
            "unit_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "is_defective": True,
            "machine_id": 123,
            "machine_temperature": 15.0,
            "machine_pressure": 1.0,
        }

        process(payload)

        mock_database.save_measurement_to_db.assert_called_once_with(**payload)
        mock_get_averages.assert_called_once_with(123, "2022-05-18T11:40:22.519222")
        mock_notifier.send.assert_not_called()

    @mock.patch("processor.database_connector")
    def test_get_averages_for_machine(self, mock_database_connector):
        mock_database_connector.get_averages_of_latest_measurements.return_value = (
            60,
            1.1,
        )
        mock_database_connector.get_defective_average.return_value = 0.13

        res = get_averages_for_machine(123, "2022-05-18T11:40:22.519222")

        self.assertEqual(
            res,
            {
                "temperature": 60,
                "pressure": 1.1,
                "defective": 13.0,
            },
        )


if __name__ == "__main__":
    unittest.main()
