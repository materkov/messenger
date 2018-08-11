from flask import request
import core
from . import helpers
from flask import g
from functools import wraps


def check_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('Authorization', '')
        auth_token = auth_token[len('Bearer '):]

        user_id = core.check_auth_token(auth_token)
        if not user_id:
            return helpers.json_response({'error': 'auth error'})

        g.auth_user_id = user_id

        return func(*args, **kwargs)
    return wrapper
