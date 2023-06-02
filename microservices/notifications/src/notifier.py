import redis_client
import sendgrid_client
from config import config
from flask import request
from flask_api import FlaskAPI, status

app = FlaskAPI(__name__)


NOTIFICATIONS_PAYLOAD_SCHEMA = {
    "machine_id": int,
    "created_at": str,
    "warnings": list,
}

WARNINGS_PAYLOAD_SCHEMA = {
    "type": str,
    "current_value": int | float,
    "target_value": int | float,
    "unit": str,
}


@app.route("/health", methods=["GET"])
def health_check():
    return "OK", status.HTTP_200_OK


@app.route("/notifications", methods=["POST"])
def send_notifications():
    notification_payload = request.data

    if not _is_notification_payload_valid(notification_payload):
        return "", status.HTTP_400_BAD_REQUEST

    if redis_client.should_send_email():
        print("Sending email...")
        payloads = redis_client.retrieve_notification_payloads()
        payloads[notification_payload["machine_id"]] = notification_payload
        res = sendgrid_client.send_to_sendgrid(payloads)
        redis_client.set_cooldown()
        return (
            "",
            status.HTTP_204_NO_CONTENT if res else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    else:
        res = redis_client.store_notification_payload(notification_payload)
        return (
            "",
            status.HTTP_200_OK if res else status.HTTP_503_SERVICE_UNAVAILABLE,
        )


def _is_notification_payload_valid(notification_payload):
    if not isinstance(notification_payload, dict):
        return False
    if not _is_according_to_schema(notification_payload, NOTIFICATIONS_PAYLOAD_SCHEMA):
        return False
    for warnings in notification_payload["warnings"]:
        if not _is_according_to_schema(warnings, WARNINGS_PAYLOAD_SCHEMA):
            return False
    return True


def _is_according_to_schema(payload, schema):
    for field, field_type in schema.items():
        if not isinstance(payload.get(field), field_type):
            return False
    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["PORT"], debug=True)
