from flask import Blueprint
from flask.ext.restful import reqparse, abort

from myapi.common.util import is_param_ok, to_json
from myapi.resources.withdraw import WithdrawResource

withdraw_blueprint = Blueprint('withdraw', __name__)


@withdraw_blueprint.route('/create', methods=['POST'])
def create():
    parser = reqparse.RequestParser()
    parser.add_argument('paypal', type=str)
    parser.add_argument('user_id', type=int)
    args = parser.parse_args()
    paypal = args['paypal']
    user_id = args['user_id']
    if not is_param_ok(paypal, user_id):
        abort(400)
    api = WithdrawResource()
    withdraw = api.create_withdraw(paypal, user_id)
    if withdraw:
        return to_json(withdraw.toJson(), True)
    else:
        return to_json('withdraw failed')
