from flask import render_template, redirect, url_for
from flask_login import login_user

from app.forms.auth_forms import LoginForm
from app.utils.form_utils import add_field_error
from app.utils.route_utils.abort_utils import util_abort
from app.utils.decorator_utils import not_auth_required
from app.models.user_model import UserModel
from app.models.string_models import UserEmailModel

@not_auth_required
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        email_obj = UserEmailModel.get_by_value(value=email)
        if email_obj is False:
            util_abort(
                code=500,
                client_msg="Server Error. Try again later",
                log_msg=f"UserEmailModel.get_by_value() returned False for email value: {email}"
            )
        
        if email_obj is None:
            form.email.errors = add_field_error(field=form.email, msg="Credentials invalid")
            form.password.errors = add_field_error(field=form.password, msg="Credentials invalid")
        else:
            user_obj = UserModel.get_user_by_email_id(email_id=email_obj.id)
            if user_obj is False:
                util_abort(
                    code=500,
                    client_msg="Server Error. Try again later",
                    log_msg=f"UserModel.get_user_by_email_id() returned False for email id: {email_obj.id}"
                )
            
            if user_obj is None:
                form.email.errors = add_field_error(field=form.email, msg="Credentials invalid")
                form.password.errors = add_field_error(field=form.password, msg="Credentials invalid")
            else:
                pword_obj = user_obj.get_password()
                if not pword_obj:
                    util_abort(
                        code=500,
                        client_msg="Server Error. Try again later",
                        log_msg=f"user_obj.get_password() returned invalid value: {pword_obj}"
                    )
                
                if not pword_obj.checkpw(password=form.password.data):
                    form.email.errors = add_field_error(field=form.email, msg="Credentials invalid")
                    form.password.errors = add_field_error(field=form.password, msg="Credentials invalid")
                else:
                    login_user(user=user_obj, remember=form.remember.data)
                    return redirect(url_for('home.home'))
    return render_template("auth/login.html", form=form)