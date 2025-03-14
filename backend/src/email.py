import smtplib
from email.message import EmailMessage
import os
from flask import current_app, render_template
from .url import create_frontend_url

SMTP_TIMEOUT = 30


def send_email(template, variables, recipients):
    message = EmailMessage()

    subject = render_template(template + "_subject.j2", **variables)
    message.add_header("Subject", subject)

    message.add_header("From", os.environ["SMTP_SENDER"])
    message.add_header("To", recipients)

    content = render_template(template + "_body.j2", **variables)
    message.set_content(content)

    body_html = content.replace("\n", "<br>\n")
    html = render_template("html_container.j2", body_html=body_html)
    message.add_alternative(html, subtype="html")

    current_app.logger.info(f"Sending email: {message.items()}")

    with smtplib.SMTP(
        host=os.environ["SMTP_ADDRESS"],
        port=os.environ["SMTP_PORT"],
        timeout=SMTP_TIMEOUT,
    ) as mailer:
        if os.environ["SMTP_USERNAME"] != "":
            mailer.starttls()
            mailer.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        mailer.send_message(message)


def send_confirmation_email(user_email: str, email_confirmation_passkey: str):
    send_email(
        "confirmation",
        {"link": create_frontend_url(f"confirmation/{email_confirmation_passkey}")},
        user_email,
    )


def send_reset_password_email(user_email: str, email_confirmation_passkey: str):
    send_email(
        "reset_password",
        {"link": create_frontend_url(f"reset_password/{email_confirmation_passkey}")},
        user_email,
    )


def send_approval_email(user_id):
    send_email(
        "approval",
        {"link": create_frontend_url(f"admin/users/{user_id}")},
        os.environ["APPROVER_EMAIL"],
    )


def send_approved_email(user_email):
    send_email("approved", {}, user_email)


def send_access_request_email(status: str):
    send_email(
        "access_request",
        {"status": status},
        os.environ["APPROVER_EMAIL"],
    )
