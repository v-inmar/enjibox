from flask import request, jsonify, make_response, current_app, url_for

from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.number_utils import string_to_decimal
from app.utils.datetime_utils import string_to_date, string_to_time

from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.api_utils.outgoing_api_utils import create_api_util

from app.models.outgoing_model import OutgoingModel
from app.models.string_models import OutgoingLabelModel, OutgoingCategoryModel, OutgoingFormModel, OutgoingCommentModel
from app.models.numeric_models import OutgoingAmountModel

@auth_required
def create_api():
    for key in current_app.config["OUTGOING_JSON_KEYS"]:
        if key not in request.json:
            util_abort(
                code=400,
                client_msg="Submitted data incomplete. Refresh the page and try again",
                log_msg=f"Request json does not contain the key '{key}'. Payload: {request.json}"
            )
    
    label_value = str(request.json["label"]).strip()[:OutgoingLabelModel.value_max_length]
    if len(label_value) < 1:
        util_abort(
            code=400,
            client_msg="Please enter a value for the Label",
            log_msg=f"Request JSON label contains empty value. Value: {label_value}"
        )
    
    category_value = str(request.json["category"]).strip()[:OutgoingCategoryModel.value_max_length]
    if len(category_value) < 1:
        util_abort(
            code=400,
            client_msg="Please enter a value for the Category",
            log_msg=f"Request JSON category contains empty value. Value: {category_value}"
        )

    form_value = str(request.json["form"]).strip()[:OutgoingFormModel.value_max_length]
    if len(form_value) < 1:
        util_abort(
            code=400,
            client_msg="Please enter a value for the Form",
            log_msg=f"Request JSON form contains empty value. Value: {form_value}"
        )
    
    amount_value = str(request.json["amount"]).strip()
    if len(amount_value) < 1:
        util_abort(
            code=400,
            client_msg="Please enter a valid value for the Amount",
            log_msg=f"Request JSON amount contains empty value. Value: {amount_value}"
        )
    
    if "." not in amount_value:
        amount_value += ".00"
    
    # This make sure only 2 decimal places without rounding
    amount_value = amount_value.split(".")[0]+"."+amount_value.split(".")[1][:2]

    amount_value_decimal = string_to_decimal(value=amount_value)
    if not amount_value_decimal:
        util_abort(
            code=400,
            client_msg="Please enter a valid value for the amount",
            log_msg=f"string_to_decimal() returned False fro the amount value: {amount_value}"
        )
    
    # value_min must be turned to string then to Decimal to preserve decimal places
    if amount_value_decimal < OutgoingAmountModel.amount_min_value:
        util_abort(
            code=400,
            client_msg="Amount entered is too small",
            log_msg=f"amount is less than the minimum allowed value. Value: {amount_value_decimal}"
        )
    
    if amount_value_decimal > OutgoingAmountModel.amount_max_value:
        util_abort(
            code=400,
            client_msg="Amount entered is too large",
            log_msg=f"amount is greater than the maximum allowed value. Value: {amount_value_decimal}"
        )
    
    date_value = str(request.json["date"]).strip()
    if len(date_value) < 1:
        util_abort(
            code=400,
            client_msg="Please enter a valid value for date",
            log_msg=f"Request JSON date contains empty value. Value: {date_value}"
        )
    
    date = string_to_date(value=date_value)
    if not date:
        util_abort(
            code=400,
            client_msg="Please enter a valid date value",
            log_msg=f"string_to_date returned False for date value: {date_value}"
        )

    time = None
    time_value = str(request.json["time"]).strip()
    if time_value:
        time = string_to_time(value=time_value)
        if not time:
            util_abort(
                code=400,
                client_msg="Please enter a valid time value",
                log_msg=f"string_to_time returned False for time value: {time_value}"
            )
    
    comment_value = str(request.json["comment"]).strip()[:OutgoingCommentModel.value_max_length]
    if len(comment_value) < 1:
        comment_value = None

    offset = request.json["offset"]
    if type(offset) != bool:
        util_abort(
            code=400,
            client_msg="Invalid value of offset",
            log_msg=f"Request JSON offset type is not boolean. Type: {type(offset)}"
        )

    outgoing_obj = create_api_util(
        user_id=current_user.id,
        label=label_value,
        category=category_value,
        form=form_value,
        amount=amount_value_decimal,
        date=date,
        time=time,
        comment=comment_value,
        offset=offset
    )

    if type(outgoing_obj) is not OutgoingModel:
        util_abort(
            code=500,
            client_msg="Server Error. Try again later",
            log_msg=f"outgoing_obj is not of type OutgoingModel. Type: {type(outgoing_obj)}"
        )
    
    currency = current_user.get_currency().value
    payload = {
        "pid":outgoing_obj.get_pid().value if outgoing_obj.get_pid() else None,
        "label":outgoing_obj.get_label().value if outgoing_obj.get_label() else None,
        "url":url_for("outgoing.read", pid=outgoing_obj.get_pid().value) if outgoing_obj.get_pid() else "",
        "amount":f"{outgoing_obj.get_amount().value:,.2f}" if outgoing_obj.get_amount() else None, # local unaware comma seperated
        "currency": currency,
        "date": outgoing_obj.date.strftime("%d %b %Y"),
        "category": outgoing_obj.get_category().value if outgoing_obj.get_category() else None,
        "form": outgoing_obj.get_form().value if outgoing_obj.get_form() else None,
        "time": outgoing_obj.time.strftime("%H:%M") if outgoing_obj.time else None,
        "comment": True if outgoing_obj.get_comment() and outgoing_obj.comment_id else False,
        "offset": outgoing_obj.offset
    }
    
    return make_response(jsonify({"status": "Created", "code": 201, "payload": payload}), 201)