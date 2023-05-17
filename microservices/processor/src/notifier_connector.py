import os
import requests

NOTIFIER_HOST = os.environ.get("NOTIFIER_HOST")
NOTIFIER_PORT = os.environ.get("NOTIFIER_PORT")


class Warnings:
    PRESSURE = "pressure_warning"
    TEMPERATURE = "temperature_warning"
    DEFECTIVE = "defective_warning"


PRESSURE_LIMIT = os.environ.get("PRESSURE_LIMIT", 1.2)  # atm
TEMPERATURE_LIMIT = os.environ.get("TEMPERATURE_LIMIT", 75)  # celsius
DEFECTIVE_LIMIT = os.environ.get("DEFECTIVE_LIMIT", 0.05)  # %

PAYLOAD_SCHEMA = {
    "type": str,
    "machine_id": int,
    "current_value": int | float,
    "target_value": int | float,
}


def send(notification_payload):
    if not _is_payload_valid(notification_payload):
        return False

    requests.post(f"{NOTIFIER_HOST}:{NOTIFIER_PORT}/", json=notification_payload)
    return True


def _is_payload_valid(notification_payload):
    if not isinstance(notification_payload, list):
        return False
    for subpayload in notification_payload:
        for field, field_type in PAYLOAD_SCHEMA.items():
            if field not in subpayload:
                return False
            if not isinstance(subpayload[field], field_type):
                return False
    return True


def build_notification_payload(payload_dict, stats):
    notification_payload = []

    if stats["pressure_average"] > PRESSURE_LIMIT:
        notification_payload.append(
            _build_single_notification_payload(
                Warnings.PRESSURE,
                payload_dict.get("machine_id"),
                stats.get("pressure_average"),
            )
        )
    if stats["temperature_average"] > TEMPERATURE_LIMIT:
        notification_payload.append(
            _build_single_notification_payload(
                Warnings.TEMPERATURE,
                payload_dict.get("machine_id"),
                stats.get("temperature_average"),
            )
        )
    if stats["defective_average"] > DEFECTIVE_LIMIT:
        notification_payload.append(
            _build_single_notification_payload(
                Warnings.DEFECTIVE_LIMIT,
                payload_dict.get("machine_id"),
                stats.get("defective_average"),
            )
        )
    return notification_payload


def _build_single_notification_payload(notification_type, machine_id, current_value):
    payload = {
        "machine_id": machine_id,
        "current_value": current_value,
        "notification_type": notification_type,
    }
    match notification_type:
        case Warnings.PRESSURE:
            payload["target_value"] = PRESSURE_LIMIT
        case Warnings.TEMPERATURE:
            payload["target_value"] = TEMPERATURE_LIMIT
        case Warnings.DEFECTIVE:
            payload["target_value"] = DEFECTIVE_LIMIT
    return payload
