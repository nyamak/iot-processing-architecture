import json
from datetime import datetime

import paho.mqtt.client as mqtt

PAYLOAD_SCHEMA = {
    "unit_id": {"type": int, "is_required": True},
    "created_at": {"type": str, "is_required": True},
    "is_defective": {"type": bool, "is_required": False},
    "machine_id": {"type": int, "is_required": True},
    "machine_temperature": {"type": float, "is_required": False},
    "machine_pressure": {"type": float, "is_required": False},
}


def _bytes_to_dict(payload_bytes):
    """
    Convert payload bytes to dictionary format.
    """
    try:
        decoded_payload = payload_bytes.decode("utf-8").replace("'", '"')
        return json.loads(decoded_payload)
    except Exception:
        return None


def _is_valid(payload_dict):
    """
    Validates if payload has all obligatory fields and has correct types.
    """
    if not isinstance(payload_dict, dict):
        return False

    for field, attrs in PAYLOAD_SCHEMA.items():
        if attrs["is_required"] and field not in payload_dict:
            return False
        if not isinstance(payload_dict[field], attrs["type"]):
            return False

    if not _is_datetime_isostring(payload_dict["created_at"]):
        return False

    return True


def _is_datetime_isostring(string):
    try:
        datetime.fromisoformat(string)
        return True
    except:
        return False


class MQTTConnector:
    def __init__(self, host, port, topic, process) -> None:
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.host = host
        self.port = port
        self.topic = topic
        self.process = process

    def on_connect(self, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        dict_payload = _bytes_to_dict(msg.payload)
        if not _is_valid(dict_payload):
            print("Error:payload not valid.")
            return

        dict_payload["created_at"] = datetime.fromisoformat(dict_payload["created_at"])
        self.process(dict_payload)

    def main(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()
        self.client.disconnect()
