from flask import Blueprint

from .create import create
from .read import read
from .reads import reads
from .update import update

outgoing_bp = Blueprint(
    name="outgoing",
    import_name=__name__,
    url_prefix="/outgoings",
    template_folder="templates"
)



outgoing_bp.add_url_rule(
    rule="",
    endpoint="reads",
    view_func=reads,
    methods=["GET"]
)

outgoing_bp.add_url_rule(
    rule="/create",
    endpoint="create",
    view_func=create,
    methods=["GET"]
)

outgoing_bp.add_url_rule(
    rule="/<pid>",
    endpoint="read",
    view_func=read,
    methods=["GET"]
)

outgoing_bp.add_url_rule(
    rule="/<pid>/update",
    endpoint="update",
    view_func=update,
    methods=["GET"]
)