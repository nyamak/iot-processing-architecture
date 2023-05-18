import os

import sendgrid_client
from flask_api import FlaskAPI, request, status

app = FlaskAPI(__name__)


WARNINGS_PAYLOAD_SCHEMA = {
    "type": str,
    "current_value": int | float,
    "target_value": int | float,
}


@app.route("/notifications", methods=["POST"])
def send_notifications():
    notification_payload = request.data
    if not _is_notification_payload_valid(notification_payload):
        return "", status.HTTP_400_BAD_REQUEST

    res = sendgrid_client.send_to_sendgrid(notification_payload)
    return (
        "",
        status.HTTP_200_OK if res else status.HTTP_503_SERVICE_UNAVAILABLE,
    )


def _is_notification_payload_valid(notification_payload):
    if not isinstance(notification_payload, dict):
        return False
    if not isinstance(notification_payload.get("machine_id"), int):
        return False
    if not isinstance(notification_payload.get("warnings"), list):
        return False
    for warnings in notification_payload["warnings"]:
        for field, field_type in WARNINGS_PAYLOAD_SCHEMA.items():
            if field not in warnings:
                return False
            if not isinstance(warnings[field], field_type):
                return False
    return True


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
