import datetime
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from app import db
from flask import current_app
from decimal import Decimal

from app.utils.random_utils import create_random_string
from app.utils.model_utils import util_helper_object_creator
from app.models.outgoing_model import OutgoingModel

from app.models.string_models import OutgoingPIDModel, OutgoingLabelModel, OutgoingCategoryModel, OutgoingFormModel, OutgoingCommentModel
from app.models.numeric_models import OutgoingAmountModel

def create_api_util(user_id: int, label: str, category: str, form: str, amount: Decimal, date: datetime.date, time: Optional[datetime.time], comment: Optional[str], offset: bool) -> OutgoingModel:
    try:
        # PID
        pid_obj = None
        count = 0
        while count < 5:
            pid = create_random_string(maxlength=OutgoingPIDModel.value_max_length)
            if not pid:
                raise ValueError(f"create_random_string() for pid returned False at count: {count}")
            
            pid_obj = OutgoingPIDModel.get_by_value(value=pid)
            if pid_obj is False:
                raise ValueError(f"OutgoingPIDModel.get_by_value() for value: {pid} returned False at count: {count}")

            if pid_obj:
                pid_obj = None # Reset
                pid = None # Reset
                count += 1 # Increment count
                continue
            
            pid_obj = OutgoingPIDModel(value=pid)
            if type(pid_obj) is not OutgoingPIDModel:
                raise TypeError(f"pid_obj is not of type OutgoingPIDModel for value: {pid}. Type: {type(pid_obj)}")
            db.session.add(pid_obj)
            db.session.flush()
            break

        if pid_obj is None:
            raise ValueError("pid_obj is None")
        
        # Label
        label_obj = util_helper_object_creator(class_model=OutgoingLabelModel, value=label)
        if not label_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {label_obj} for class model: OutgoingLabelModel with value: {label}")
        
        # Category
        cat_obj = util_helper_object_creator(class_model=OutgoingCategoryModel, value=category)
        if not cat_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {cat_obj} for class model: OutgoingCategoryModel with value: {category}")
        
        # Form
        form_obj = util_helper_object_creator(class_model=OutgoingFormModel, value=form)
        if not form_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {form_obj} for class model: OutgoingFormModel with value: {form}")
        
        # Amount
        amount_obj = util_helper_object_creator(class_model=OutgoingAmountModel, value=amount)
        if not amount_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {amount_obj} for class model: OutgoingAmountModel with value: {amount}")
        

        
        # Comment
        comment_obj = None
        if comment:
            comment_obj = util_helper_object_creator(class_model=OutgoingCommentModel, value=comment)
            if not comment_obj:
                raise ValueError(f"util_helper_object_creator() returned invalid value: {comment_obj} for class model: OutgoingCommentModel with value: {comment}")
        
        
        # Outgoing
        outgoing_obj = OutgoingModel(
            user_id=user_id,
            pid_id=pid_obj.id,
            label_id=label_obj.id,
            form_id=form_obj.id,
            category_id=cat_obj.id,
            amount_id=amount_obj.id,
            date=date,
            time=time,
            comment_id=comment_obj.id if comment_obj else None,
            offset=offset
        )

        if type(outgoing_obj) is not OutgoingModel:
            raise TypeError(f"outgoing_obj is not of type OutgoingModel. Type: {type(outgoing_obj)}")
        db.session.add(outgoing_obj)
        db.session.commit()
        return outgoing_obj
    except (SQLAlchemyError, ValueError, TypeError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False

def update_api_utils(outgoing_obj: OutgoingModel, label: str, category: str, form: str, amount: Decimal, date: datetime.date, time: Optional[datetime.time], comment: Optional[str], offset: bool) -> OutgoingModel:
    try:
        # Label
        label_obj = util_helper_object_creator(class_model=OutgoingLabelModel, value=label)
        if not label_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {label_obj} for class model: OutgoingLabelModel with value: {label}")
        
        # Category
        cat_obj = util_helper_object_creator(class_model=OutgoingCategoryModel, value=category)
        if not cat_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {cat_obj} for class model: OutgoingCategoryModel with value: {category}")
        
        # Form
        form_obj = util_helper_object_creator(class_model=OutgoingFormModel, value=form)
        if not form_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {form_obj} for class model: OutgoingFormModel with value: {form}")
        
        # Amount
        amount_obj = util_helper_object_creator(class_model=OutgoingAmountModel, value=amount)
        if not amount_obj:
            raise ValueError(f"util_helper_object_creator() returned invalid value: {amount_obj} for class model: OutgoingAmountModel with value: {amount}")

        
        # Comment
        comment_obj = None
        if comment:
            comment_obj = util_helper_object_creator(class_model=OutgoingCommentModel, value=comment)
            if not comment_obj:
                raise ValueError(f"util_helper_object_creator() returned invalid value: {comment_obj} for class model: OutgoingCommentModel with value: {comment}")
        

        outgoing_obj.label_id = label_obj.id
        outgoing_obj.amount_id = amount_obj.id
        outgoing_obj.category_id = cat_obj.id
        outgoing_obj.form_id = form_obj.id
        outgoing_obj.date = date
        outgoing_obj.time = time
        outgoing_obj.comment_id = comment_obj.id if comment_obj else None
        outgoing_obj.offset = offset
        outgoing_obj.last_edited = datetime.datetime.utcnow()
        db.session.commit()
        return outgoing_obj
    except (SQLAlchemyError, ValueError, TypeError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False


def delete_api_utils(outgoing_obj: OutgoingModel) -> bool:
    try:
        outgoing_obj.date_deleted = datetime.datetime.utcnow()
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(msg=e, exc_info=1)
        return False


