import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
from config import Config

from app.utils.log_utils import CustomLogFormatter

db = SQLAlchemy(session_options={'autocommit': False})
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
limiter = Limiter(get_remote_address)
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_class):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    log_path = "./logs/app.log"

    formatter = CustomLogFormatter("[%(asctime)s] %(levelname)s: %(remote_addr)s %(method)s:%(url)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler = TimedRotatingFileHandler(
        filename=log_path,
        utc=True,
        when="midnight"
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    csrf.init_app(app=app)
    mail.init_app(app=app)
    login_manager.init_app(app=app)
    limiter.init_app(app=app)
    celery.conf.update(app.config)

    from app import user_loader

    from app import model_loader

    from app.blueprint_loader import load_blueprints, load_api_blueprints
    load_blueprints(app=app)
    load_api_blueprints(app=app)

    from app.error_loader import load_error
    load_error(app=app)


    return app