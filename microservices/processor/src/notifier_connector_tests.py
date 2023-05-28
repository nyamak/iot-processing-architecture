import unittest
from datetime import datetime
from unittest.mock import ANY, patch

from notifier_connector import Thresholds, Warnings, build_notification_payload, send
from requests.exceptions import Timeout


class NotifierConnectorTest(unittest.TestCase):
    @patch("notifier_connector.requests")
    def test_send_timeout(self, mock_requests):
        mock_requests.post.side_effect = Timeout
        payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:12.519222",
            "warnings": [
                {
                    "type": Warnings.PRESSURE,
                    "current_value": 1.3,
                    "target_value": 1.2,
                    "unit": "atm",
                }
            ],
        }

        with self.assertRaises(Timeout):
            send(payload)
            mock_requests.post.assert_called_once()

    @patch("notifier_connector.requests")
    def test_send_success(self, mock_requests):
        mock_requests.post.return_value.status_code = 200
        payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:12.519222",
            "warnings": [
                {
                    "type": Warnings.TEMPERATURE,
                    "current_value": 100,
                    "target_value": 90,
                    "unit": "°C",
                }
            ],
        }

        res = send(payload)

        mock_requests.post.assert_called_once_with(ANY, json=payload)
        self.assertTrue(res)

    def test_build_notification_payload_success(self):
        averages = {
            "temperature": 100,
            "pressure": 1,
            "defective": 10.0,
        }
        machine_id = 123

        res = build_notification_payload(
            machine_id, datetime.fromisoformat("2022-05-18T11:40:12.519222"), averages
        )

        self.assertEqual(machine_id, res.get("machine_id"))
        self.assertEqual("2022-05-18T11:40:12.519222", res.get("created_at"))
        self.assertIn(
            {
                "type": Warnings.TEMPERATURE,
                "current_value": averages.get("temperature"),
                "target_value": Thresholds.TEMPERATURE,
                "unit": "°C",
            },
            res.get("warnings"),
        )
        self.assertIn(
            {
                "type": Warnings.DEFECTIVE,
                "current_value": averages.get("defective"),
                "target_value": Thresholds.DEFECTIVE,
                "unit": "%",
            },
            res.get("warnings"),
        )


if __name__ == "__main__":
    unittest.main()
