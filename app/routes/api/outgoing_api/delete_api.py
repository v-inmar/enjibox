from flask import jsonify, make_response, url_for, flash

from flask_login import current_user
from app.utils.decorator_utils import auth_required
from app.utils.route_utils.abort_utils import util_abort
from app.utils.route_utils.api_utils.outgoing_api_utils import delete_api_utils
from app.models.outgoing_model import OutgoingModel
from app.models.string_models import OutgoingPIDModel

@auth_required
def delete_api(pid):
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
            client_msg="Resource Not Found. Try refreshing the page",
            log_msg=f"OutgoingModel.get_by_pid_id() returned None for pid_id: {pid_obj.id}"
        )
    
    if current_user.id != outgoing_obj.user_id:
        util_abort(
            code=404,
            client_msg="Resource Not Found. Try refreshing the page",
            log_msg=f"Resource with pid: {pid} does not belong to the current user"
        )
    
    if not delete_api_utils(outgoing_obj=outgoing_obj):
        util_abort(
            code=500,
            client_msg="Server Error. Try again later",
            log_msg=f"delete_api_utils() returned False for outgoing object with id: {outgoing_obj.id}"
        )

    year = int(outgoing_obj.date.strftime("%Y"))
    month = outgoing_obj.date.strftime("%B")

    flash(message="Deleted!", category="message")
    
    payload = {
        "url": url_for("outgoing.reads", year=year, month=month, page=1)
    }
    return make_response(jsonify({"status": "OK", "code": 200, "payload": payload}), 200)
    
