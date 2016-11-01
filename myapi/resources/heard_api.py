from flask import Blueprint
from flask.ext.restful import reqparse, abort

from myapi.common.util import is_param_ok, to_json
from myapi.resources.heard import HeardResource

heard_blueprint = Blueprint('heard', __name__)


@heard_blueprint.route('/add', methods=['POST'])
def add():
    parser = reqparse.RequestParser()
    parser.add_argument('question_id', type=int)
    parser.add_argument('user_id', type=int)
    args = parser.parse_args()
    question_id = args['question_id']
    user_id = args['user_id']
    if not is_param_ok(question_id, user_id):
        abort(400)
    api = HeardResource()
    heard = api.set_heard_user(question_id, user_id)
    if heard:
        return to_json(heard.toJson(), True)
    else:
        return to_json('add heard user failed')


@heard_blueprint.route('/list', methods=['POST'])
def get_heard_questions():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int)
    parser.add_argument('offset', type=int)
    parser.add_argument('size', type=int)
    args = parser.parse_args()
    user_id = args['user_id']
    offset = args['offset']
    size = args['size']
    if not is_param_ok(user_id, offset, size):
        abort(400)
    api = HeardResource()
    data = api.get_user_heard_questions(user_id, offset, size)
    return to_json(data, True)


@heard_blueprint.route('/check', methods=['POST'])
def check_user_heard():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int)
    parser.add_argument('question_id', type=int)
    args = parser.parse_args()
    user_id = args['user_id']
    question_id = args['question_id']
    if not is_param_ok(user_id, question_id):
        abort(400)
    api = HeardResource()
    data = api.check_user_heard_question(user_id, question_id)
    if data:
        return to_json('heard', True)
    else:
        return to_json('unheard', True)
