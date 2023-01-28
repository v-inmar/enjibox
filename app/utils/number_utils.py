from decimal import Decimal
from flask import current_app


def string_to_decimal(value: str) -> Decimal:
    '''
    Returns Decimal value

    @param value: string value to be converted to Decimal i.e. 9.99
    '''
    try:
        return Decimal(value)
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False


def string_to_int(value: str) -> int:
    '''
    Returns int value from string

    @param value - string value to be converted to int
    '''
    try:
        return int(value)
    except ValueError as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False