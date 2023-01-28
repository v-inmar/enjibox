from flask import render_template, abort, url_for
from flask_login import current_user

from app.utils.decorator_utils import auth_required
from app.models.outgoing_model import OutgoingModel
from app.models.string_models import OutgoingLabelModel, OutgoingCommentModel, OutgoingCategoryModel, OutgoingFormModel
from app.models.numeric_models import OutgoingAmountModel


@auth_required
def create():
    categories = []
    forms = []
    currency = current_user.get_currency().value

    outgoing_objs = OutgoingModel.get_all_by_user_id(user_id=current_user.id)
    if outgoing_objs:
        for obj in outgoing_objs:
            category = obj.get_category().value
            if category:
                if category not in categories:
                    categories.append(category)
            
            form = obj.get_form().value
            if form:
                if form not in forms:
                    forms.append(form)

    constants = {
        "currency": currency,
        "categories": categories,
        "categories_default":"",
        "forms": forms,
        "form_default":"",
        "url": url_for("outgoing_api.create_api"),
        "label_max":OutgoingLabelModel.value_max_length,
        "comment_max":OutgoingCommentModel.value_max_length,
        "amount_min":f"{OutgoingAmountModel.amount_min_value:,.2f}",
        "amount_max":f"{OutgoingAmountModel.amount_max_value:,.2f}",
        "category_max":OutgoingCategoryModel.value_max_length,
        "form_max":OutgoingFormModel.value_max_length
    }
    return render_template(
        "outgoing/create.html",
        constants=constants
    )