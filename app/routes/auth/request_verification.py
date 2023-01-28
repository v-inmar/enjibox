from flask import render_template, current_app, request, redirect, url_for, flash
from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.utils.route_utils.auth_utils import request_verification_util
from app.utils.form_utils import add_field_error
from app.forms.auth_forms import RequestVerificationForm

@auth_required
def request_verification():
    if current_user.verified:
        return redirect(url_for("home.home"))
    
    site_key = current_app.config["R_SITE_KEY"]
    recaptcha_error = None
    form = RequestVerificationForm()
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

                current_email = current_user.get_email().value if current_user.get_email() else util_abort(code=500, client_msg="Server Error. Try again later", log_msg="Unable to get current_user's email")

                if current_email != email:
                    form.email.errors = add_field_error(field=form.email, msg="Email is not recognized")
                else:
                    if not request_verification_util(email=current_email):
                        util_abort(
                            code=500,
                            client_msg="Server Error. Try again later",
                            log_msg=f"request_verification_util() returned False for email: {current_email}"
                        )
                    
                    flash(message="Please check your email inbox or spam folder for the new verification instruction", category="message")
                    return redirect(url_for("home.home"))
    return render_template("auth/request_verification.html", form=form, site_key=site_key, recaptcha_error=recaptcha_error)
