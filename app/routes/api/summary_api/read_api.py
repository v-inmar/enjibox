import datetime
from flask import request, jsonify, make_response, current_app, url_for
from flask_login import current_user
from decimal import Decimal

from app.utils.decorator_utils import auth_required
from app.utils.datetime_utils import string_to_date

from app.models.outgoing_model import OutgoingModel



@auth_required
def read_api():
    currency = current_user.get_currency().value if current_user.get_currency() else ""

    # initialize defaults
    server_date = datetime.date.today()
    server_year = server_date.strftime("%Y")
    server_month = server_date.strftime("%m")
    server_day = server_date.strftime("%d")

    year = None
    month = None
    day = None
    param_keys = [str(key).lower() for key in request.args.keys()]
    if "year" in param_keys:
        year = request.args["year"]
    
    if "month" in param_keys:
        month = request.args["month"]
    
    if "day" in param_keys:
        day = request.args["day"]
    
    date = string_to_date(value=f"{year}-{month}-{day}")
    if not date:
        year = server_year
        month = server_month
        day = server_day
        date = string_to_date(value=f"{year}-{month}-{day}")
    

    today = {
        "total": Decimal("0.00"),
        "items": 0,
        "category":{
            "highest_total": dict(),
            "most_used": dict()
        },
        "form":{
            "highest_total": dict(),
            "most_used": dict()
        }
    }

    this_week = {
        "total": Decimal("0.00"),
        "items": 0,
        "category":{
            "highest_total": dict(),
            "most_used": dict()
        },
        "form":{
            "highest_total": dict(),
            "most_used": dict()
        }
    }

    this_month = {
        "total": Decimal("0.00"),
        "items": 0,
        "category":{
            "highest_total": dict(),
            "most_used": dict()
        },
        "form":{
            "highest_total": dict(),
            "most_used": dict()
        }
    }

    this_year = {
        "total": Decimal("0.00"),
        "items": 0,
        "category":{
            "highest_total": dict(),
            "most_used": dict()
        },
        "form":{
            "highest_total": dict(),
            "most_used": dict()
        }
    }

    out_objs = OutgoingModel.get_all_by_user_id_with_year(user_id=current_user.id, year=int(year))
    if out_objs:
  
        for obj in out_objs:
            obj_amount = obj.get_amount().value if obj.get_amount() else Decimal("0.00")
            obj_category = obj.get_category().value if obj.get_category() else None
            obj_form = obj.get_form().value if obj.get_form() else None

            helper_util(obj.date == date, today, obj_amount, obj.offset, obj_category, obj_form)
            # Start of the week is Sunday - 0, Monday - 1, etc
            helper_util(obj.date.strftime("%U") == date.strftime("%U"), this_week, obj_amount, obj.offset, obj_category, obj_form)
            helper_util(obj.date.strftime("%m") == date.strftime("%m"), this_month, obj_amount, obj.offset, obj_category, obj_form)
            helper_util(obj.date.strftime("Y") == date.strftime("Y"), this_year, obj_amount, obj.offset, obj_category, obj_form)

    
    # Change the highest total and most used into sorted list
    # It is turned to list to maintain sorted structure
    helper_make_the_sort_util(today)
    helper_make_the_sort_util(this_week)
    helper_make_the_sort_util(this_month)
    helper_make_the_sort_util(this_year)

    # Format number values
    today["total"] = f"{today['total']:,.2f}"
    this_week["total"] = f"{this_week['total']:,.2f}"
    this_month["total"] = f"{this_month['total']:,.2f}"
    this_year["total"] = f"{this_year['total']:,.2f}"




    # category_highest_total["total"] = f"{category_highest_total['total']:,.2f}"
    # form_highest_total["total"] = f"{form_highest_total['total']:,.2f}"

    payload = {
        "currency": currency,
        "amount": {
            "today": today,
            "this_week": this_week,
            "this_month": this_month,
            "this_year": this_year
        }
    }
    return make_response(jsonify({"status": "OK", "code": 200, "payload": payload}), 200)


def helper_make_the_sort_util(parent_dictionary):
    c_dict = parent_dictionary["category"]
    f_dict = parent_dictionary["form"]
    c_dict["highest_total"] = helper_to_sorted_list_util(c_dict["highest_total"], is_int=False)
    f_dict["highest_total"] = helper_to_sorted_list_util(f_dict["highest_total"], is_int=False)
    c_dict["most_used"] = helper_to_sorted_list_util(c_dict["most_used"])
    f_dict["most_used"] = helper_to_sorted_list_util(f_dict["most_used"])



def helper_to_sorted_list_util(dictionary, is_int=True):
    tuple_list = list(dictionary.items())
    if tuple_list:
        tuple_list.sort(key=lambda y: y[1], reverse=True)

        only_three = tuple_list[:3] # only top 3
        if not is_int:
            for idx, v in enumerate(only_three):
                only_three[idx] = [v[0], f"{v[1]:,.2f}"]
        return  only_three
    return []


def helper_util(comparator, dictionary, amount, offset, category, form):
    if comparator:
        dictionary["total"] += amount if not offset else Decimal("0.00")
        dictionary["items"] += 1

        if category:
            c_dict = dictionary["category"]

            cht_dict = c_dict["highest_total"]
            cht_keys = cht_dict.keys()
            if category not in cht_keys:
                cht_dict[category] = amount
            else:
                cht_dict[category] += amount

            cmu_dict = c_dict["most_used"]
            cmu_keys = cmu_dict.keys()
            if category not in cmu_keys:
                cmu_dict[category] = 1
            else:
                cmu_dict[category] += 1
        
        if form:
            f_dict = dictionary["form"]

            fht_dict = f_dict["highest_total"]
            fht_keys = fht_dict.keys()
            if form not in fht_keys:
                fht_dict[form] = amount
            else:
                fht_dict[form] += amount

            fmu_dict = f_dict["most_used"]
            fmu_keys = fmu_dict.keys()
            if form not in fmu_keys:
                fmu_dict[form] = 1
            else:
                fmu_dict[form] += 1