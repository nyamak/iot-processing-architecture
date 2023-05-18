import os

import requests

NOTIFIER_HOST = os.environ.get("NOTIFIER_HOST")
NOTIFIER_PORT = os.environ.get("NOTIFIER_PORT")


class Warnings:
    PRESSURE = "pressure_warning"
    TEMPERATURE = "temperature_warning"
    DEFECTIVE = "defective_warning"


class Thresholds:
    PRESSURE = os.environ.get("PRESSURE_LIMIT", 1.2)  # atm
    TEMPERATURE = os.environ.get("TEMPERATURE_LIMIT", 75)  # celsius
    DEFECTIVE = os.environ.get("DEFECTIVE_LIMIT", 0.05)  # %


def send(notification_payload):
    response = requests.post(
        f"{NOTIFIER_HOST}:{NOTIFIER_PORT}/notifications", json=notification_payload
    )
    return response.status_code == 200


def build_notification_payload(machine_id, stats):
    notification_payload = []

    if stats["pressure_average"] > Thresholds.PRESSURE:
        notification_payload.append(
            _build_single_notification_payload(
                Warnings.PRESSURE,
                machine_id,
                stats.get("pressure_average"),
            )
        )
    if stats["temperature_average"] > Thresholds.TEMPERATURE:
        notification_payload.append(
            _build_single_notification_payload(
                Warnings.TEMPERATURE,
                machine_id,
                stats.get("temperature_average"),
            )
        )
    if stats["defective_average"] > Thresholds.DEFECTIVE:
        notification_payload.append(
            _build_single_notification_payload(
                Warnings.DEFECTIVE,
                machine_id,
                stats.get("defective_average"),
            )
        )
    return notification_payload


def _build_single_notification_payload(notification_type, machine_id, current_value):
    payload = {
        "machine_id": machine_id,
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
