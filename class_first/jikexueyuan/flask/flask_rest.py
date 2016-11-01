from flask import Flask
from flask.ext.restful import Api, Resource, abort
from flask.ext.restful import reqparse

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': "set up the project"},
    'todo2': {'task': "build the project"},
    'todo3': {'task': "run the project"}
}


def abort_if_todo_is_none(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


class TaskListAPI(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = 'todo%i' % 100
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class TaskAPI(Resource):
    def get(self, id):
        abort_if_todo_is_none(id)
        return TODOS[id]

    def delete(self, id):
        abort_if_todo_is_none(id)
        del TODOS[id]
        return '', 204


api.add_resource(TaskListAPI, '/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/api/v1.0/task/<id>', endpoint='task')

if __name__ == '__main__':
    app.run(debug=True)
