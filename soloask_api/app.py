from flask import Flask
from flask.ext.restful import Api

from soloask_api.resources.user_api import UserResource, UserListResource, UserLoginResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserLoginResource, '/user/login', endpoint='login')
api.add_resource(UserResource, '/user/info', endpoint='user')
api.add_resource(UserListResource, '/user/list', endpoint='user_list')

if __name__ == '__main__':
    app.run('192.168.0.82', debug=True)
