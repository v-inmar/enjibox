from flask import render_template, url_for
from decimal import Decimal
from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.route_utils.abort_utils import util_abort
from app.models.outgoing_model import OutgoingModel
from app.models.string_models import OutgoingLabelModel, OutgoingCategoryModel, OutgoingFormModel, OutgoingCommentModel, OutgoingPIDModel
from app.models.numeric_models import OutgoingAmountModel

@auth_required
def update(pid):
    pid_obj = OutgoingPIDModel.get_by_value(value=pid)
    if pid_obj is False:
        util_abort(
            code=500,
            client_msg="Server Error. Try again later",
            log_msg=f"OutgoingPIDModel.get_by_value() returned False for value: {pid}"
        )
    
    if pid_obj is None:
        util_abort(
            code=404,
            client_msg="Resource Not Found. Try refreshing the page",
            log_msg=f"OutgoingPIDModel.get_by_value() returned None for pid: {pid}"
        )

    outgoing_obj = OutgoingModel.get_by_pid_id(pid_id=pid_obj.id)
    if outgoing_obj is False:
        util_abort(
            code=500,
            client_msg="Server Error. Try again later",
            log_msg=f"OutgoingModel.get_by_pid_id() returned False for pid_id: {pid_obj.id}"
        )
    
    if outgoing_obj is None:
        util_abort(
            code=404,
            client_msg="Resource Not Found",
            log_msg=f"OutgoingModel.get_by_pid_id() returned None for pid_id: {pid_obj.id}"
        )
    
    if outgoing_obj.user_id != current_user.id:
        util_abort(
            code=404,
            client_msg="Resource Not Found",
            log_msg=f"user does not own the resource with pid_id: {pid_obj.id}"
        )
    # yyyy-mm-dd
    item = {
        "label": outgoing_obj.get_label().value if outgoing_obj.get_label() else None,
        "category": outgoing_obj.get_category().value if outgoing_obj.get_category() else None,
        "form": outgoing_obj.get_form().value if outgoing_obj.get_form() else None,
        "amount": outgoing_obj.get_amount().value if outgoing_obj.get_amount() else Decimal("0.00"),
        "date": outgoing_obj.date.strftime("%Y-%m-%d"),
        "time": outgoing_obj.time.strftime("%H:%M") if outgoing_obj.time else None,
        "comment": outgoing_obj.get_comment().value if outgoing_obj.comment_id and outgoing_obj.get_comment() else None,
        "offset": outgoing_obj.offset,
        "url": url_for("outgoing.read", pid=outgoing_obj.get_pid().value) if outgoing_obj.get_pid() else ""
    }
    
    categories = []
    forms = []
    currency = current_user.get_currency().value

    outgoing_objs = OutgoingModel.get_all_by_user_id(user_id=current_user.id)
    if outgoing_objs:
        for obj in outgoing_objs:
            cat_value = obj.get_category().value
            if cat_value:
                if cat_value not in categories:
                    categories.append(cat_value)
            
            form_value = obj.get_form().value
            if form_value:
                if form_value not in forms:
                    forms.append(form_value)

    

    constants = {
        "currency": currency,
        "categories": categories,
        "categories_default":"",
        "forms": forms,
        "form_default":"",
        "url": url_for("outgoing_api.update_api", pid=outgoing_obj.get_pid().value),
        "label_max":OutgoingLabelModel.value_max_length,
        "comment_max":OutgoingCommentModel.value_max_length,
        "amount_min":f"{OutgoingAmountModel.amount_min_value:,.2f}",
        "amount_max":f"{OutgoingAmountModel.amount_max_value:,.2f}",
        "category_max":OutgoingCategoryModel.value_max_length,
        "form_max":OutgoingFormModel.value_max_length
    }
    return render_template("outgoing/update.html", constants=constants, item=item)