from flask.ext.restful import Resource, marshal_with, abort
from flask.ext.restful import fields
from flask.ext.restful import reqparse

from soloask_api.common.db import session
from soloask_api.common.util import token_required, to_json, is_param_ok, gen_token
from soloask_api.models.user import User

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'icon': fields.String,
    'title': fields.String,
    'introduction': fields.String,
    'price': fields.Float,
    'income': fields.Float,
    'device_token': fields.String,
    'ask_num': fields.Integer,
    'answer_num': fields.Integer,
    'heard_num': fields.Integer,
    'earning': fields.Float,
    'third_party_uuid': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('third_id', type=str)
parser.add_argument('icon', type=str)
parser.add_argument('device_token', type=str)
parser.add_argument('id', type=int)
parser.add_argument('title', type=str)
parser.add_argument('introduction', type=str)
parser.add_argument('price', type=float)
parser.add_argument('earning', type=float)
parser.add_argument('income', type=float)
parser.add_argument('ask_num', type=int)
parser.add_argument('answer_num', type=int)
parser.add_argument('heard_num', type=int)


class UserLoginResource(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        third_party_uuid = args['third_id']
        icon = args['icon']
        device_token = args['device_token']
        if not is_param_ok(third_party_uuid, username, icon):
            abort(400)
        exist_user_data = session.query(User).filter(User.third_party_uuid == third_party_uuid).first()
        if exist_user_data:
            return exist_user_data
        new_user_data = User(third_party_uuid, username, icon, device_token)
        session.add(new_user_data)
        session.commit()
        if new_user_data:
            data = new_user_data.to_json()
            token = gen_token(new_user_data.id)
            data.update(token=token)
            return to_json(data, True)
        else:
            return to_json('login failed')
        return new_user_data


class UserResource(Resource):
    @token_required
    @marshal_with(user_fields, envelope='data')
    def post(self):
        args = parser.parse_args()
        print args['id']
        user = session.query(User).filter(User.id == args['id']).first()
        if not user:
            abort(404)
        return user


class UserListResource(Resource):
    @marshal_with(user_fields, envelope='data')
    def get(self):
        user_list = session.query(User).all()
        return user_list
