from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature, BadSignature
from flask import current_app, redirect, url_for, flash
from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.auth_utils import verify_email_util


@auth_required
def verify_email(token):
    if current_user.verified:
        return redirect(url_for("home.home"))
    
    try:
        one_day = 864000
        email = URLSafeTimedSerializer(secret_key=current_app.config["SERIALIZER_KEY"]).loads(s=token, max_age=one_day, salt=current_app.config["VERIFY_SERIALIZER_SALT"])
        current_email = current_user.get_email().value if current_user.get_email() else util_abort(code=500, client_msg="Server Error. Try again later", log_msg="Unable to get current_user's email")
        if current_email != email.lower().strip():
            raise BadTimeSignature(message=f"current user's email did not match the token email: {email}. Token: {token}")
        
        if not verify_email_util(user_obj=current_user):
            util_abort(
                code=500,
                client_msg="Server Error. Try again later",
                log_msg=f"verify_email_util() returned False for user id: {current_user.id}"
            )
        
        flash(message="Email Verified!", category="message")
        return redirect(url_for("home.home"))
    except SignatureExpired as e:
        current_app.logger.error(msg=e, exc_info=1)
        flash(message="The link had expired. Please request a new link to verify your email", category="error")
        return redirect(url_for("auth.request_verification"))
    except (BadTimeSignature, BadSignature) as e:
        current_app.logger.error(msg=e, exc_info=1)
        util_abort(
            code=404,
            client_msg="Resource Not Found",
            log_msg=f"URLSafeTimedSerializer does not recognized the token: {token}"
        )