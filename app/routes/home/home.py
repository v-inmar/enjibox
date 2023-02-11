from flask import render_template, current_app
from flask_login import current_user

def home():
    if current_user.is_authenticated:       
        return render_template(
            "home/home.html"
        )
    
    return render_template("home/home_unauth.html", app_name=current_app.config["APP_NAME"])