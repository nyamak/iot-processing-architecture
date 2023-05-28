import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest import mock

from gateway_connector import MQTTConnector


class GatewayConnectorTests(unittest.TestCase):
    def test_on_message_invalid_payload(self):
        mock_process = mock.Mock()

        connector = MQTTConnector("0.0.0.0", 1234, "topic", mock_process)

        msg = SimpleNamespace()
        msg.topic = "topic"
        msg.payload = b"invalid_payload"
        msg.qos = 0
        msg.retain = False

        connector.on_message({}, msg)

        mock_process.assert_not_called()

    def test_on_message_success(self):
        mock_process = mock.Mock()

        connector = MQTTConnector("0.0.0.0", 1234, "topic", mock_process)

        msg = SimpleNamespace()
        msg.topic = "topic"
        msg.payload = b"{'unit_id':123,'created_at':'2022-05-18T11:40:22.519222','is_defective': true,'machine_id':123,'machine_temperature':110.0,'machine_pressure':1.2}"
        msg.qos = 0
        msg.retain = False

        connector.on_message({}, msg)

        mock_process.assert_called_once_with(
            {
                "unit_id": 123,
                "created_at": datetime.fromisoformat("2022-05-18T11:40:22.519222"),
                "is_defective": True,
                "machine_id": 123,
                "machine_temperature": 110.0,
                "machine_pressure": 1.2,
            }
        )

    def test_on_message_invalid_payload_missing_field(self):
        mock_process = mock.Mock()

        connector = MQTTConnector("0.0.0.0", 1234, "topic", mock_process)

        msg = SimpleNamespace()
        msg.topic = "topic"
        msg.payload = b"{'unit_id':123,'created_at':'2022-05-18T11:40:22.519222','is_defective': true,'machine_temperature':110.0,'machine_pressure':1.2}"
        msg.qos = 0
        msg.retain = False

        connector.on_message({}, msg)

        mock_process.assert_not_called()


if __name__ == "__main__":
    unittest.main()
