from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)
tasks = [
    {
        'id': 1,
        'title': u'Honda',
        'description': u'CBF190',
        'done': False
    },
    {
        'id': 1,
        'title': u'Honda',
        'description': u'CBF190',
        'done': False
    }
]


# get task list
@app.route('/api/v1.0/tasks', methods=['POST', 'GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


# get task detail
@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# add task into tasks
@app.route('/api/v1.0/tasks', methods=['POST'])
def add_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'NOT Found'}), 404)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
