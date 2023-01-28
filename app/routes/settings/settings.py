from flask import render_template
from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.random_utils import hide_email_util

@auth_required
def settings():
    account = {
        "firstname": current_user.get_firstname().value,
        "lastname": current_user.get_lastname().value,
        "email": hide_email_util(email=current_user.get_email().value),
        "currency": current_user.get_currency().value
    }
    return render_template("settings/settings.html", account=account)