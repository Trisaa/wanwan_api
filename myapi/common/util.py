from functools import wraps

from flask import jsonify
from flask.ext.restful import reqparse
from itsdangerous import Serializer, SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from myapi.config import Config


def to_json(data, success=False):
    if success:
        return jsonify({'data': data, 'code': 1, 'message': 'Success'})
    return jsonify({'data': {}, 'code': 0, 'message': data})


def gen_token(uid, expiration=30 * 24 * 60 * 60):
    s = Serializer(Config.SERECT_KEY, expires_in=expiration)
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
        s = Serializer(Config.SERECT_KEY)
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
