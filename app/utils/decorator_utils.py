from functools import wraps

from flask_login import current_user
from flask import redirect, url_for, request

def auth_required(func):
    '''
    Decorator to redirect users to login page if not authenticated
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def not_auth_required(func):
    '''
    Decorator to redirect users to home page if authenticated
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("home.home"))
        return func(*args, **kwargs)
    return wrapper