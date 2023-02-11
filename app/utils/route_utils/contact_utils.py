import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from flask import current_app, render_template

from app.utils.email_utils import send_email_util
from app.utils.random_utils import create_random_string
from app.utils.model_utils import util_helper_object_creator
from app.models.contact_model import ContactModel
from app.models.string_models import ContactPIDModel, UserFirstnameModel, UserLastnameModel, ContactMessageModel, UserEmailModel

def message_util(firstname: str, lastname: str, email: str, message: str) -> bool:
    try:
        # Deals with PID
        count = 0
        pid_obj = None
        while count < 5:
            pid = create_random_string(maxlength=ContactPIDModel.value_max_length)
            if not pid:
                raise ValueError(f"create_random_string() for pid returned False at count: {count}")

            obj = ContactPIDModel.get_by_value(value=pid)
            if obj is False:
                raise ValueError(f"ContactPIDModel.get_by_value() returned False at count: {count} for pid: {pid}")
            
            if obj:
                count += 1 # increment
                pid = None # reset
                pid_obj = None # reset 
                continue
            else:
                pid_obj = ContactPIDModel(value=pid)
                db.session.add(pid_obj)
                db.session.flush()
                break

        if pid_obj is None:
            raise ValueError("pid_obj is None after loop")
        
        # Deals with Firstname
        firstname_obj = util_helper_object_creator(class_model=UserFirstnameModel, value=firstname)
        if not firstname_obj:
            raise ValueError(f"firstname_obj has an invalid value: {firstname_obj} for the firstname value: {firstname}")
        
        # Deals with Lastname
        lastname_obj = util_helper_object_creator(class_model=UserLastnameModel, value=lastname)
        if not lastname_obj:
            raise ValueError(f"lastname_obj has an invalid value: {lastname_obj} for the lastname value: {lastname}")

        # Deals with email
        email_obj = util_helper_object_creator(class_model=UserEmailModel, value=email.strip().lower())
        if not email_obj:
            raise ValueError(f"email_obj has an invalid value: {email_obj}")
        
        # Deals with Message
        message_obj = util_helper_object_creator(class_model=ContactMessageModel, value=message)
        if not message_obj:
            raise ValueError(f"message_obj has an invalid value: {message_obj}")


        contact_obj = ContactModel(
            pid_id=pid_obj.id,
            firstname_id=firstname_obj.id,
            lastname_id=lastname_obj.id,
            email_id=email_obj.id,
            message_id=message_obj.id
        )
        db.session.add(contact_obj)
        db.session.commit()

        # Send to user
        send_email_util.delay(
            subject=f"Thank you for your message",
            recipients=[email],
            text_body=render_template("email_service/contact/body.txt", pid=pid_obj.value, firstname=firstname, message=message, app_name=current_app.config['APP_NAME']),
            html_body=render_template("email_service/contact/body.html", pid=pid_obj.value, firstname=firstname, message=message, app_name=current_app.config['APP_NAME'])
        )

        # Send to admin/support
        send_email_util.delay(
            subject=f"New Message",
            recipients=[current_app.config["MAIL_ADMIN"]],
            text_body=render_template(
                "email_service/contact/to_support/body.txt",
                pid=pid_obj.value,
                firstname=firstname,
                lastname=lastname,
                email=email,
                date_time=datetime.datetime.utcnow(),
                message=message_obj.value
            ),
            html_body=render_template(
                "email_service/contact/to_support/body.html",
                pid=pid_obj.value,
                firstname=firstname,
                lastname=lastname,
                email=email,
                date_time=datetime.datetime.utcnow(),
                message=message_obj.value
            )
        )
        return True
    except (SQLAlchemyError, ValueError, Exception) as e:
        db.session.rollback()
        current_app.logger.error(msg=e, exc_info=1)
        return False