from app.main.model.user import User
from app.main.db import get_db
from app.main.util.dto import UserDto

api = UserDto.api
user = UserDto.user


def make_admin(public_id):
    user = User.from_pub_id(public_id)
    if user is None:
        api.abort(404)
    return user.make_admin()


def del_user(public_id):
    user = User.from_pub_id(public_id)
    if user is None:
        api.abort(404)
    return user.delete()

def get_all_users():
    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()

    if not users:
        api.abort(404)
    res = {
        'data': []
    }
    for user in users:
        user = User(user['username'])
        user.fetch_info()
        res['data'].append(user.to_json())
    
    return res


def get_one_user(pub):
    db = get_db()
    user = db.execute(
        'SELECT username FROM user WHERE pub_id = ?', (pub,)
    ).fetchone()
    if not user:
        api.abort(404)
    user = User(user['username'])
    user.fetch_info()
    return {'data':user.to_json()}
