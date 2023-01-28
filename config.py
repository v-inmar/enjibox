import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config(object):
    # -- Keys -- #
    SECRET_KEY = os.getenv("secret_key")
    SERIALIZER_KEY = os.getenv("serializer_key")
    VERIFY_SERIALIZER_SALT = os.getenv("verify_serializer_salt")
    FORGOT_PASSWORD_SERIALIZER_SALT = os.getenv("forgot_password_serializer_salt")
    R_SITE_KEY = os.getenv("recaptcha_site_key")
    R_SECRET_KEY = os.getenv("recaptcha_secret_key")

    # -- Mail Server -- #
    MAIL_SERVER = os.getenv("mail_server")
    MAIL_PORT = os.getenv("mail_port")
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.getenv("mail_username")
    MAIL_PASSWORD = os.getenv("mail_password")
    MAIL_SENDER = os.getenv("mail_sender")

    # -- DB -- #
    DBUSER = os.getenv("dbuser")
    DBPASS = os.getenv("dbpass")
    DBHOST = os.getenv("dbhost")
    DBDB = os.getenv("dbdb")
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




class DevConfig(Config):

    # -- KEYS -- #
    SECRET_KEY = os.getenv("secret_key")
    SERIALIZER_KEY = os.getenv("serializer_key")
    CONFIRM_SERIALIZER_SALT = os.getenv("confirm_serializer_salt")

    # -- DB -- #
    DBUSER = os.getenv("dbuser")
    DBPASS = os.getenv("dbpass")
    DBHOST = os.getenv("dbhost")
    DBDB = os.getenv("dbdb")
    DB_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DBUSER, DBPASS, DBHOST, DBDB)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    RATELIMIT_STORAGE_URI="redis://localhost:6379"
    RATELIMIT_DEFAULT="3 per 1 second, 60 per minute"

    # -- SESSION -- #
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True