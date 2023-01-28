import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from app.models.base_model import BaseModel
from app import db

class StringModelMixin:

    @classmethod
    def get_by_value(cls, value: str):
        f'''
        Class Method: Returns model object

        @param value - String
        '''
        try:
            return cls.query.filter(cls.value == value).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    @classmethod
    def get_all_like_value(cls, value: str):
        '''
        Returns list of cls objects after using a "ilike" query. Note "ilike" is case insensitive

        @param: value - String
        '''
        try:
            if value:
                return cls.query.filter(cls.value.ilike("%"+value+"%")).all()
            return []
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False


class UserFirstnameModel(BaseModel, StringModelMixin):
    '''
    ORM class for firstname
    '''
    
    value_max_length: int = 32
    __tablename__ = "user_firstname_model"

    # case sensitive i.e. Firstname != firstname
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class UserLastnameModel(BaseModel, StringModelMixin):
    '''
    ORM Class for lastname
    '''
    
    value_max_length: int = 32
    __tablename__ = "user_lastname_model"

    # case sensitive i.e. Lastname != lastname
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class UserTokenModel(BaseModel, StringModelMixin):
    '''
    ORM class for token. This token is used for user authentication.

    Change password must also change this token to ensure all user clients will be logged out
    '''
    value_max_length: int = 64
    __tablename__ = "user_token_model"
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False, unique=True)

    def __init__(self, value:str) -> None:
        super().__init__()
        self.value=value


class UserPIDModel(BaseModel, StringModelMixin):
    '''
    ORM class for public id value of the user
    '''

    # Maximum length of the string
    value_max_length: int = 32

    __tablename__ = "user_pid_model"

    value = db.Column(db.String(value_max_length), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class UserEmailModel(BaseModel, StringModelMixin):
    '''
    ORM class for email address value of the user
    '''
    value_max_length: int = 128
    __tablename__ = "user_email_model"
    value = db.Column(db.String(value_max_length), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        # email address must be stored as lowercased values
        self.value = str(value).lower()


class UserPasswordModel(BaseModel, StringModelMixin):
    '''
    ORM class for password value of the user. The value is hashed
    '''
    value_max_length: int = 128

    __tablename__ = "user_password_model"
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False)
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value # hashed password
    
    def checkpw(self, password: str) -> bool:
        '''
        Return boolean for checking the password

        @param password - String value
        '''
        return bcrypt.checkpw(password=str(password).encode("utf8"), hashed_password=str(self.value).encode("utf8"))

class UserCurrencyModel(BaseModel, StringModelMixin):
    '''
    ORM class for user's currency
    '''
    value_max_length = 4

    __tablename__ = "user_currency_model"
    # case sensitive i.e. Currency != currency
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False)
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

class OutgoingPIDModel(BaseModel, StringModelMixin):
    '''
    ORM class for public id value of the outgoing
    '''

    # Maximum length of the string
    value_max_length: int = 32

    __tablename__ = "outgoing_pid_model"

    value = db.Column(db.String(value_max_length), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class OutgoingLabelModel(BaseModel, StringModelMixin):
    '''
    ORM class for the label of the outgoing
    '''

    # Maximum length of the string
    value_max_length: int = 128

    __tablename__ = "outgoing_label_model"

    # case sensitive i.e. Label != label
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value
    

    # @classmethod
    # def get_all_like_value(cls, value: str):
    #     '''
    #     Returns list of cls objects after using a "ilike" query. Note "ilike" is case insensitive

    #     @param: value - String
    #     '''
    #     try:
    #         if value:
    #             return cls.query.filter(cls.value.ilike("%"+value+"%")).all()
    #         return []
    #     except SQLAlchemyError as e:
    #         current_app.logger.error(msg=e, exc_info=1)
    #         return False


class OutgoingCategoryModel(BaseModel, StringModelMixin):
    """
    ORM class for the category of the outgoing
    """

    # Maximum length of the string
    value_max_length: str = 32

    __tablename__ = "outgoing_category_model"

    # case sensitive i.e. Category != category
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False, unique=True)

    def __init__(self, value:str) -> None:
        super().__init__()
        self.value=value



class OutgoingFormModel(BaseModel, StringModelMixin):
    """
    ORM class for the form of the outgoing
    i.e. Cash, Card (Debit), etc
    """

    # Maximum length of the string
    value_max_length: str = 32

    __tablename__ = "outgoing_form_model"

    # case sensitive i.e. Form != form
    value = db.Column(db.String(value_max_length, collation="utf8mb4_0900_as_cs"), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value=value


class OutgoingCommentModel(BaseModel, StringModelMixin):
    """
    ORM class for the comment of the outgoing
    """

    # Maximum length of the string
    value_max_length = 10000

    __tablename__ = "outgoing_comment_model"
    
    value = db.Column(db.Text, nullable=False)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value=value


class ContactPIDModel(BaseModel, StringModelMixin):
    value_max_length: int = 8

    __tablename__ = "contact_pid_model"

    value = db.Column(db.String(value_max_length), nullable=False, unique=True)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class ContactMessageModel(BaseModel, StringModelMixin):
    value_max_length = 20000
    __tablename__ = "contact_message_model"
    value = db.Column(db.Text, nullable=False)

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value=value