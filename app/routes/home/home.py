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
        # year = int(datetime.date.today().strftime("%Y")) # default year
        
        # # Get query param keys
        # param_keys = [str(key).lower() for key in request.args.keys()]
        # if "year" not in param_keys:
        #     # redirect with proper query param
        #     return redirect(url_for("home.home", year=year))
        # else:
        #     year_int = string_to_int(request.args["year"])
        #     if year_int:
        #         year = year_int
        #     else:
        #         # redirect with proper query param
        #         return redirect(url_for("home.home", year=year))
        
        
        # all_out_objs = OutgoingModel.get_all_by_user_id(user_id=current_user.id)
        # if all_out_objs is False:
        #     util_abort(
        #         code=500,
        #         client_msg="Server Error. Try again later",
        #         log_msg=f"OutgoingModel.get_all_by_user_id() returned False for user id: {current_user.id}"
        #     )
        
        # # All the years in the record of the current user
        # years = [year]

        # # Total Amount for the selected year
        # year_total = Decimal("0.00")

        
        # # make dictionary from calendar names with starting total amount of 0 (zero)
        # month_values = dict()
        # for month_abbr in list(calendar.month_abbr)[1:13]:
        #     month_values[month_abbr] = {
        #         "total": Decimal("0.00")
        #     }

        # # print(month_values.keys())
        
        # if all_out_objs:
        #     print(all_out_objs)
        #     for obj in all_out_objs:
        #         obj_year = int(obj.date.strftime("%Y"))
        #         obj_short_month_name = obj.date.strftime("%b")
        #         if obj_year not in years:
        #             years.append(obj_year) # grab the year
                
        #         if obj_year == year:
        #             # only perform for the selected year
        #             year_total += obj.get_amount().value if obj.get_amount() else Decimal("0.00")
        #             month_values[obj_short_month_name]["total"] += obj.get_amount().value if obj.get_amount() else Decimal("0.00")
        
        return render_template(
            "home/home.html"
        )
    
    return render_template("home/home_unauth.html")