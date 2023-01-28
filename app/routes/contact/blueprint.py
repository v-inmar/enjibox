from flask import Blueprint

from .message import message

contact_bp = Blueprint(
    name="contact",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/contact"
)

contact_bp.add_url_rule(
    rule="/message",
    endpoint="message",
    view_func=message,
    methods=["GET", "POST"]
)

