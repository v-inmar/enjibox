import datetime
from typing import Union
from calendar import monthrange
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, asc, and_
from flask import current_app
from app.models.base_model import BaseModel
from app import db

class DateAndTimeModelMixin:
    @classmethod
    def get_by_value(cls, value: Union[datetime.date, datetime.time]):
        try:
            return cls.query.filter(cls.value == value).first() or None
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False




class OutgoingDateModel(BaseModel, DateAndTimeModelMixin):
    """
    ORM class for the date of the outgoing
    """

    __tablename__ = "outgoing_date_model"

    value = db.Column(db.Date, nullable=False, unique=True)

    def __init__(self, value: datetime.date) -> None:
        super().__init__()
        self.value=value
    
    @classmethod
    def get_by_month_and_year(cls, month: int, year: int) -> list:
        '''
        Class Method: Returns list of DateModel object that matches the month and year

        Descending Order

        @param month - Integer representation of the month i.e. 1 == January, etc
        @param year - Integer representation of the year i.e. 2022, etc
        '''
        try:
            num_days = monthrange(year, month)[1] # get the maximum days for the given month and year
            return cls.query.filter(
                and_(
                    cls.value >= datetime.date(year=year, month=month, day=1),
                    cls.value <= datetime.date(year=year, month=month, day=num_days)
                )
            ).order_by(cls.value.desc()).all() or None
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    @classmethod
    def get_ids_by_month_and_year(cls, month: int, year: int) -> list[int]:
        '''
        Class Method: Returns list of DateModel object ids that matches the month and year

        Descending Order

        @param month - Integer representation of the month i.e. 1 == January, etc
        @param year - Integer representation of the year i.e. 2022, etc
        '''
        try:
            ids: list[int] = []
            num_days = monthrange(year, month)[1] # get the maximum days for the given month and year
            objs = cls.query.filter(
                and_(
                    cls.value >= datetime.date(year=year, month=month, day=1),
                    cls.value <= datetime.date(year=year, month=month, day=num_days)
                )
            ).order_by(desc(cls.value)).all() or None

            if objs:
                for obj in objs:
                    ids.append(obj.id)
            return ids
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False


class OutgoingTimeModel(BaseModel, DateAndTimeModelMixin):
    """
    ORM class for the time of the outgoing
    """

    __tablename__ = "outgoing_time_model"

    value = db.Column(db.Time, nullable=False, unique=True)

    def __init__(self, value: datetime.time) -> None:
        super().__init__()
        self.value=value