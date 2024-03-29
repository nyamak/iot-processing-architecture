import unittest
from datetime import datetime
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

        payload_dict = {
            "unit_id": 123,
            "created_at": datetime.fromisoformat("2022-05-18T11:40:22.519222"),
            "is_defective": True,
            "machine_id": 123,
            "machine_temperature": 110.0,
            "machine_pressure": 1.2,
        }

        process(payload_dict)

        mock_database.save_payload_to_db.assert_called_once_with(**payload_dict)
        mock_get_averages.assert_called_once_with(
            123,
            datetime.fromisoformat("2022-05-18T11:39:22.519222"),
        )
        mock_notifier.build_notification_payload.assert_called_once_with(
            123,
            datetime.fromisoformat("2022-05-18T11:40:22.519222"),
            {
                "temperature": 150.0,
                "pressure": 1.5,
                "defective": 20.0,
            },
        )
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
            "created_at": datetime.fromisoformat("2022-05-18T11:40:22.519222"),
            "is_defective": True,
            "machine_id": 123,
            "machine_temperature": 15.0,
            "machine_pressure": 1.0,
        }

        process(payload)

        mock_database.save_payload_to_db.assert_called_once_with(**payload)
        mock_get_averages.assert_called_once_with(
            123, datetime.fromisoformat("2022-05-18T11:39:22.519222")
        )
        mock_notifier.build_notification_payload.assert_called_once_with(
            123,
            datetime.fromisoformat("2022-05-18T11:40:22.519222"),
            {
                "temperature": 15.0,
                "pressure": 1.0,
                "defective": 2.0,
            },
        )
        mock_notifier.send.assert_not_called()

    @mock.patch("processor.database_connector")
    def test_get_averages_for_machine_success(self, mock_database_connector):
        mock_database_connector.get_averages.return_value = (
            60,
            1.1,
            0.13,
        )

        res = get_averages_for_machine(
            123, datetime.fromisoformat("2022-05-18T11:40:12.519222")
        )

        self.assertEqual(
            res,
            {
                "temperature": 60,
                "pressure": 1.1,
                "defective": 13.0,
            },
        )

    @mock.patch("processor.database_connector")
    def test_get_averages_for_machine_no_average(self, mock_database_connector):
        mock_database_connector.get_averages.return_value = (
            None,
            None,
            None,
        )

        res = get_averages_for_machine(
            123, datetime.fromisoformat("2022-05-18T11:40:12.519222")
        )

        self.assertEqual(
            res,
            {
                "temperature": 0.0,
                "pressure": 0.0,
                "defective": 0.0,
            },
        )


if __name__ == "__main__":
    unittest.main()
