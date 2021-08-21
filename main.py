from flask import Flask, render_template, request, url_for, redirect, flash, session

from database_connection import get_connection_string, open_database, connection_handler

import data_manager

app = Flask(__name__)

app.secret_key = data_manager.get_secret_key()


@app.route('/', methods=["GET", "POST"])
def login():
    get_connection_string()
    open_database()

    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # print(data_manager.account_exists(username, password))

        if data_manager.account_exists(username, password):
            print("1")
            session['username'] = request.form.get('username')
            session['password'] = request.form.get('password')
            return redirect(url_for('home', username=username))
        else:
            print(data_manager.account_exists(username, password))
            return redirect(url_for("register"))


@app.route('/logout')
def logout():
    session.pop('username', default=None)
    session.pop('password', default=None)
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        registration_date = data_manager.get_time()
        sex = request.form.get('sex')
        age = request.form.get('age')
        data_manager.register_user(username, password, registration_date, sex, age)
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route('/home/username')
def home():
    if session['username']:
        information = data_manager.get_all_questions()
        return render_template('home.html', username=session['username'], information=information)


@app.route('/home/show_users')
def get_all_users():
    information = data_manager.get_all_users()
    return render_template("all_users.html", information=information)


@app.route('/home/post_question', methods=["GET", "POST"])
def post_a_question():
    if request.method == "POST":
        id_user = data_manager.get_user_id(session['username'])
        question_title = request.form.get('title')
        question_message = request.form.get('message')
        id_user = id_user[0].get('id_user')
        data_manager.post_question(question_title, question_message, id_user)
        return redirect(url_for("home"))
    else:
        return render_template("post_question.html")


if __name__ == '__main__':
    app.run(debug=True)
