import datetime
from sqlalchemy.dialects.mysql import DATETIME
from app import db
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

class BaseModel(db.Model):
    '''
    Abstract ORM class to be inherit by all concrete models
    '''
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    date_created = db.Column(DATETIME(fsp=6), nullable=False)

    def __init__(self) -> None:
        super().__init__()
        self.date_created = datetime.datetime.utcnow()
    
    @classmethod
    def get_by_id(cls, id: int):
        '''
        Class Method: Returns class object

        @param id - Integer representation of object id
        '''
        try:
            return cls.query.filter(cls.id == id).first() or None
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False