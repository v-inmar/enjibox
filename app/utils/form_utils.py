from wtforms import Field
from flask import current_app

def add_field_error(field: Field, msg: str) -> tuple:
    """
    Returns tuple of errors

    Note: tuple(list(field.errors).append(msg)) fails if the list is empty because object is NoneType.
    So it is done this way

    @param field - wtforms.Field
    @param msg - string
    """
    try:
        new_list = [msg]
        current_error_list = list(field.errors)
        return tuple(current_error_list+new_list)
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False