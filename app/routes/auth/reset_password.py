from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature, BadSignature
from flask import render_template, current_app, request, redirect, url_for, flash
from flask_login import current_user

from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.utils.route_utils.auth_utils import reset_password_util
from app.forms.auth_forms import ResetPasswordForm

from app.models.string_models import UserEmailModel
from app.models.user_model import UserModel

def reset_password(token):
    if current_user.is_authenticated:
        flash(message="Please change your password via the Settings", category="error")
        flash(message="If you cannot remember your password. Please logout and click 'Forgot Password' during the login", category="error")
        return redirect(url_for("settings.password"))
    
    try:
        one_hour = 3600
        email = URLSafeTimedSerializer(secret_key=current_app.config["SERIALIZER_KEY"]).loads(s=token, max_age=one_hour, salt=current_app.config["FORGOT_PASSWORD_SERIALIZER_SALT"])

        email_obj = UserEmailModel.get_by_value(value=email)
        if email_obj is False:
            util_abort(
                code=500,
                client_msg="Server Error. Try again later",
                log_msg=f"UserEmailModel.get_by_value() returned False for email: {email}"
            )
        
        if email_obj is None:
            util_abort(
                code=404,
                client_msg="Resource Not Found",
                log_msg=f"UserEmailModel.get_by_value() returned None for email: {email}"
            )
        
        user_obj = UserModel.get_user_by_email_id(email_id=email_obj.id)
        if user_obj is False:
            util_abort(
                code=500,
                client_msg="Server Error. Try again later",
                log_msg=f"UserModel.get_user_by_email_id() returned False for email id: {email_obj.id}"
            )
        
        if user_obj is None:
            util_abort(
                code=404,
                client_msg="Resource Not Found",
                log_msg=f"UserModel.get_user_by_email_id() returned None for email id: {email_obj.id}"
            )
        


        site_key = current_app.config["R_SITE_KEY"]
        recaptcha_error = None
        form = ResetPasswordForm()
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
                    if not reset_password_util(user_obj=user_obj, password=form.new_password.data):
                        util_abort(
                            code=500,
                            client_msg="Server Error. Try again later",
                            log_msg=f"reset_password_util() returned False with user id: {user_obj.id}"
                        )
                    
                    flash(message="Password Reset successful!", category="message")
                    flash(message="Please login with your new password", category="message")
                    return redirect(url_for("auth.login"))

        return render_template("auth/reset_password.html", form=form, site_key=site_key, recaptcha_error=recaptcha_error)
    except SignatureExpired as e:
        current_app.logger.error(msg=e, exc_info=1)
        flash(message="The link had expired. Please request a new link to reset your password", category="error")
        return redirect(url_for("auth.forgot_password"))
    except (BadTimeSignature, BadSignature) as e:
        current_app.logger.error(msg=e, exc_info=1)
        util_abort(
            code=404,
            client_msg="Resource Not Found",
            log_msg=f"URLSafeTimedSerializer does not recognized the token: {token}"
        )
    
    
    
