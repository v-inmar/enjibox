from flask import Blueprint
from .home import home

home_bp = Blueprint(
    name="home",
    import_name=__name__,
    template_folder="templates"
)

home_bp.add_url_rule(
    rule="/",
    endpoint="home",
    view_func=home,
    methods=["GET"]
)

home_bp.add_url_rule(
    rule="/home",
    endpoint="home",
    view_func=home,
    methods=["GET"]
)

home_bp.add_url_rule(
    rule="/index",
    endpoint="home",
    view_func=home,
    methods=["GET"]
)