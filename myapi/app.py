from flask import Flask

from myapi.resources.heard_api import heard_blueprint
from myapi.resources.question_api import question_blueprint
from myapi.resources.user_api import user_blueprint
from myapi.resources.withdraw_api import withdraw_blueprint


def register_blueprint(app):
    blueprints = [
        (user_blueprint, '/api/user'),
        (question_blueprint, '/api/question'),
        (heard_blueprint, '/api/heard'),
        (withdraw_blueprint, '/api/withdraw')
    ]
    for module, prefix in blueprints:
        app.register_blueprint(module, url_prefix=prefix)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_blueprint(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='192.168.0.82', debug=True)
