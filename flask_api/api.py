from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.restful import reqparse

app = Flask(__name__)
api = Api(app)


class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='user\'s name')
            parser.add_argument('password', type=str, help='user\'s password')
            args = parser.parse_args()

            _userName = args['username']
            _userPassword = args['password']
            return {'name': args['username'], 'password': args['password']}
        except Exception as e:
            return {'error': str(e)}


api.add_resource(CreateUser, '/createuser')

if __name__ == '__main__':
    app.run(debug=True)
