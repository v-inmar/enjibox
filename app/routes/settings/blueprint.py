from flask import Blueprint
from .settings import settings
from .names import names
from .email import email
from .password import password
from .currency import currency

settings_bp = Blueprint(
    name="settings",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/settings"
)

settings_bp.add_url_rule(
    rule="",
    endpoint="settings",
    view_func=settings,
    methods=["GET"]
)


settings_bp.add_url_rule(
    rule="/names",
    endpoint="names",
    view_func=names,
    methods=["GET", "POST"]
)

settings_bp.add_url_rule(
    rule="/email",
    endpoint="email",
    view_func=email,
    methods=["GET", "POST"]
)

settings_bp.add_url_rule(
    rule="/password",
    endpoint="password",
    view_func=password,
    methods=["GET", "POST"]
)

settings_bp.add_url_rule(
    rule="/currency",
    endpoint="currency",
    view_func=currency,
    methods=["GET", "POST"]
)