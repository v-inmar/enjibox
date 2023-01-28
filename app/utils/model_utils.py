from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from app import db


def util_helper_object_creator(class_model, value):
    try:
        obj = class_model.get_by_value(value=value)
        if obj is False:
            raise ValueError(f"{class_model}.get_by_value() returned False for value: {value}")
        
        if obj is None:
            obj = class_model(value=value)
            db.session.add(obj)
            db.session.flush()
        return obj
    except (SQLAlchemyError, ValueError) as e:
        current_app.logger.error(msg=e, exc_info=1)
        db.session.rollback()
        return False