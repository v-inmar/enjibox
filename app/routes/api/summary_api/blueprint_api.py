from flask import Blueprint

from .read_api import read_api

summary_api_bp = Blueprint(
    name="summary_api",
    import_name=__name__,
    url_prefix="/api/v1/summary"
)

summary_api_bp.add_url_rule(
    rule="",
    endpoint="read_api",
    view_func=read_api,
    methods=["GET"]
)