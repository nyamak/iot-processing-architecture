import unittest
from unittest.mock import ANY, patch

from notifier_connector import Thresholds, Warnings, build_notification_payload, send
from requests.exceptions import Timeout


class NotifierConnectorTest(unittest.TestCase):
    @patch("notifier_connector.requests")
    def test_send_timeout(self, mock_requests):
        mock_requests.post.side_effect = Timeout
        payload = [
            {
                "type": Warnings.PRESSURE,
                "machine_id": 123,
                "current_value": 1.3,
                "target_value": 1.2,
            }
        ]

        with self.assertRaises(Timeout):
            send(payload)
            mock_requests.post.assert_called_once()

    @patch("notifier_connector.requests")
    def test_send_success(self, mock_requests):
        payload = [
            {
                "type": Warnings.TEMPERATURE,
                "machine_id": 123,
                "current_value": 100,
                "target_value": 90,
            }
        ]

        res = send(payload)

        mock_requests.post.assert_called_once_with(ANY, json=payload)
        self.assertTrue(res)

    @patch("notifier_connector.requests")
    def test_send_invalid_payload(self, mock_requests):
        payload = [
            {
                "type": Warnings.DEFECTIVE,
                "machine_id": "not_an_int",
                "current_value": 0.10,
                "target_value": 0.05,
            }
        ]

        res = send(payload)

        mock_requests.post.assert_not_called()
        self.assertFalse(res)

    def test_build_notification_payload_success(self):
        stats = {
            "temperature_average": 100,
            "pressure_average": 1,
            "defective_average": 0.10,
        }
        machine_id = 123

        res = build_notification_payload(machine_id, stats)

        self.assertIn(
            {
                "type": Warnings.TEMPERATURE,
                "machine_id": machine_id,
                "current_value": stats.get("temperature_average"),
                "target_value": Thresholds.TEMPERATURE,
            },
            res,
        )
        self.assertIn(
            {
                "type": Warnings.DEFECTIVE,
                "machine_id": machine_id,
                "current_value": stats.get("defective_average"),
                "target_value": Thresholds.DEFECTIVE,
            },
            res,
        )


if __name__ == "__main__":
    unittest.main()
