import unittest
from unittest import mock

import notifier
from flask_api import status


class NotifierTest(unittest.TestCase):
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_invalid_payload_no_machine_id(
        self, mock_sendgrid_client
    ):
        payload = {
            "machine_id": None,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        m = mock.MagicMock()
        m.data = payload
        with mock.patch("notifier.request", m):
            res = notifier.send_notifications()
            self.assertEqual(res, ("", status.HTTP_400_BAD_REQUEST))
            mock_sendgrid_client.send_to_sendgrid.assert_not_called()

    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_invalid_payload_invalid_warning(
        self, mock_sendgrid_client
    ):
        payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                },
                {
                    "type": "temperature",
                    "current_value": None,
                    "target_value": 0.9,
                    "unit": "°C",
                },
            ],
        }
        m = mock.MagicMock()
        m.data = payload
        with mock.patch("notifier.request", m):
            res = notifier.send_notifications()
            self.assertEqual(res, ("", status.HTTP_400_BAD_REQUEST))
            mock_sendgrid_client.send_to_sendgrid.assert_not_called()

    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_success(self, mock_sendgrid_client):
        mock_sendgrid_client.send_to_sendgrid.return_value = True
        payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        m = mock.MagicMock()
        m.data = payload
        with mock.patch("notifier.request", m):
            res = notifier.send_notifications()
            self.assertEqual(res, ("", status.HTTP_200_OK))
            mock_sendgrid_client.send_to_sendgrid.assert_called_once_with(payload)


if __name__ == "__main__":
    unittest.main()
