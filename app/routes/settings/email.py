from flask import render_template, flash, url_for, redirect, current_app, request
from flask_login import current_user

from app.utils.decorator_utils import auth_required
from app.utils.form_utils import add_field_error
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.utils.route_utils.settings_utils import edit_email_util
from app.forms.settings_forms import SettingsEmailForm
from app.models.string_models import UserEmailModel
from app.models.user_model import UserModel

@auth_required
def email():
    site_key = current_app.config["R_SITE_KEY"]
    recaptcha_error = None
    email_form = SettingsEmailForm()
    if email_form.validate_on_submit():
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
                
                if not pword_obj.checkpw(password=email_form.password.data):
                    email_form.password.errors = add_field_error(field=email_form.password, msg="Not recognised")
                else:
                    email = email_form.email.data.strip().lower()
                    if email == current_user.get_email().value:
                        flash(message="Email Address has not changed!", category="message")
                        return redirect(url_for("settings.settings"))
                    else:
                        email_available = True
                        email_obj = UserEmailModel.get_by_value(value=email)
                        if email_obj is False:
                            util_abort(
                                code=500,
                                client_msg="Server Error. Try again later",
                                log_msg=f"UserEmailModel.get_by_value() returned False for the email value: {email}"
                            )
                        
                        if email_obj:
                            user_obj = UserModel.get_user_by_email_id(email_id=email_obj.id)
                            if user_obj is False:
                                util_abort(
                                    code=500,
                                    client_msg="Server Error. Try again later",
                                    log_msg=f"UserModel.get_user_by_email_id() returned False for email id: {email_obj.id}"
                                )
                            
                            if user_obj:
                                email_form.email.errors = add_field_error(field=email_form.email, msg="Email Address not available")
                                email_available = False
                        
                        if email_available:
                            if not edit_email_util(user_obj=current_user, email=email):
                                util_abort(
                                    code=500,
                                    client_msg="Server Error. Try again later",
                                    log_msg=f"edit_email_util() return invalid for user with id: {current_user.id} and email: {email}"
                                )
                            else:
                                flash(message="Email Address Saved", category="message")
                                flash(message="Please check your email inbox or spam folder on how to verify your email", category="message")
                                flash(message="Please re-login", category="message")
                                return redirect(url_for("settings.settings"))
                
    return render_template("settings/email.html", form=email_form, site_key=site_key, recaptcha_error=recaptcha_error)
