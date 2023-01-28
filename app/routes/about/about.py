from flask import render_template, current_app

def about():
    app_name = current_app.config["APP_NAME"]
    return render_template("about/about.html", app_name=app_name)