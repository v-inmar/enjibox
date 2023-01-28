from flask import render_template, url_for, redirect, flash
from flask_login import current_user

from app.utils.decorator_utils import auth_required
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.settings_utils import edit_name_util
from app.forms.settings_forms import SettingsNamesForm

@auth_required
def names():


    names_form = SettingsNamesForm(
        firstname=current_user.get_firstname().value,
        lastname=current_user.get_lastname().value
    )
    if names_form.validate_on_submit():
        new_firstname = names_form.firstname.data if names_form.firstname.data != current_user.get_firstname().value else None
        new_lastname = names_form.lastname.data if names_form.lastname.data != current_user.get_lastname().value else None
        if new_firstname is None and new_lastname is None:
            flash(message="Names has not changed!", category="message")
            return redirect(url_for("settings.settings"))
        
        result = edit_name_util(user_obj=current_user, firstname=new_firstname, lastname=new_lastname)
        if not result:
            util_abort(
                code=500,
                client_msg="Server Error. Try again later",
                log_msg=f"edit_name_util() returned invalid value: {result} for firstname: {new_firstname} and lastname: {new_lastname}"
            )
        
        flash(message="Names Saved!", category="message")
        return redirect(url_for("settings.settings"))
            
    return render_template("settings/names.html", form=names_form)
