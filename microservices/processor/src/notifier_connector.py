import requests
from config import config


class Warnings:
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    DEFECTIVE = "defective"


class Thresholds:
    PRESSURE = config["PRESSURE_LIMIT"]  # atm
    TEMPERATURE = config["TEMPERATURE_LIMIT"]  # celsius
    DEFECTIVE = config["DEFECTIVE_LIMIT"]  # %


def send(notification_payload):
    try:
        response = requests.post(
            f"http://{config['NOTIFIER_HOST']}:{config['NOTIFIER_PORT']}/notifications",
            json=notification_payload,
        )
        return response.status_code == 200
    except:
        print("Failed to send notification.")
        return False


def build_notification_payload(machine_id, created_at, averages):
    notification_payload = {
        "machine_id": machine_id,
        "created_at": created_at.isoformat(),
        "warnings": [],
    }

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
            payload["unit"] = "atm"
        case Warnings.TEMPERATURE:
            payload["target_value"] = Thresholds.TEMPERATURE
            payload["unit"] = "°C"
        case Warnings.DEFECTIVE:
            payload["target_value"] = Thresholds.DEFECTIVE
            payload["unit"] = "%"
    return payload
