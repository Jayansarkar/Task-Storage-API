from flask_restplus import Resource

from app.main.service.auth_service import (login, login_user, register,
                                           register_user)
from app.main.util.dto import AuthDto

api = AuthDto.api


@api.route('/login')
@api.response(404, "Invalid username or password")
@api.response(200, 'success')
class Login(Resource):
    @api.doc("user login")
    @api.expect(login)
    def post(self):
        return login_user(api.payload)


@api.route('/register')
@api.response(403, "username or password should not be blank")
@api.response(201, 'success')
@api.doc(security='apikey')
class Register(Resource):
    @api.doc("New user registration")
    @api.expect(register)
    def post(self):
        return register_user(api.payload)
