from flask import Blueprint

from .create_api import create_api
from .delete_api import delete_api
from .update_api import update_api

outgoing_api_bp = Blueprint(
    name="outgoing_api",
    import_name=__name__,
    url_prefix="/api/v1/outgoings"
)

outgoing_api_bp.add_url_rule(
    rule="",
    endpoint="create_api",
    view_func=create_api,
    methods=["POST"]
)


outgoing_api_bp.add_url_rule(
    rule="/<pid>",
    endpoint="delete_api",
    view_func=delete_api,
    methods=["DELETE"]
)

outgoing_api_bp.add_url_rule(
    rule="/<pid>",
    endpoint="update_api",
    view_func=update_api,
    methods=["PUT"]
)
