import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

FROM_EMAIL = os.getenv("OUTREACH_FROM_EMAIL")


def send_email(to_email, subject, body):
    """
    Send an email using Resend.
    """

    if not resend.api_key:
        raise ValueError("RESEND_API_KEY not found")

    if not FROM_EMAIL:
        raise ValueError("OUTREACH_FROM_EMAIL not found")

    if not to_email:
        raise ValueError("Recipient email is missing")

    params = {"from": FROM_EMAIL, "to": [to_email], "subject": subject, "text": body}

    response = resend.Emails.send(params)

    return response
