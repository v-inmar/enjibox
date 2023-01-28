from flask_mail import Message
from app import mail, celery
from flask import current_app

@celery.task
def send_email(msg: Message):
    mail.send(message=msg)

def send_email_util(subject: str, text_body: str, html_body: str, recipients: list[str]) -> None:
    print(current_app.config["MAIL_SENDER"])
    app = current_app._get_current_object()
    msg = Message(subject=subject, sender=app.config["MAIL_SENDER"], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_email(msg=msg)