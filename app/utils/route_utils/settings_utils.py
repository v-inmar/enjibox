import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, render_template
from app import db

from app.utils.model_utils import util_helper_object_creator
from app.utils.random_utils import create_random_string
from app.utils.email_utils import send_email_util
from app.models.user_model import UserModel
from app.models.string_models import UserFirstnameModel, UserLastnameModel, UserTokenModel, UserEmailModel, UserPasswordModel, UserCurrencyModel

def edit_name_util(user_obj: UserModel, firstname: Optional[str], lastname: Optional[str]) -> UserModel:
    '''
    Returns UserModel object

    @param user_obj: UserModel object
    @param firstname: Optional string or None
    @param lastname: Optional string or None
    '''
    try:
        if firstname is None and lastname is None:
            return user_obj
        
        firstname_id = None
        if firstname:
            fname_obj = util_helper_object_creator(class_model=UserFirstnameModel, value=firstname)
            if not fname_obj:
                raise ValueError(f"util_helper_object_creator() returned invalid value: {fname_obj} for firstname value: {firstname}")
            
            firstname_id = fname_obj.id
        
        lastname_id = None
        if lastname:
            lname_obj = util_helper_object_creator(class_model=UserLastnameModel, value=lastname)
            if not lname_obj:
                raise ValueError(f"util_helper_object_creator() returned invalid value: {lname_obj} for lastname value: {lastname}")
            lastname_id = lname_obj.id
        
        current_fname_id = user_obj.firstname_id
        current_lname_id = user_obj.lastname_id

        user_obj.firstname_id = firstname_id if firstname_id else current_fname_id
        user_obj.lastname_id = lastname_id if lastname_id else current_lname_id
        db.session.commit()
        return user_obj
    except (SQLAlchemyError, ValueError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False


def edit_email_util(user_obj: UserModel, email: str) -> UserModel:
    '''
    Returns UserMode object

    @param user_obj: UserModel object
    @param email: string
    '''
    try:
        # Deals with Email
        email_obj = UserEmailModel.get_by_value(value=email)
        if email_obj is False:
            raise ValueError(f"UserEmailModel.get_by_value() returned False for email value: {email}")
        
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
        
        user_obj.token_id = token_obj.id
        user_obj.email_id = email_obj.id
        user_obj.verified = None
        db.session.commit()


        token = URLSafeTimedSerializer(secret_key=current_app.config["SERIALIZER_KEY"]).dumps(obj=email, salt=current_app.config["VERIFY_SERIALIZER_SALT"])
        send_email_util.delay(
            subject=f"Email Address Changed",
            recipients=[email],
            text_body=render_template("email_service/verify_email/body.txt", token=token),
            html_body=render_template("email_service/verify_email/body.html", token=token)
        )
        return user_obj
    except (SQLAlchemyError, ValueError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False


def edit_password_util(user_obj: UserModel, password: str) -> UserModel:
    '''
    Returns UserModel object

    @param user_obj: UserModel
    @param password: string
    '''
    try:
        #  Deals with Password
        hashed_pword = bcrypt.hashpw(password=str(password).encode("utf8"), salt=bcrypt.gensalt())
        password_obj = util_helper_object_creator(class_model=UserPasswordModel, value=hashed_pword)
        if not password_obj:
            raise ValueError(f"password_obj has an invalid value: {password_obj} for the password: {password} with hash value: {hashed_pword} ")
        
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
        
        user_obj.token_id = token_obj.id
        user_obj.password_id = password_obj.id
        db.session.commit()

        email = user_obj.get_email().value if user_obj.get_email() else None

        if email:
            send_email_util.delay(
                subject="Password Changed",
                text_body=render_template("email_service/password_change/body.txt"),
                html_body=render_template("email_service/password_change/body.html"),
                recipients=[email]
            )
        return user_obj
    except (SQLAlchemyError, ValueError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False


def edit_currency_util(user_obj: UserModel, currency: str) -> UserModel:
    '''
    Returns UserModel object

    @param user_obj: UserModel
    @param currency: string
    '''
    try:
        currency_obj = util_helper_object_creator(class_model=UserCurrencyModel, value=currency)
        if not currency_obj:
            raise ValueError(f"currency_obj has an invalid value: {currency_obj} for the currency: {currency}")
        
        user_obj.currency_id = currency_obj.id
        db.session.commit()
        return user_obj
    except (SQLAlchemyError, ValueError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False