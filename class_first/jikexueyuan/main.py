from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from wtforms import Form, TextField, PasswordField
from wtforms import validators

from class_first.jikexueyuan.model import User

app = Flask(__name__)


class LoginForm(Form):
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])


@app.route("/register", methods=['GET', 'POST'])
def register():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        u = User(myForm.username.data, myForm.password.data)
        u.add()
        return redirect("http://www.baidu.com")
    return render_template('index.html', form=myForm)


@app.route("/login", methods=['GET', 'POST'])
def login():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        u = User(myForm.username.data, myForm.password.data)
        if u.isUserExisted():
            return redirect("http://www.baidu.com")
        else:
            return "Login failed"
    return render_template('index.html', form=myForm)


if __name__ == "__main__":
    app.run(port=8080)
