from flask import abort

def util_abort(code: int, client_msg: str, log_msg: str) -> abort:
    '''
    Returns abort
    '''
    return abort(
        code=code,
        description=(
            client_msg,
            log_msg
        )
    )