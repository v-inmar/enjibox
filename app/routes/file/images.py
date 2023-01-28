import os
from flask import send_from_directory, current_app

def logo():
    try:
        INTERNAL_BASE_DIR = os.path.join(os.path.abspath(current_app.root_path), "directory", "internal", "")
        return send_from_directory(INTERNAL_BASE_DIR, current_app.config["LOGO"])
    except (OSError, Exception) as e:
        current_app.logger.error(msg=e, exc_info=1)
        return ""


def favicon():
    try:
        INTERNAL_BASE_DIR = os.path.join(os.path.abspath(current_app.root_path), "directory", "internal", "")
        return send_from_directory(INTERNAL_BASE_DIR, current_app.config["FAVICON"])
    except (OSError, Exception) as e:
        current_app.logger.error(msg=e, exc_info=1)
        return ""


def illustration(file):
    try:
        ILLUSTRATIONS_BASE_DIR = os.path.join(os.path.abspath(current_app.root_path), "directory", "internal", "illustrations")
        return send_from_directory(ILLUSTRATIONS_BASE_DIR, file)
    except (OSError, Exception) as e:
        current_app.logger.error(msg=e, exc_info=1)
        return ""