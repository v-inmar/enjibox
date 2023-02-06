import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config(object):
    # -- Keys -- #
    SECRET_KEY = os.environ.get("secret_key")
    SERIALIZER_KEY = os.environ.get("serializer_key")
    VERIFY_SERIALIZER_SALT = os.environ.get("verify_serializer_salt")
    FORGOT_PASSWORD_SERIALIZER_SALT = os.environ.get("forgot_password_serializer_salt")
    R_SITE_KEY = os.environ.get("recaptcha_site_key")
    R_SECRET_KEY = os.environ.get("recaptcha_secret_key")

    # -- Mail Server -- #
    MAIL_SERVER = os.environ.get("mail_server")
    MAIL_PORT = os.environ.get("mail_port")
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.environ.get("mail_username")
    MAIL_PASSWORD = os.environ.get("mail_password")
    MAIL_SENDER = os.environ.get("mail_sender")

    # -- DB -- #
    DBUSER = os.environ.get("dbuser")
    DBPASS = os.environ.get("dbpass")
    DBHOST = os.environ.get("dbhost")
    DBDB = os.environ.get("dbdb")
    DB_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DBUSER, DBPASS, DBHOST, DBDB)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # -- Rate Limit -- #
    RATELIMIT_STORAGE_URI="redis://localhost:6379"
    RATELIMIT_DEFAULT="3 per 1 second, 60 per minute"

    # -- Session -- #
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    # -- Celery Config -- #
    CELERY_BROKER_URL = "redis://localhost:6379"
    result_backend = "redis://localhost:6379"
    # -- Images -- #
    LOGO = "elogo.svg"
    FAVICON = "favicon.ico"

    # -- Constants -- #
    OUTGOING_JSON_KEYS = ["label", "amount", "date", "time", "category", "form", "comment", "offset"]
    APP_NAME = "Enjibox"