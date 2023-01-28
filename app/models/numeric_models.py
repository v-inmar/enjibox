from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from decimal import Decimal
from app import db
from app.models.base_model import BaseModel

class NumericModelMixin:
    @classmethod
    def get_by_value(cls, value: Decimal):
        try:
            return cls.query.filter(cls.value == value).first() or None
        except SQLAlchemyError as e:
            current_app.logger.error(msg=e, exc_info=1)
            return False


class OutgoingAmountModel(BaseModel, NumericModelMixin):
    """
    ORM class for the amount value of the payment
    i.e. 12.99
    """
    # Minimun and Maximum value of the amount
    amount_max_value = Decimal("10000000.00")
    amount_min_value = Decimal("0.01")

    __tablename__ = "outgoing_amount_model"

    # Decimal
    value = db.Column(db.Numeric(10,2), nullable=False, unique=True)

    def __init__(self, value: Decimal) -> None:
        super().__init__()
        self.value=value