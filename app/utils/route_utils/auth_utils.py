import datetime
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, current_app
from app import db
from app.utils.email_utils import send_email_util
from app.utils.random_utils import create_random_string
from app.utils.model_utils import util_helper_object_creator
from app.utils.route_utils.settings_utils import edit_password_util
from app.models.user_model import UserModel
from app.models.string_models import UserFirstnameModel, UserLastnameModel, UserTokenModel, UserPIDModel, UserPasswordModel, UserEmailModel, UserCurrencyModel


def signup_util(firstname: str, lastname: str, email: str, password: str, currency: str) -> UserModel:
    """
    Returns a newly created UserModel object. This function is a utility for creating new users during sign up

    @param firstname: string
    @param lastname: string
    @param email: string
    @param password: string
    @param symbol: string
    """
    try:
        # Deals with PID
        count = 0
        pid_obj = None
        while count < 5:
            pid = create_random_string(maxlength=UserPIDModel.value_max_length)
            if not pid:
                raise ValueError(f"create_random_string() for pid returned False at count: {count}")

            obj = UserPIDModel.get_by_value(value=pid)
            if obj is False:
                raise ValueError(f"UserPIDModel.get_by_value() returned False at count: {count} for pid: {pid}")
            
            if obj:
                count += 1 # increment
                pid = None # reset
                pid_obj = None # reset 
                continue
            else:
                pid_obj = UserPIDModel(value=pid)
                db.session.add(pid_obj)
                db.session.flush()
                break

        if pid_obj is None:
            raise ValueError("pid_obj is None after loop")
        
        # Deals with Token
        count = 0
        token_obj = None
        while count < 5:
            token = create_random_string(maxlength=UserTokenModel.value_max_length)
            if not token:
                raise ValueError(f"create_random_string() for token returned False at count: {count}")

            obj = UserTokenModel.get_by_value(value=token)
            if obj is False:
                raise ValueError(f"UserTokenModel.get_by_value returned False at count: {count} for token: {token}")
            
            if obj:
                token = None # reset
                token_obj = None # reset
                count += 1 # increment
                continue
            else:
                token_obj = UserTokenModel(value=token)
                db.session.add(token_obj)
                db.session.flush()
                break

        if token_obj is None:
            raise ValueError("token_obj is None after loop")
        
        # Deals with Firstname
        firstname_obj = util_helper_object_creator(class_model=UserFirstnameModel, value=firstname)
        if not firstname_obj:
            raise ValueError(f"firstname_obj has an invalid value: {firstname_obj} for the firstname value: {firstname}")
        
        # Deals with Lastname
        lastname_obj = util_helper_object_creator(class_model=UserLastnameModel, value=lastname)
        if not lastname_obj:
            raise ValueError(f"lastname_obj has an invalid value: {lastname_obj} for the lastname value: {lastname}")
        
        # Deals with Currency
        currency_obj = util_helper_object_creator(class_model=UserCurrencyModel, value=currency)
        if not currency_obj:
            raise ValueError(f"currency_obj has an invalid value: {currency_obj} for the currency value: {currency_obj}")
        
        # Deals with Email
        email_obj = UserEmailModel.get_by_value(value=email)
        if email_obj is False:
            raise ValueError("email_obj is False")
        
        if email_obj:
            user_email_obj = UserModel.get_user_by_email_id(email_id=email_obj.id)
            if user_email_obj is False:
                raise ValueError(f"user_email_obj is False for the email id: {email_obj.id}")
            
            if user_email_obj:
                raise ValueError(f"user_email_obj is not None which means the email is already in use")
        else:
            email_obj = UserEmailModel(value=email)
            db.session.add(email_obj)
            db.session.flush()
        
        #  Deals with Password
        hashed_pword = bcrypt.hashpw(password=str(password).encode("utf8"), salt=bcrypt.gensalt())
        password_obj = util_helper_object_creator(class_model=UserPasswordModel, value=hashed_pword)
        if not password_obj:
            raise ValueError(f"password_obj has an invalid value: {password_obj} for the password hash value: {hashed_pword}")


        # Deals with User
        user_obj = UserModel(
            token_id=token_obj.id,
            pid_id=pid_obj.id,
            email_id=email_obj.id,
            password_id=password_obj.id,
            firstname_id=firstname_obj.id,
            lastname_id=lastname_obj.id,
            currency_id=currency_obj.id
        )
        db.session.add(user_obj)
        db.session.commit()

        
        token = URLSafeTimedSerializer(secret_key=current_app.config["SERIALIZER_KEY"]).dumps(obj=email, salt=current_app.config["VERIFY_SERIALIZER_SALT"])
        send_email_util.delay(
            subject=f"Welcome To {current_app.config['APP_NAME']}",
            recipients=[email],
            text_body=render_template("email_service/verify_email/body.txt", token=token),
            html_body=render_template("email_service/verify_email/body.html", token=token)
        )
        return user_obj
    except (SQLAlchemyError, ValueError, TypeError, Exception) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False


def verify_email_util(user_obj: UserModel) -> UserModel:
    """
    Returns UserModel object after inserting utc datetime to the verified field

    @param user_obj: UserModel object
    """
    try:
        user_obj.verified = datetime.datetime.utcnow()
        db.session.commit()
        return user_obj
    except SQLAlchemyError as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False


def request_verification_util(email: str) -> bool:
    '''
    Returns True after sending a new verification link to the @param email

    @param email: str
    '''
    try:
        token = URLSafeTimedSerializer(secret_key=current_app.config["SERIALIZER_KEY"]).dumps(obj=email, salt=current_app.config["VERIFY_SERIALIZER_SALT"])
        send_email_util.delay(
            subject=f"Verify Email Address",
            recipients=[email],
            text_body=render_template("email_service/verify_email/body.txt", token=token),
            html_body=render_template("email_service/verify_email/body.html", token=token)
        )
        return True
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False


def forgot_password_util(email: str) -> bool:
    try:
        token = URLSafeTimedSerializer(secret_key=current_app.config["SERIALIZER_KEY"]).dumps(obj=email, salt=current_app.config["FORGOT_PASSWORD_SERIALIZER_SALT"])
        send_email_util.delay(
            subject=f"Reset Password",
            recipients=[email],
            text_body=render_template("email_service/forgot_password/body.txt", token=token),
            html_body=render_template("email_service/forgot_password/body.html", token=token)
        )
        return True
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False


def reset_password_util(user_obj: UserModel, password: str) -> bool:
    try:
        # Uses the edit password util within the settings feature
        if not edit_password_util(user_obj=user_obj, password=password):
            raise ValueError(f"edit_password_util() returned False for user id: {user_obj.id} during within reset_password_util")
        return True
    except SQLAlchemyError as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False