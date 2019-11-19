import functools
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash, url_for, g

app = Flask(__name__)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = 'admin'
        passw = 'password'

        if username != user:
            error = 'Incorrect username.'
        elif passw != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user
            return redirect('/dashboard')

        flash(error)

    return render_template('login.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(r'D:\Coding Projects\IS211_Assignment12\hw12.db')
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM students")
        student_rows = cur.fetchall()

        cur.execute("SELECT * FROM quizzes")
        quiz_rows = cur.fetchall()
        

    return render_template('dashboard.html', student_rows = student_rows, quiz_rows = quiz_rows)

if __name__ == '__main__':
    app.secret_key = 'sekrit'
    app.run()