from flask import Blueprint
from flask import request
from flask.ext.restful import reqparse, abort

from myapi.common.util import is_param_ok, to_json
from myapi.resources.question import QuestionResource

question_blueprint = Blueprint('question', __name__)


@question_blueprint.route('/')
def index():
    return 'hello world'


@question_blueprint.route('/create', methods=['POST'])
def create_question():
    parser = reqparse.RequestParser()
    parser.add_argument('content', type=str)
    parser.add_argument('price', type=float)
    parser.add_argument('public', type=int)
    parser.add_argument('ask_uuid', type=int)
    parser.add_argument('answer_uuid', type=int)
    args = parser.parse_args()
    content = args['content']
    price = args['price']
    public = args['public']
    asker = args['ask_uuid']
    answer = args['answer_uuid']
    if not is_param_ok(content, price, public, asker, answer):
        abort(400)
    api = QuestionResource()
    question = api.create_question(content=content, price=price, public=public, ask_uuid=asker, answer_uuid=answer)
    if question:
        return to_json(question.toJson(), True)
    else:
        return to_json('create the question failed')


@question_blueprint.route('/answer', methods=['POST'])
def answer_question():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('url', type=str)
    parser.add_argument('length', type=int)
    args = parser.parse_args()
    id = args['id']
    url = args['url']
    length = args['length']
    if not is_param_ok(id, url, length):
        abort(400)
    api = QuestionResource()
    question = api.answer_question(id, length, url)
    if question:
        return to_json(question.toJson(), True)
    else:
        return 'answer question failed'


@question_blueprint.route('/related', methods=['POST'])
def get_related_questions():
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('user_id', type=int)
    parser.add_argument('offset', type=int)
    parser.add_argument('size', type=int)
    args = parser.parse_args()
    request_type = args['type']
    user_id = args['user_id']
    offset = args['offset']
    size = args['size']
    if not is_param_ok(request_type, user_id, offset, size):
        abort(400)
    api = QuestionResource()
    data = api.get_related_questions(request_type, user_id, offset, size)
    return to_json(data, True)


@question_blueprint.route('/hot', methods=['POST'])
def get_hot_questions():
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int, location='json')
    parser.add_argument('size', type=int, location='json')
    args = parser.parse_args()
    # args = request.get_json(force=True)
    offset = args['offset']
    size = args['size']
    if not is_param_ok(offset, size):
        abort(400)
    api = QuestionResource()
    data = api.get_hot_questions(offset, size)
    return to_json(data, True)


@question_blueprint.route('/similar', methods=['POST'])
def get_similar_questions():
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int)
    parser.add_argument('size', type=int)
    parser.add_argument('keyword', type=str)
    args = parser.parse_args()
    # args = request.get_json(force=True)
    offset = args['offset']
    size = args['size']
    keyword = args['keyword']
    if not is_param_ok(offset, size, keyword):
        abort(400)
    api = QuestionResource()
    data = api.get_similar_questions(keyword, offset, size)
    return to_json(data, True)


@question_blueprint.route('/detail', methods=['POST'])
def get_question_detail():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    args = parser.parse_args()
    id = args['id']
    if not is_param_ok(id):
        abort(400)
    api = QuestionResource()
    question = api.get_question_detail(id)
    if question:
        return to_json(question.toJson(), True)
    else:
        return to_json('get question detail failed')
