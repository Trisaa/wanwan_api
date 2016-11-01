from functools import wraps

from flask import jsonify
from flask.ext.restful import reqparse
from itsdangerous import Serializer, SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from soloask_api.common.config import SERECT_KEY


def to_json(data, success=False):
    if success:
        return jsonify({'data': data, 'code': 1})
    return jsonify({'data': data, 'code': 0})


def gen_token(uid, expiration=30 * 24 * 60 * 60):
    s = Serializer(SERECT_KEY, expires_in=expiration)
    return s.dumps({'id': uid})


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        token = args['token']
        if token is None:
            return to_json('token required')
        s = Serializer(SERECT_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return to_json('token expired')
        except BadSignature:
            return to_json('token useless')
        kwargs['id'] = data['id']
        return func(*args, **kwargs)

    return wrapper


def is_param_ok(*args):
    for arg in args:
        if arg is None:
            return False
    return True
