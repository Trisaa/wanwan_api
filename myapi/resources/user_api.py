from flask import Blueprint
from flask import abort
from flask.ext.restful import reqparse

from myapi.common.util import is_param_ok, gen_token, to_json, token_required
from myapi.resources.user import UserResource

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def index():
    return 'hello world'


@user_blueprint.route('/login', methods=['POST'])
def user_login():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('third_id', type=str)
    parser.add_argument('icon', type=str)
    parser.add_argument('device_token', type=str)
    args = parser.parse_args()
    username = args['username']
    third_party_uuid = args['third_id']
    icon = args['icon']
    device_token = args['device_token']

    if not is_param_ok(username, third_party_uuid, icon):
        abort(400)
    model = UserResource()
    new_user_data = model.login(third_party_uuid, username, icon, device_token)

    if new_user_data:
        data = new_user_data.toJson()
        token = gen_token(new_user_data.id)
        data.update(token=token)
        return to_json(data, True)
    else:
        return to_json('login failed')


@user_blueprint.route('/info', methods=['POST'])
@token_required
def get_userinfo(token, id):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    args = parser.parse_args()
    user_id = args['id']
    if not is_param_ok(user_id):
        abort(400)
    model = UserResource()
    data = model.get_user_info(user_id)
    if data:
        return to_json(data.toJson(), True)
    else:
        return to_json('User doesn\'t exist')


@user_blueprint.route('/update', methods=['POST'])
def update_userinfo():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('title', type=str)
    parser.add_argument('introduction', type=str)
    parser.add_argument('price', type=float)
    args = parser.parse_args()
    user_id = args['id']
    title = args['title']
    introduction = args['introduction']
    price = args['price']

    model = UserResource()
    if not is_param_ok(user_id, title, introduction, price):
        abort(400)
    data = model.update_user_info(user_id, title=title, introduction=introduction, price=price)
    if data:
        return to_json(data.toJson(), True)
    else:
        return to_json('User doesn\'t exist')


@user_blueprint.route('/list', methods=['POST'])
def get_user_list():
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int)
    parser.add_argument('size', type=int)
    args = parser.parse_args()
    offset = args['offset']
    size = args['size']
    if not is_param_ok(offset, size):
        abort(400)
    model = UserResource()
    data = model.get_user_list(offset, size)
    if data:
        return to_json(data, True)
    else:
        return to_json('Something wrong happened while querying')


@user_blueprint.route('/similar', methods=['POST'])
def get_similar_users():
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int)
    parser.add_argument('size', type=int)
    parser.add_argument('keyword', type=str)
    args = parser.parse_args()
    offset = args['offset']
    size = args['size']
    keyword = args['keyword']
    if not is_param_ok(offset, size, keyword):
        abort(400)
    model = UserResource()
    data = model.get_similar_users(keyword, offset, size)
    return to_json(data, True)
