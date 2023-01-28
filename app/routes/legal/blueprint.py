from flask import Blueprint

from .privacy import privacy
from .terms import terms

legal_bp = Blueprint(
    name="legal",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/legal"
)

legal_bp.add_url_rule(
    rule="/privacy",
    endpoint="privacy",
    view_func=privacy,
    methods=["GET"]
)

legal_bp.add_url_rule(
    rule="/terms",
    endpoint="terms",
    view_func=terms,
    methods=["GET"]
)