from flask import Blueprint
from .login import login
from .signup import signup
from .logout import logout
from .verify_email import verify_email
from .request_verification import request_verification
from .forgot_password import forgot_password
from .reset_password import reset_password


auth_bp = Blueprint(
    name="auth",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/auth"
)

auth_bp.add_url_rule(
    rule="/logout",
    endpoint="logout",
    view_func=logout,
    methods=["GET"]
)

auth_bp.add_url_rule(
    rule="/login",
    endpoint="login",
    view_func=login,
    methods=["POST", "GET"]
)

auth_bp.add_url_rule(
    rule="/signup",
    endpoint="signup",
    view_func=signup,
    methods=["POST", "GET"]
)

auth_bp.add_url_rule(
    rule="/verify_email/<token>",
    endpoint="verify_email",
    view_func=verify_email,
    methods=["GET"]
)

auth_bp.add_url_rule(
    rule="/request_verification",
    endpoint="request_verification",
    view_func=request_verification,
    methods=["POST", "GET"]
)

auth_bp.add_url_rule(
    rule="/forgot_password",
    endpoint="forgot_password",
    view_func=forgot_password,
    methods=["POST", "GET"]
)

auth_bp.add_url_rule(
    rule="/reset_password/<token>",
    endpoint="reset_password",
    view_func=reset_password,
    methods=["POST", "GET"]
)