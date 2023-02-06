from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_user
from app.forms.auth_forms import SignUpForm
from app.models.user_model import UserModel
from app.models.string_models import UserEmailModel

from app.utils.form_utils import add_field_error
from app.utils.route_utils.auth_utils import signup_util
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.utils.decorator_utils import not_auth_required

@not_auth_required
def signup():
    site_key = current_app.config["R_SITE_KEY"]
    recaptcha_error = None
    form = SignUpForm()
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
                email_available = True
                email = form.email.data.strip().lower()

                email_obj = UserEmailModel.get_by_value(value=email)
                if email_obj is False:
                    util_abort(
                        code=500,
                        client_msg="Server Error. Try again later",
                        log_msg=f"UserEmailModel.get_by_value() returned False for email value: {email}"
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
                        form.email.errors = add_field_error(form.email, "Email address is not available")
                        email_available = False

                if email_available:
                    user_obj = signup_util(
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        email=email,
                        password=form.password.data,
                        currency=form.currency.data
                    )

                    if type(user_obj) is not UserModel:
                        util_abort(
                            code=500,
                            client_msg="Server Error. Try again later",
                            log_msg=f"user_obj is not of type UserModel. Type: {type(user_obj)}"
                        )
                    

                    flash(message=f"Welcome to {current_app.config['APP_NAME']}", category="message")
                    flash(message="Please check your email inbox or spam folder on how to verify your email", category="message")
                    login_user(user=user_obj, remember=True)
                    return redirect(url_for("home.home"))

    return render_template("auth/signup.html", form=form, site_key=site_key, recaptcha_error=recaptcha_error)