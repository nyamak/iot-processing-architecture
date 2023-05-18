import os

import requests

NOTIFIER_HOST = os.environ.get("NOTIFIER_HOST")
NOTIFIER_PORT = os.environ.get("NOTIFIER_PORT")


class Warnings:
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    DEFECTIVE = "defective"


class Thresholds:
    PRESSURE = os.environ.get("PRESSURE_LIMIT", 1.2)  # atm
    TEMPERATURE = os.environ.get("TEMPERATURE_LIMIT", 75)  # celsius
    DEFECTIVE = os.environ.get("DEFECTIVE_LIMIT", 0.05)  # %


def send(notification_payload):
    response = requests.post(
        f"{NOTIFIER_HOST}:{NOTIFIER_PORT}/notifications", json=notification_payload
    )
    return response.status_code == 200


def build_notification_payload(machine_id, averages):
    notification_payload = {"machine_id": machine_id, "warnings": []}

    if averages["pressure"] > Thresholds.PRESSURE:
        notification_payload["warnings"].append(
            _build_single_notification_payload(
                Warnings.PRESSURE,
                averages.get("pressure"),
            )
        )
    if averages["temperature"] > Thresholds.TEMPERATURE:
        notification_payload["warnings"].append(
            _build_single_notification_payload(
                Warnings.TEMPERATURE,
                averages.get("temperature"),
            )
        )
    if averages["defective"] > Thresholds.DEFECTIVE:
        notification_payload["warnings"].append(
            _build_single_notification_payload(
                Warnings.DEFECTIVE,
                averages.get("defective"),
            )
        )
    return notification_payload


def _build_single_notification_payload(notification_type, current_value):
    payload = {
        "current_value": current_value,
        "type": notification_type,
    }
    match notification_type:
        case Warnings.PRESSURE:
            payload["target_value"] = Thresholds.PRESSURE
        case Warnings.TEMPERATURE:
            payload["target_value"] = Thresholds.TEMPERATURE
        case Warnings.DEFECTIVE:
            payload["target_value"] = Thresholds.DEFECTIVE
    return payload
