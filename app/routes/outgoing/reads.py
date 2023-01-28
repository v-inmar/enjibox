import datetime
import calendar
from decimal import Decimal
from flask import render_template, request, redirect, url_for, json
from flask_login import current_user

from app.utils.decorator_utils import auth_required
from app.utils.number_utils import string_to_int
from app.utils.datetime_utils import string_to_date
from app.models.outgoing_model import OutgoingModel
from app.models.string_models import OutgoingLabelModel, OutgoingCategoryModel, OutgoingFormModel

@auth_required
def reads():
    # Get query param keys
    param_keys = [str(key).lower() for key in request.args.keys()]

    to_redirect = False

    page=1
    if "page" in param_keys:
        p = string_to_int(value=request.args["page"])
        if p:
            page=p
    else:
        to_redirect=True

    label = ""
    if "label" in param_keys:
        label=request.args["label"]
    else:
        to_redirect = True
    
    date_from = datetime.date.today()
    if "date_from" in param_keys:
        df = string_to_date(request.args["date_from"])
        if df:
            date_from = df
    else:
        to_redirect = True
    
    date_to = datetime.date.today()
    if "date_to" in param_keys:
        dt = string_to_date(request.args["date_to"])
        if dt:
            date_to = dt
    else:
        to_redirect = True
    
    category = ""
    if "category" in param_keys:
        category = request.args["category"]
    else:
        to_redirect = True
    
    form = ""
    if "form" in param_keys:
        form = request.args["form"]
    else:
        to_redirect = True

    if to_redirect:
        return redirect(url_for("outgoing.reads", label=label, date_from=date_from, date_to=date_to, category=category, form=form, page=page))
    

    # Initialize list for the select element options in frontend
    categories = []
    forms = []

    # TODO: Find a better way
    # Get all the categories and forms the user had used, that are not deleted
    out_objs = OutgoingModel.get_all_by_user_id(user_id=current_user.id)
    if out_objs:
        for obj in out_objs:
            obj_category = obj.get_category().value if obj.get_category() else ""
            obj_form = obj.get_form().value if obj.get_form() else ""

            if obj_category not in categories:
                categories.append(obj_category)
            
            if obj_form not in forms:
                forms.append(obj_form)
    

    # Make sure that the passed in values are valid and exist
    category_default = category if category in categories else None
    form_default = form if form in forms else None
    
    category_id = None
    if category_default:
        category_obj = OutgoingCategoryModel.get_by_value(value=category_default)
        if category_obj:
            category_id = category_obj.id

    form_id = None
    if form_default:
        form_obj = OutgoingFormModel.get_by_value(value=form_default)
        if form_obj:
            form_id = form_obj.id
    
    # Get all the labels that resembles the label parameter
    label_ids = None
    if label:
        label_objs = OutgoingLabelModel.get_all_like_value(value=label) # case insensitive
        if label_objs:
            for label_obj in label_objs:
                if label_ids is None:
                    label_ids = []
                
                if label_obj.id not in label_ids:
                    label_ids.append(label_obj.id)

    # Get all the filtered objects without pagination
    # This allows to get the total value
    all_filtered_objs = OutgoingModel.get_all_with_filter(
        user_id=current_user.id,
        label_ids=label_ids,
        date_from=date_from,
        date_to=date_to,
        category_id=category_id,
        form_id=form_id
    )

    total = {
        "amount": Decimal("0.00"),
        "with_offset": False
    }
    if all_filtered_objs:
        for obj in all_filtered_objs:
            if obj.offset:
                total["with_offset"] = True
            total["amount"] += obj.get_amount().value if obj.get_amount() and not obj.offset else Decimal("0.00")

    # Get all the filtered objects with pagination
    paginated_objs = OutgoingModel.get_paginated_with_filter(
        user_id=current_user.id,
        label_ids=label_ids,
        date_from=date_from,
        date_to=date_to,
        category_id=category_id,
        form_id=form_id,
        page=page,
        per_page=15
    )

    num_of_pages = 0
    num_of_items = 0
    if paginated_objs:
        num_of_pages = paginated_objs.pages
        num_of_items = paginated_objs.total
        for obj in paginated_objs:
            print(f"user id: {current_user.id} outgoing id: {obj.id}")

    return render_template(
        "outgoing/reads.html",
        categories=categories,
        category_default = category_default,
        forms=forms,
        form_default=form_default,
        date_from=date_from,
        date_to=date_to,
        label=label,
        page=page,
        num_of_pages=num_of_pages,
        num_of_items=num_of_items,
        paginated_objs=paginated_objs,
        total=total
    )