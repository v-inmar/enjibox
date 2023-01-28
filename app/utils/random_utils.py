import uuid
from flask import current_app

def create_random_string(maxlength: int):
    '''
    Returns a random string with a max value length constraint.
    It uses uuid4 to create the random string

    @param maxlength - 64bit integer
    '''
    try:
        return str(uuid.uuid4().hex+uuid.uuid4().hex)[:maxlength]
    except Exception as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False


def hide_email_util(email: str) -> str:
    '''
    Returns a masked email address i.e. email@email.com to e***l@email.com

    @param email: str
    '''
    try:
        if "@" not in email:
            raise ValueError(f"email does not contain '@' symbol: {email}")
        
        if "." not in email:
            raise ValueError(f"email does not contain '.' symbol: {email}")
        

        split_email = email.split("@")
        if len(split_email) != 2:
            raise ValueError(f"split_email length is not equals to 2. Length: {len(split_email)}")
        
        if len(split_email[0].strip()) < 1:
            raise ValueError(f"split_email[0] stripped has invalid length. Length: {len(split_email[0].strip())}")
        
        name = split_email[0].strip()[0]
        if len(split_email[0].strip()) > 1:
            name += '*' * len(split_email[0].strip()[1:-1])
            name += split_email[0].strip()[-1]
        
        return name+"@"+split_email[1]
    except ValueError as e:
        current_app.logger.error(msg=e, exc_info=1)
        return False