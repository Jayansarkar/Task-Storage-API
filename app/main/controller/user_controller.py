from flask import request
from flask_restplus import Resource

from app.main.service.user_service import (del_user, get_all_users,
                                           get_one_user, make_admin, user)
from app.main.util.decorator import admin_token_required, token_required
from app.main.util.dto import UserDto

api = UserDto.api


@api.route('/')
@api.response(404, "No user found")
@api.doc(security='apikey')
class AllUsers(Resource):
    @api.marshal_list_with(user, envelope='data')
    @token_required
    def get(self):
        return get_all_users()


@api.route('/<public_id>')
@api.response(404, "user not found")
@api.param('public_id', 'The User identifier')
@api.doc(security='apikey')
class SingleUser(Resource):
    @api.marshal_with(user, envelope='data')
    @token_required
    def get(self, public_id):
        return get_one_user(public_id)

    
    @admin_token_required
    def put(self, public_id):
        return make_admin(public_id)

    
    @admin_token_required
    def delete(self, public_id):
        return del_user(public_id)
