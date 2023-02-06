from flask import render_template, redirect, url_for, current_app, request, flash
from flask_login import current_user


from app.utils.route_utils.auth_utils import forgot_password_util
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.forms.auth_forms import ForgotPasswordForm
from app.models.string_models import UserEmailModel
from app.models.user_model import UserModel
from app.utils.decorator_utils import not_auth_required

@not_auth_required
def forgot_password():
    if current_user.is_authenticated:
        flash(message="Please change your password via the Settings", category="error")
        flash(message="If you cannot remember your password. Please logout and click 'Forgot Password' during the login", category="error")
        return redirect(url_for("settings.password"))
    
    site_key = current_app.config["R_SITE_KEY"]
    recaptcha_error = None
    form = ForgotPasswordForm()
    if form.validate_on_submit():
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
                email = form.email.data.strip().lower()

                email_obj = UserEmailModel.get_by_value(value=email)
                if email_obj is False:
                    util_abort(
                        code=500,
                        client_msg="Server Error. Try again later",
                        log_msg=f"UserEmailModel.get_by_value() returned False for email: {email}"
                    )
                
                if email_obj:
                    user_obj = UserModel.get_user_by_email_id(email_id=email_obj.id)
                    if user_obj is False:
                        util_abort(
                            code=500,
                            client_msg="Server Error. Try again later",
                            log_msg=f"UserModel.get_user_by_email_id() return False for email id: {email_obj.id}"
                        )
                    
                    # Only send email if the actual user exists with the given email
                    if user_obj:
                        if not forgot_password_util(email=email):
                            util_abort(
                                code=500,
                                client_msg="Server Error. Try again later",
                                log_msg=f"forgot_password_util() returned False for email: {email}"
                            )
                
                # Regardless whether the user exists with the given email or not, give feedback to user
                # This will help minimize user guessing other people's email
                flash(message="Email Sent!", category="message")
                flash(message="Please check your email inbox or spam folder for instructions on how to reset your password", category="message")
                return redirect(url_for("home.home"))
    return render_template("auth/forgot_password.html", form=form, recaptcha_error=recaptcha_error, site_key=site_key)