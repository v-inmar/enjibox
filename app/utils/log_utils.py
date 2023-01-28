import logging
from flask import (
    has_request_context,
    request
)

class CustomLogFormatter(logging.Formatter):

    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.method = None
            record.remote_addr = None
        
        return super().format(record=record)