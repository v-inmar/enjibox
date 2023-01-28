from flask import Blueprint

from .about import about

about_bp = Blueprint(
    name="about",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/about"
)

about_bp.add_url_rule(
    rule="",
    endpoint="about",
    view_func=about,
    methods=["GET"]
)
