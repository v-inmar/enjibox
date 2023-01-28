from flask import Blueprint

from .images import logo
from .images import favicon
from .images import illustration

file_bp = Blueprint(
    name="file",
    import_name=__name__,
    url_prefix="/files"
)

file_bp.add_url_rule(
    rule="/logo",
    endpoint="logo",
    view_func=logo,
    methods=["GET"]
)

file_bp.add_url_rule(
    rule="/favicon",
    endpoint="favicon",
    view_func=favicon,
    methods=["GET"]
)

file_bp.add_url_rule(
    rule="/illustrations/<file>",
    endpoint="illustration",
    view_func=illustration,
    methods=["GET"]
)