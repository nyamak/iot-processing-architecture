import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_to_sendgrid(notification_payload):
    message = build_mail(notification_payload)
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(e.message)
        return False


def build_mail(notification_payload):
    if len(notification_payload) == 1:
        subject = f"{notification_payload[0]['type']} - Machine ID: {notification_payload[0]['machine_id']}"
    else:
        subject = f"{len(notification_payload)} warnings - Machine ID: {notification_payload[0]['machine_id']}"

    return Mail(
        from_email=os.environ.get("SENDGRID_FROM_EMAIL"),
        to_emails=os.environ.get("SENDGRID_TO_EMAIL"),
        subject=subject,
        html_content="""
        <strong>and easy to do anywhere, even with Python</strong>
        """,
    )
