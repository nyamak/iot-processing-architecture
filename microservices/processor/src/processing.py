import json
import math

import database as db

PAYLOAD_SCHEMA = {
    "unit_id": {"type": int, "is_required": True},
    "created_at": {"type": str, "is_required": True},
    "is_defective": {"type": bool, "is_required": False},
    "machine_id": {"type": int, "is_required": True},
    "machine_temperature": {"type": float, "is_required": False},
    "machine_pressure": {"type": float, "is_required": False},
}


# TODO: remove this from here
def process(payload_bytes):
    """
    Processes the payload in the dictionary format.
    """
    payload_dict = bytes_to_dict(payload_bytes)
    if is_valid(payload_dict):
        db.save_metrics_to_db(**payload_dict)


def bytes_to_dict(payload_bytes):
    """
    Convert payload bytes to dictionary format.
    """
    try:
        decoded_payload = payload_bytes.decode("utf-8").replace("'", '"')
        return json.dumps(decoded_payload)
    except Exception:
        return None


def is_valid(payload_dict):
    """
    Validates if payload has all obligatory fields and has correct types.
    """
    if not isinstance(payload_dict, dict):
        return False

    for k, v in PAYLOAD_SCHEMA.items():
        if v.get("is_required") and k not in payload_dict:
            return False
        if not isinstance(payload_dict[k], v.get("type")):
            return False
    return True


# TODO: remove this from here
# TODO: get these fucking things done lol like just calculate all the averages
# and see if they are varying too much or over a threshold IDK lol
def get_stats_for_device(device_id, timestamp):
    stats = dict()
    metrics = db.get_latest_metrics(device_id, timestamp)
    temperatures, pressures = [], []
    for temperature, pressure in metrics:
        temperatures.append(temperature)
        pressures.append(pressure)

    stats["temperature_average"] = sum(temperatures) / len(temperatures)
    stats["pressure_average"] = sum(pressures) / len(pressures)
    return stats
