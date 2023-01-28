from flask import Flask

from app.routes.auth.blueprint import auth_bp
from app.routes.home.blueprint import home_bp
from app.routes.outgoing.blueprint import outgoing_bp
from app.routes.settings.blueprint import settings_bp
from app.routes.file.blueprint import file_bp
from app.routes.contact.blueprint import contact_bp
from app.routes.about.blueprint import about_bp
from app.routes.legal.blueprint import legal_bp

def load_blueprints(app: Flask) -> None:
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(outgoing_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(legal_bp)



from app.routes.api.outgoing_api.blueprint_api import outgoing_api_bp
from app.routes.api.summary_api.blueprint_api import summary_api_bp

def load_api_blueprints(app: Flask) -> None:
    app.register_blueprint(outgoing_api_bp)
    app.register_blueprint(summary_api_bp)
