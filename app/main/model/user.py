from app.main import flask_bcrypt
from app.main.db import get_db
from app.main.util.dto import UserDto

import uuid

api = UserDto.api

class User:

    def __init__(self, username):
        self.username = username
        self.name = None
        self.pw_hash = None
        self.pub_id = None
        self.id = None
        self.admin = None

    @classmethod
    def from_pub_id(cls, pub_id):
        db = get_db()
        user = db.execute(
            'SELECT username FROM user WHERE pub_id = ?', (pub_id,)
        ).fetchone()
        if not user:
            return None
        return cls(user['username'])

    def __check_username(self):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (self.username,)
        ).fetchone()

        if user is None:
            return False
        self.name = user['name']
        self.pw_hash = user['password']
        self.id = user['id']
        self.pub_id = user['pub_id']
        self.admin = True if user['admin'] else False

        return True

    def fetch_info(self):
        self.__check_username()

    def check_password(self, passwd):
        if not self.__check_username():
            return False
        return flask_bcrypt.check_password_hash(self.pw_hash, passwd)

    def create_user(self, passwd):
        db = get_db()
        if self.__check_username():
            return False
        self.pub_id = str(uuid.uuid4())
        self.pw_hash = flask_bcrypt.generate_password_hash(passwd)
        db.execute(
            'INSERT INTO user (username, name, password, pub_id) VALUES (?, ?, ?, ?)',
            (self.username, self.name, self.pw_hash, self.pub_id)
        )
        db.commit()

        return True

    def make_admin(self):
        if not self.__check_username():
            return 'user not found', 404
        db = get_db()
        self.admin = True
        db.execute(
            "UPDATE user SET admin = ? WHERE username = ?", (True, self.username)
        )
        db.commit()
        return {
            'message': "User successfully updated",
            'user': self.to_json()
        }

    def delete(self):
        if not self.fetch_info():
            api.abort(404)
        db = get_db()
        db.execute(
            'DELETE FROM user WHERE username = ?', (self.username,)
        )

    def is_admin(self):
        return self.admin

    def to_json(self):
        return {
            'name': self.name,
            'username': self.username,
            'public id': self.pub_id,
            'admin': self.admin,
            'password hash': str(self.pw_hash)
        }

