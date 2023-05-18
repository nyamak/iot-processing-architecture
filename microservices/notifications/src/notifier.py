import sendgrid_client
from flask_api import FlaskAPI, request, status

app = FlaskAPI(__name__)


NOTIFICATION_PAYLOAD_SCHEMA = {
    "type": str,
    "machine_id": int,
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
    if not isinstance(notification_payload, list):
        return False
    for subpayload in notification_payload:
        for field, field_type in NOTIFICATION_PAYLOAD_SCHEMA.items():
            if field not in subpayload:
                return False
            if not isinstance(subpayload[field], field_type):
                return False
    return True
