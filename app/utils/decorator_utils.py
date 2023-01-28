from functools import wraps

from flask_login import current_user
from flask import redirect
from flask import url_for
from flask import request

def auth_required(func):
    '''
    Decorator to redirect users to login page if not authenticated
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        return func(*args, **kwargs)
    return wrapper

