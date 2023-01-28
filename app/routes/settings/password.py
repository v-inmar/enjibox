from flask import render_template, flash, url_for, redirect, current_app, request
from flask_login import current_user

from app.utils.decorator_utils import auth_required
from app.utils.form_utils import add_field_error
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.utils.route_utils.settings_utils import edit_password_util

from app.forms.settings_forms import SettingsPasswordForm


@auth_required
def password():
    site_key = current_app.config["R_SITE_KEY"]
    recaptcha_error = None
    password_form = SettingsPasswordForm()
    if password_form.validate_on_submit():
        recaptcha = request.form["g-recaptcha-response"]
        if len(recaptcha) < 1:
            recaptcha_error = "ReCaptcha is needed"
        else:
            resp_json = check_recaptcha_util(response=recaptcha, remote_addr=request.remote_addr)
            if resp_json is False:
                util_abort(
                    code=500,
                    client_msg="Server Error. Please try again later",
                    log_msg=f"check_recaptcha_util() returned False for recaptcha: {recaptcha} with remote_addr: {request.remote_addr}"
                )
            if "success" not in resp_json:
                util_abort(
                    code=500,
                    client_msg="Server Error. Try again later",
                    log_msg=f"resp_json does not contain the json key 'success'. JSON: {resp_json}"
                )
            
            if not resp_json["success"]:
                recaptcha_error = "Failed. Please refresh the page and try again"
            
            else:
                pword_obj = current_user.get_password()
                if not pword_obj:
                    util_abort(
                        code=500,
                        client_msg="Server Error. Try again later",
                        log_msg=f"current_user.get_password() returned invalid value: {pword_obj}"
                    )
                
                if not pword_obj.checkpw(password=password_form.current_password.data):
                    password_form.current_password.errors = add_field_error(field=password_form.current_password, msg="Password not recognized")
                else:
                    if not edit_password_util(user_obj=current_user, password=password_form.new_password.data):
                        util_abort(
                            code=500,
                            client_msg="Server Error. Try again later",
                            log_msg=f"edit_password_util() returned False for user with id: {current_user.id} and password value: {password_form.new_password.data}"
                        )
                    
                    flash(message="Password Saved", category="message")
                    flash(message="Please re-login", category="message")
                    return redirect(url_for("settings.settings"))

    return render_template("settings/password.html", form=password_form, site_key=site_key, recaptcha_error=recaptcha_error)
