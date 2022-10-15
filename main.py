from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flask
from firebase import firebase, db

app = flask.Flask(__name__)
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            data = {"password": password, "sleep": 0, "noise": 0, "roommate_num": 0, "phil_response": 0}
            db.child("users").child(username).set(data)
            return redirect(url_for('index'))

        flash(error)

    return render_template('register.html')
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = db.child("users")

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

if __name__ == '__main__':
    app.run()