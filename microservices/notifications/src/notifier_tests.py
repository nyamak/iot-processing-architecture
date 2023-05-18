import unittest
from unittest import mock

import notifier
from flask_api import status


class NotifierTest(unittest.TestCase):
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_invalid_payload(self, mock_sendgrid_client):
        payload = [
            {
                "type": "pressure_warning",
                "machine_id": "NOT AN INT",
                "current_value": 1,
                "target_value": 0.9,
            }
        ]
        m = mock.MagicMock()
        m.data = payload
        with mock.patch("notifier.request", m):
            res = notifier.send_notifications()
            self.assertEqual(res, ("", status.HTTP_400_BAD_REQUEST))
            mock_sendgrid_client.send_to_sendgrid.assert_not_called()

    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_success(self, mock_sendgrid_client):
        mock_sendgrid_client.send_to_sendgrid.return_value = True
        payload = [
            {
                "type": "pressure_warning",
                "machine_id": 123,
                "current_value": 1,
                "target_value": 0.9,
            }
        ]
        m = mock.MagicMock()
        m.data = payload
        with mock.patch("notifier.request", m):
            res = notifier.send_notifications()
            self.assertEqual(res, ("", status.HTTP_200_OK))
            mock_sendgrid_client.send_to_sendgrid.assert_called_once_with(payload)


if __name__ == "__main__":
    unittest.main()
