from flask_mail import Message
from app import mail, celery
from flask import current_app, json


@celery.task
def send_email_util(subject: str, text_body: str, html_body: str, recipients: list[str]) -> None:
    '''
    Sends email decorated as a celery task for background processing
    '''
    app = current_app._get_current_object()
    with app.app_context():
        msg = Message(subject=subject, sender=app.config["MAIL_SENDER"], recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)