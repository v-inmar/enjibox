from flask import url_for
from flask import redirect
from flask_login import logout_user

from app.utils.decorator_utils import auth_required

@auth_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
