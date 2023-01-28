import requests
from flask import current_app

def check_recaptcha_util(response, remote_addr):
    try:
        url = "https://www.google.com/recaptcha/api/siteverify"
        url += "?secret="+current_app.config["R_SECRET_KEY"]
        url += "&response="+response
        url += "&remoteip="+remote_addr

        resp = requests.post(url)
        return resp.json()
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False