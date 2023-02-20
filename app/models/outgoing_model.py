from __future__ import annotations # use for type hinting. MUST GO AT THE VERY TOP
import datetime
from calendar import monthrange
from typing import Optional, List, Union
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, asc, and_
from flask import current_app
from app.models.base_model import BaseModel
from sqlalchemy.dialects.mysql import DATETIME
from app import db

from app.models.date_time_models import OutgoingDateModel, OutgoingTimeModel
from app.models.string_models import OutgoingPIDModel, OutgoingLabelModel, OutgoingCategoryModel, OutgoingFormModel, OutgoingCommentModel
from app.models.numeric_models import OutgoingAmountModel

class OutgoingModel(BaseModel):
    '''
    ORM class for the outgoing model
    '''
    __tablename__ = "outgoing_model"
    user_id = db.Column(db.BigInteger, db.ForeignKey("user_model.id"), nullable=False)
    pid_id = db.Column(db.BigInteger, db.ForeignKey("outgoing_pid_model.id"), nullable=False, unique=True)
    label_id = db.Column(db.BigInteger, db.ForeignKey("outgoing_label_model.id"), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey("outgoing_category_model.id"), nullable=False)
    form_id = db.Column(db.BigInteger, db.ForeignKey("outgoing_form_model.id"), nullable=False)
    amount_id = db.Column(db.BigInteger, db.ForeignKey("outgoing_amount_model.id"), nullable=False)
    comment_id = db.Column(db.BigInteger, db.ForeignKey("outgoing_comment_model.id"), nullable=True)
    offset = db.Column(db.Boolean(), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    last_edited = db.Column(DATETIME(fsp=6), nullable=True)
    date_deleted = db.Column(DATETIME(fsp=6), nullable=True)

    def __init__(self, user_id: int, pid_id: int, label_id: int, form_id: int, category_id: int, amount_id: int, date: datetime.date, time: Optional[datetime.time], comment_id: Optional[int], offset: bool) -> None:
        super().__init__()
        self.user_id = user_id
        self.pid_id = pid_id
        self.label_id = label_id
        self.form_id = form_id
        self.category_id = category_id
        self.amount_id = amount_id
        self.date = date
        self.time = time
        self.comment_id = comment_id
        self.offset = offset
        self.last_edited = None
        self.date_deleted = None
    
    def get_pid(self) -> OutgoingPIDModel:
        '''
        Returns OutgoingPIDModel object
        '''
        try:
            return OutgoingPIDModel.query.filter(OutgoingPIDModel.id == self.pid_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    def get_label(self) -> OutgoingLabelModel:
        '''
        Returns OutgoingLabelModel object
        '''
        try:
            return OutgoingLabelModel.query.filter(OutgoingLabelModel.id == self.label_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    def get_category(self) -> OutgoingCategoryModel:
        '''
        Returns OutgoingCategoryModel object
        '''
        try:
            return OutgoingCategoryModel.query.filter(OutgoingCategoryModel.id == self.category_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    def get_form(self) -> OutgoingFormModel:
        '''
        Returns OutgoingFormModel object
        '''
        try:
            return OutgoingFormModel.query.filter(OutgoingFormModel.id == self.form_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    def get_amount(self) -> OutgoingAmountModel:
        '''
        Returns OutgoingAmountModel object
        '''
        try:
            return OutgoingAmountModel.query.filter(OutgoingAmountModel.id == self.amount_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    def get_comment(self) -> OutgoingCommentModel:
        '''
        Returns OutgoingCommentModel object
        '''
        try:
            return OutgoingCommentModel.query.filter(OutgoingCommentModel.id == self.comment_id).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    @classmethod
    def get_by_pid_id(cls, pid_id: str) -> OutgoingModel:
        '''
        Class Method: Returns OutgoingModel object that matches the pid_id

        @param pid_id - Integer representation of the pid_id
        '''
        try:
            return cls.query.filter(cls.pid_id == pid_id, cls.date_deleted == None).first()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    @classmethod
    def get_all_by_user_id(cls, user_id: int) -> list:
        '''
        Class Method: Returns a list of OutgoingModel objects that matches the user_id.

        This does not include objects that has value for date_deleted.

        @param user_id: Integer that represents the user's id
        '''
        try:
            return cls.query.filter(cls.user_id == user_id, cls.date_deleted == None).all()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    

    @classmethod
    def get_all_by_user_id_with_year(cls, user_id: int, year: int):
        try:
            return cls.query.filter(
                cls.user_id==user_id,
                cls.date_deleted==None,
                and_(
                    cls.date >= datetime.date(year=year, month=1, day=1),
                    cls.date <= datetime.date(year=year, month=12, day=31)
                )
            ).all()
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False

    @classmethod
    def get_paginated_with_filter(cls, user_id: int, label_ids: Optional[List[int]], date_from: datetime.date, date_to: datetime.date, category_id: Optional[int], form_id: Optional[int], page:int=1, per_page:int=100) -> list:
        '''
        Class Method: Returns a paginated list of OutgoingModel objects that matches the params.

        This does not include objects that has value for date_deleted

        Order by date descending

        NOTE: VERY UGLY! FIND A BETTER WAY
        '''
        try:
            if label_ids and category_id and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id,cls.form_id==form_id,cls.label_id.in_(label_ids)).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)
            
            if label_ids is None and category_id and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id,cls.form_id==form_id).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)

            if label_ids is None and category_id is None and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.form_id==form_id).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)
            
            if label_ids is None and category_id is None and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to)).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)
            
            if label_ids and category_id is None and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.label_id.in_(label_ids)).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)
            
            if label_ids and category_id and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id,cls.label_id.in_(label_ids)).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)
            
            if label_ids and category_id is None and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.form_id==form_id,cls.label_id.in_(label_ids)).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)

            if label_ids is None and category_id and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id).order_by(cls.date.desc()).paginate(page=page,per_page=per_page)
            
            return None
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False
    
    @classmethod
    def get_all_with_filter(cls, user_id: int, label_ids: Optional[List[int]], date_from: datetime.date, date_to: datetime.date, category_id: Optional[int], form_id: Optional[int]) -> list:
        '''
        Class Method: Returns a paginated list of OutgoingModel objects that matches the params.

        This does not include objects that has value for date_deleted

        NOTE: VERY UGLY! FIND A BETTER WAY
        '''
        try:
            if label_ids and category_id and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id,cls.form_id==form_id,cls.label_id.in_(label_ids)).all()
            
            if label_ids is None and category_id and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id,cls.form_id==form_id).all()

            if label_ids is None and category_id is None and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.form_id==form_id).all()
            
            if label_ids is None and category_id is None and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to)).all()
            
            if label_ids and category_id is None and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.label_id.in_(label_ids)).all()
            
            if label_ids and category_id and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id,cls.label_id.in_(label_ids)).all()
            
            if label_ids and category_id is None and form_id:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.form_id==form_id,cls.label_id.in_(label_ids)).all()

            if label_ids is None and category_id and form_id is None:
                return cls.query.filter(cls.user_id==user_id,cls.date_deleted==None,and_(cls.date >= date_from,cls.date <= date_to),cls.category_id==category_id).all()
            
            return None
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False