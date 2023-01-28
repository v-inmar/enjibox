from flask import render_template, request, current_app, flash, url_for, redirect
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.recaptcha_utils import check_recaptcha_util
from app.forms.contact_froms import ContactForm
from app.utils.route_utils.contact_utils import message_util

def message():
    site_key = current_app.config["R_SITE_KEY"]
    recaptcha_error = None
    form = ContactForm()
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
                firstname = form.firstname.data.strip()
                lastname = form.lastname.data.strip()
                email = form.email.data.strip().lower()
                message = form.message.data.strip()

                if not message_util(firstname=firstname,lastname=lastname,email=email,message=message):
                    util_abort(
                        code=500,
                        client_msg="Server Error. Try again later.",
                        log_msg=f"message_util() return False"
                    )
                flash(message="Message Sent", category="message")
                return redirect(url_for("home.home"))
    return render_template("contact/message.html", form=form, recaptcha_error=recaptcha_error, site_key=site_key)
