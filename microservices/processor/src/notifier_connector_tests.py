import unittest
from requests.exceptions import Timeout
from unittest.mock import patch, ANY

from notifier_connector import (
    send,
    PRESSURE_WARNING,
    TEMPERATURE_WARNING,
    DEFECTIVE_WARNING,
)


class NotifierConnectorTest(unittest.TestCase):
    @patch("notifier_connector.requests")
    def test_send_timeout(self, mock_requests):
        mock_requests.post.side_effect = Timeout
        payload = {
            "type": PRESSURE_WARNING,
            "machine_id": 123,
            "current_value": 1.3,
            "target_value": 1.2,
        }

        with self.assertRaises(Timeout):
            send(payload)
            mock_requests.post.assert_called_once()

    @patch("notifier_connector.requests")
    def test_send_success(self, mock_requests):
        payload = {
            "type": TEMPERATURE_WARNING,
            "machine_id": 123,
            "current_value": 100,
            "target_value": 90,
        }

        res = send(payload)

        mock_requests.post.assert_called_once_with(ANY, json=payload)
        self.assertTrue(res)

    @patch("notifier_connector.requests")
    def test_send_invalid_payload(self, mock_requests):
        payload = {
            "type": DEFECTIVE_WARNING,
            "machine_id": "not_an_int",
            "current_value": 0.10,
            "target_value": 0.05,
        }

        res = send(payload)

        mock_requests.post.assert_not_called()
        self.assertFalse(res)


if __name__ == "__main__":
    unittest.main()
