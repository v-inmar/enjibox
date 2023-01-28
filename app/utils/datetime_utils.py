import datetime
from flask import current_app

def string_to_date(value: str) -> datetime.date:
    '''
    Returns datetime.date value

    @param value: string date that is has the format (yyyy-mm-dd) i.e. 1990-12-25
    '''
    try:
        return datetime.date.fromisoformat(value)
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False


def string_to_time(value: str) -> datetime.time:
    '''
    Returns datetime.time value

    @param value: string time to be converted 
    '''
    try:
        return datetime.time.fromisoformat(value)
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False
