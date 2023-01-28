from __future__ import annotations
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin
from flask import current_app
from app.models.base_model import BaseModel
from app import db
from sqlalchemy.dialects.mysql import DATETIME

from app.models.string_models import UserTokenModel, UserPasswordModel, UserEmailModel, UserPIDModel, UserFirstnameModel, UserLastnameModel, UserCurrencyModel

class UserModel(BaseModel, UserMixin):
    '''
    ORM class for the user model
    '''
    __tablename__ = "user_model"

    token_id = db.Column(db.BigInteger, db.ForeignKey("user_token_model.id"), nullable=False, unique=True)
    pid_id = db.Column(db.BigInteger, db.ForeignKey("user_pid_model.id"), nullable=False, unique=True)
    email_id = db.Column(db.BigInteger, db.ForeignKey("user_email_model.id"), nullable=False, unique=True)
    password_id = db.Column(db.BigInteger, db.ForeignKey("user_password_model.id"), nullable=False)
    firstname_id = db.Column(db.BigInteger, db.ForeignKey("user_firstname_model.id"), nullable=False)
    lastname_id = db.Column(db.BigInteger, db.ForeignKey("user_lastname_model.id"), nullable=False)
    currency_id = db.Column(db.BigInteger, db.ForeignKey("user_currency_model.id"), nullable=False)
    verified = db.Column(DATETIME(fsp=6), nullable=True)
    deactivated = db.Column(DATETIME(fsp=6), nullable=True)

    def __init__(self, token_id: int, pid_id: int, email_id: int, password_id: int, firstname_id: int, lastname_id: int, currency_id) -> None:
        super().__init__()
        self.token_id = token_id
        self.pid_id = pid_id
        self.email_id = email_id
        self.password_id = password_id
        self.firstname_id = firstname_id
        self.lastname_id = lastname_id
        self.currency_id = currency_id
        self.deactivated = None
        self.verified = None
    
    def get_id(self):
        '''
        Returns string or None.
        This overrides the Flask-Login UserMixin get_id method
        '''
        try:
            return UserTokenModel.get_by_id(id=self.token_id).value
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return None
    

    def get_email(self):
        '''
        Returns UserEmailModel object
        '''
        try:
            return UserEmailModel.get_by_id(id=self.email_id)
            # return UserEmailModel.query.filter(id==self.email_id).first()
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    def get_pid(self):
        '''
        Returns UserPIDModel object
        '''
        try:
            return UserPIDModel.get_by_id(id=self.pid_id)
            # return UserPIDModel.query.filter(id==self.pid_id).first()
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    def get_password(self):
        '''
        Returns UserPasswordModel object
        '''
        try:
            return UserPasswordModel.get_by_id(id=self.password_id)
            # return UserPasswordModel.query.filter(id=self.password_id).first()
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    def get_firstname(self):
        '''
        Returns UserFirstnameModel object
        '''
        try:
            return UserFirstnameModel.get_by_id(id=self.firstname_id)
            # return UserFirstnameModel.query.filter(id==self.firstname_id).first()
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    def get_lastname(self):
        '''
        Returns UserLastnameModel object
        '''
        try:
            return UserLastnameModel.get_by_id(id=self.lastname_id)
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    def get_currency(self):
        '''
        Returns UserCurrencyModel object
        '''
        try:
            return UserCurrencyModel.get_by_id(id=self.currency_id)
        except Exception as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    @classmethod
    def get_user_by_token_id(cls, token_id: int) -> UserModel:
        '''
        Returns UserModel object that matches the token_id param

        @param token_id: Integer
        '''
        try:
            return cls.query.filter(cls.token_id == token_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    @classmethod
    def get_user_by_email_id(cls, email_id: int) -> UserModel:
        '''
        Returns UserModel object that matches the email_id param

        @param email_id: Integer
        '''
        try:
            return cls.query.filter(cls.email_id == email_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    

    # @classmethod
    # def get_user_by_email(cls, email:str) -> UserModel:
    #     '''
    #     Returns UserModel object

    #     @param email: string email address, must be stripped and lowercased
    #     '''
    #     try:
    #         email_obj = UserEmailModel.get_by_value(value=email)
    #         if email_obj is False:
    #             raise ValueError(f"UserEmailModel.get_by_value() returned False for email value: {email}")
            
    #         if email_obj is None:
    #             return None
            
    #         return cls.query.filter(cls.email_id == email_obj.id).first()
    #     except (SQLAlchemyError, ValueError) as e:
    #         current_app.logger.error(msg=e, exc_info=1)
    #         return False
    # @classmethod
    # def get_by_email(cls, email: str) -> UserModel:
    #     '''
    #     Class Method: Returns UserEmailModel object that matches the email

    #     @param: email - String
    #     '''
    #     try:
    #         email_obj = UserEmailModel.get_by_value(value=email)
    #         if email_obj is False:
    #             raise ValueError("UserEmailModel.get_by_value() returned False")
            
    #         if email_obj is None:
    #             return None
            
    #         return cls.query.filter(cls.email_id == email_obj.id).first() or None
    #     except SQLAlchemyError as e:
    #         current_app.logger.error(msg=e, exc_info=1)
    #         return False
    
    # @classmethod
    # def get_by_pid(cls, pid: str) -> UserModel:
    #     '''
    #     Class Method: Returns UserModel object that matches the pid

    #     @param: pid = String
    #     '''
    #     try:
    #         return cls.query.filter(cls.pid == pid).first() or None
    #     except SQLAlchemyError as e:
    #         current_app.logger.error(msg=e, exc_info=1)
    #         return False
    
    # @classmethod
    # def get_by_token(cls, token: str) -> UserModel:
    #     '''
    #     Class Method: Returns UserModel object that matches the token

    #     @param: token = String
    #     '''
    #     try:
    #         return cls.query.filter(cls.token == token).first() or None
    #     except SQLAlchemyError as e:
    #         current_app.logger.error(msg=e, exc_info=1)
    #         return False