import unittest
from unittest import mock

import sendgrid_client
from sendgrid import Mail


class SendGridClientTestCase(unittest.TestCase):
    @mock.patch("sendgrid_client.Mail")
    def test_build_notifications_mail_success_one_warning(self, mock_mail):
        notification_payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1.2,
                    "target_value": 1.0,
                    "unit": "atm",
                }
            ],
        }

        res = sendgrid_client.build_notifications_mail([notification_payload])

        self.assertIsNotNone(res)
        mock_mail.assert_called_once_with(
            from_email=None,
            to_emails=None,
            subject="Report: 1 warning(s)",
            html_content="""<h1 style="text-align:center">Warning(s):</h1>
<p><strong>Machine ID:</strong> 123</p>
<p style="margin-left:40px"><strong>Datetime</strong>: 2022-05-18T11:40:22.519222</p>
<p style="margin-left:40px"><strong>Pressure</strong>: 1.20 atm (1.00)</p>
""",
        )

    @mock.patch("sendgrid_client.Mail")
    def test_build_notifications_mail_success(self, mock_mail):
        notification_payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1.2,
                    "target_value": 1.0,
                    "unit": "atm",
                },
                {
                    "type": "defective",
                    "current_value": 10.0,
                    "target_value": 5.0,
                    "unit": "%",
                },
                {
                    "type": "temperature",
                    "current_value": 120,
                    "target_value": 100,
                    "unit": "°C",
                },
            ],
        }

        res = sendgrid_client.build_notifications_mail([notification_payload])

        self.assertIsNotNone(res)
        mock_mail.assert_called_once_with(
            from_email=None,
            to_emails=None,
            subject="Report: 1 warning(s)",
            html_content="""<h1 style="text-align:center">Warning(s):</h1>
<p><strong>Machine ID:</strong> 123</p>
<p style="margin-left:40px"><strong>Datetime</strong>: 2022-05-18T11:40:22.519222</p>
<p style="margin-left:40px"><strong>Pressure</strong>: 1.20 atm (1.00)</p>
<p style="margin-left:40px"><strong>Defective</strong>: 10.00 % (5.00)</p>
<p style="margin-left:40px"><strong>Temperature</strong>: 120.00 °C (100.00)</p>
""",
        )

    @mock.patch("sendgrid_client.Mail")
    def test_build_notifications_mail_success_all_warnings(self, mock_mail):
        notification_payloads = [
            {
                "machine_id": 123,
                "created_at": "2022-05-18T11:40:22.519222",
                "warnings": [
                    {
                        "type": "pressure",
                        "current_value": 1.2,
                        "target_value": 1.0,
                        "unit": "atm",
                    },
                ],
            },
            {
                "machine_id": 456,
                "created_at": "2022-05-18T11:40:22.519222",
                "warnings": [
                    {
                        "type": "defective",
                        "current_value": 10.0,
                        "target_value": 5.0,
                        "unit": "%",
                    },
                    {
                        "type": "temperature",
                        "current_value": 120,
                        "target_value": 100,
                        "unit": "°C",
                    },
                ],
            },
        ]

        res = sendgrid_client.build_notifications_mail(notification_payloads)

        self.assertIsNotNone(res)
        mock_mail.assert_called_once_with(
            from_email=None,
            to_emails=None,
            subject="Report: 2 warning(s)",
            html_content="""<h1 style="text-align:center">Warning(s):</h1>
<p><strong>Machine ID:</strong> 123</p>
<p style="margin-left:40px"><strong>Datetime</strong>: 2022-05-18T11:40:22.519222</p>
<p style="margin-left:40px"><strong>Pressure</strong>: 1.20 atm (1.00)</p>
<p><strong>Machine ID:</strong> 456</p>
<p style="margin-left:40px"><strong>Datetime</strong>: 2022-05-18T11:40:22.519222</p>
<p style="margin-left:40px"><strong>Defective</strong>: 10.00 % (5.00)</p>
<p style="margin-left:40px"><strong>Temperature</strong>: 120.00 °C (100.00)</p>
""",
        )


if __name__ == "__main__":
    unittest.main()
