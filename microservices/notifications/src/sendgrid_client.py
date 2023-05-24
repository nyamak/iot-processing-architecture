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
        print(e.to_dict)
        return False


def build_mail(notification_payload):
    return Mail(
        from_email=os.environ.get("SENDGRID_FROM_EMAIL"),
        to_emails=os.environ.get("SENDGRID_TO_EMAIL"),
        subject=_generate_subject(
            notification_payload["machine_id"], notification_payload["warnings"]
        ),
        html_content=_generate_email_content(notification_payload),
    )


def _generate_subject(machine_id, warnings):
    if len(warnings) == 1:
        subject = f"{warnings[0]['type'].title()} warning"
    else:
        subject = f"{len(warnings)} warnings"
    return subject + f" - Machine ID: {machine_id}"


def _generate_email_content(notification_payload):
    body = f"""
<h1 style="text-align:center">Warning(s):</h1>
<p style="text-align:center"><strong>Machine ID:</strong> {notification_payload['machine_id']}</p>
<p style="text-align:center"><strong>Datetime</strong>: {notification_payload['created_at']}</p>
"""
    for warning in notification_payload.get("warnings"):
        body += f"""<p style="text-align:center"><strong>{warning['type'].title()}</strong>: {warning['current_value']} {warning['unit']} ({warning['target_value']})</p>
"""
    return body
