from config import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_to_sendgrid(notification_payloads):
    message = build_notifications_mail(notification_payloads)
    try:
        sg = SendGridAPIClient(config["SENDGRID_API_KEY"])
        response = sg.send(message)
        print("Calling Sendgrid:")
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(e.to_dict)
        return False


def build_notifications_mail(notification_payloads):
    return Mail(
        from_email=config["SENDGRID_FROM_EMAIL"],
        to_emails=config["SENDGRID_TO_EMAIL"],
        subject=f"Report: {len(notification_payloads)} warning(s)",
        html_content=_generate_multiple_notifications_email_content(
            notification_payloads
        ),
    )


def _generate_multiple_notifications_email_content(notification_payloads):
    body = '<h1 style="text-align:center">Warning(s):</h1>\n'
    for payload in notification_payloads.values():
        body += f"""<p><strong>Machine ID:</strong> {payload['machine_id']}</p>
<p style="margin-left:40px"><strong>Datetime</strong>: {payload['created_at']}</p>
"""
        for warning in payload.get("warnings"):
            body += f"""<p style="margin-left:40px"><strong>{warning['type'].title()}</strong>: {warning['current_value']:.2f} {warning['unit']} ({warning['target_value']:.2f})</p>
"""
    return body
