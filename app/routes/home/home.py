import datetime
import calendar
from decimal import Decimal
from flask import render_template, url_for, current_app, request, redirect, json
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer
from app.utils.number_utils import string_to_int
from app.utils.route_utils.abort_utils import util_abort

from app.models.outgoing_model import OutgoingModel

def home():
    if current_user.is_authenticated:       
        return render_template(
            "home/home.html"
        )
    
    return render_template("home/home_unauth.html")