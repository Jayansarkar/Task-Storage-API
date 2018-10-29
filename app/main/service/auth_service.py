from app.main.model.user import User
from app.main.util.dto import AuthDto
from app.main.config import key

import jwt
from datetime import datetime, timedelta

api = AuthDto.api
login = AuthDto.login
register = AuthDto.register


def login_user(payload):
    username, password = payload['username'], payload['password']
    user = User(username)
    if user.check_password(password):
        token = jwt.encode(
            payload={
                'public_id': user.pub_id,
                'exp': datetime.utcnow() + timedelta(hours=6)
            },key = key
        )
        return {
                    'message': 'login successful',
                    'data': {
                        'user': user.to_json(),
                        'token': token.decode('UTF-8')
                    }
                }, 200
    return {'message': "Invalid username or password"}, 404

def register_user(payload):
    username, password = payload['username'], payload['password']
    user = User(username)
    user.name = payload['name']
    if user.create_user(password):
        return {'message': 'User created successfully'}, 201
    return "User exits!", 402
