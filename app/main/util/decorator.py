from flask import request

from functools import wraps
import jwt

from app.main.model.user import User
from app.main.config import key


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            return {'message': 'token is missing'}, 401
        token = request.headers['X-API-KEY']
        try:
            jwt.decode(token, key=key)
            print('hi')
        except:
            return {'message': 'token is invalid'}, 401

        return f(*args, **kwargs)

    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            return {'message': 'token is missing'}, 401
        token = request.headers['X-API-KEY']
        try:
            data = jwt.decode(token, key=key)
            cur_user = User.from_pub_id(data['public_id'])
            cur_user.fetch_info()
            if not cur_user.is_admin():
                return {'message': 'admin privilage required'}, 403
        except:
            return {'message': 'token is invalid'}, 401

        return f(*args, **kwargs)

    return decorated