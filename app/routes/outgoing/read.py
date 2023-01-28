from flask import render_template, url_for

from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.route_utils.abort_utils import util_abort
from app.models.outgoing_model import OutgoingModel
from app.models.string_models import OutgoingPIDModel

@auth_required
def read(pid):
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
    currency = current_user.get_currency().value
    item = {
        "currency":currency,
        "label": outgoing_obj.get_label().value if outgoing_obj.get_label() else None,
        "category": outgoing_obj.get_category().value if outgoing_obj.get_category() else None,
        "form": outgoing_obj.get_form().value if outgoing_obj.get_form() else None,
        "amount": f"{outgoing_obj.get_amount().value:,.2f}" if outgoing_obj.get_amount() else None,
        "date": outgoing_obj.date.strftime("%a, %d %b %Y"),
        "time": outgoing_obj.time.strftime("%H:%M") if outgoing_obj.time else None,
        "comment": outgoing_obj.get_comment().value if outgoing_obj.comment_id and outgoing_obj.get_comment() else None,
        "offset": outgoing_obj.offset,
        "edit_url": url_for("outgoing.update", pid=outgoing_obj.get_pid().value) if outgoing_obj.get_pid() else "",
        "delete_url": url_for("outgoing_api.delete_api", pid=outgoing_obj.get_pid().value) if outgoing_obj.get_pid() else "",
        "date_created": outgoing_obj.date_created,
        "date_edited": outgoing_obj.last_edited
    }
    
    return render_template("outgoing/read.html", item=item)