from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from app import login_manager
from app.models.user_model import UserModel
from app.models.string_models import UserTokenModel

@login_manager.user_loader
def load_user(token):
    '''
    Returns the UserModel object that owns the token or None

    @param token: string
    '''
    try:
        token_obj = UserTokenModel.get_by_value(value=token)
        if token_obj:
            user_obj = UserModel.get_user_by_token_id(token_id=token_obj.id)
            if user_obj:
                return user_obj
        return None
    except ValueError as e:
        current_app.logger.error(msg=e, exc_info=1)
        return None

