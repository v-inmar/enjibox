from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from app.utils.decorator_utils import auth_required
from app.forms.settings_forms import SettingsCurrencyForm
from app.utils.route_utils.settings_utils import edit_currency_util
from app.utils.route_utils.abort_utils import util_abort

@auth_required
def currency():
    currency = current_user.get_currency().value 
    currency_form = SettingsCurrencyForm(symbol=currency)
    if currency_form.validate_on_submit():
        if not edit_currency_util(user_obj=current_user, currency=currency_form.currency.data.strip()):
            util_abort(
                code=500,
                client_msg="Server Error. Try again later",
                log_msg=f"edit_currency_util() return invalid for user with id: {current_user.id} and currency: {currency_form.currency.data.strip()}"
            )
        flash(message="Currency Saved!", category="message")
        return redirect(url_for("settings.settings"))
    return render_template("settings/currency.html", form=currency_form)
