# model.py
from flask import jsonify

from flask import abort

from flask import request

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lebron@localhost/testdb'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @app.route('/api/user/create', methods=['POST'])
    def create_user(self):
        if not request.json or not 'username' in request.json:
            abort(400)
        try:
            user = User(request.json.username, request.json.get('password', '123456'))
            db.session.add(user)
            db.session.commit()
            return jsonify({'username': user.username})
        except Exception, e:
            db.session.rollback()
            return e
        finally:
            return 0

    @app.route('/api/user/<user_id>', methods=['GET'])
    def get_userinfo(self, user_id):
        return jsonify({'user': User.query.get(user_id)})

    @app.route('/api/user', methods=['GET'])
    def get_all_user(self):
        return jsonify({'user_list': User.query.all()})

    def isUserExisted(self):
        tempUser = User.query.filter_by(username=self.username, password=self.password).first()
        if tempUser is None:
            return 0
        else:
            return 1


if __name__ == "__main__":
    app.run(debug=True)
