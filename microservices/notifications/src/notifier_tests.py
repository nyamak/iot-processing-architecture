import unittest
from unittest import mock

import notifier
from flask_api import status


class NotifierTest(unittest.TestCase):
    @mock.patch("notifier.redis_client")
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_invalid_payload_no_machine_id(
        self, mock_sendgrid_client, mock_redis_client
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
            mock_redis_client.should_send_email.assert_not_called()

    @mock.patch("notifier.redis_client")
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_invalid_payload_invalid_warning(
        self, mock_sendgrid_client, mock_redis_client
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
            mock_redis_client.should_send_email.assert_not_called()

    @mock.patch("notifier.redis_client")
    def test_send_notifications_success_cooldown(self, mock_redis_client):
        mock_redis_client.should_send_email.return_value = False
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
            mock_redis_client.store_notification_payload.assert_called_once_with(
                payload
            )
            self.assertEqual(res, ("", status.HTTP_200_OK))

    @mock.patch("notifier.redis_client")
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_success_no_cooldown(
        self, mock_sendgrid_client, mock_redis_client
    ):
        mock_sendgrid_client.send_to_sendgrid.return_value = True
        mock_redis_client.should_send_email.return_value = True
        mock_redis_client.retrieve_notification_payloads.return_value = {}
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
            mock_sendgrid_client.send_to_sendgrid.assert_called_once_with(
                {123: payload}
            )
            mock_redis_client.set_cooldown.assert_called_once()

    @mock.patch("notifier.redis_client")
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_success_no_cooldown_cached(
        self, mock_sendgrid_client, mock_redis_client
    ):
        mock_sendgrid_client.send_to_sendgrid.return_value = True
        mock_redis_client.should_send_email.return_value = True
        mock_redis_client.retrieve_notification_payloads.return_value = {
            456: {
                "machine_id": 456,
                "created_at": "2022-05-18T11:40:22.519222",
                "warnings": [
                    {
                        "type": "temperature",
                        "current_value": 76.0,
                        "target_value": 75.0,
                        "unit": "°C",
                    }
                ],
            }
        }
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
            mock_sendgrid_client.send_to_sendgrid.assert_called_once_with(
                {
                    456: {
                        "machine_id": 456,
                        "created_at": "2022-05-18T11:40:22.519222",
                        "warnings": [
                            {
                                "type": "temperature",
                                "current_value": 76.0,
                                "target_value": 75.0,
                                "unit": "°C",
                            }
                        ],
                    },
                    123: payload,
                }
            )
            mock_redis_client.set_cooldown.assert_called_once()

    @mock.patch("notifier.redis_client")
    @mock.patch("notifier.sendgrid_client")
    def test_send_notifications_success_no_cooldown_cached_repeat(
        self, mock_sendgrid_client, mock_redis_client
    ):
        mock_sendgrid_client.send_to_sendgrid.return_value = True
        mock_redis_client.should_send_email.return_value = True
        mock_redis_client.retrieve_notification_payloads.return_value = {
            123: {
                "machine_id": 123,
                "created_at": "2022-05-18T11:40:22.519222",
                "warnings": [
                    {
                        "type": "temperature",
                        "current_value": 76.0,
                        "target_value": 75.0,
                        "unit": "°C",
                    }
                ],
            }
        }
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
            mock_sendgrid_client.send_to_sendgrid.assert_called_once_with(
                {
                    123: payload,
                }
            )
            mock_redis_client.set_cooldown.assert_called_once()


if __name__ == "__main__":
    unittest.main()
