import functools
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, session, flash, url_for, g
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
hw12_db = os.path.join(THIS_FOLDER, 'hw12.db')

app = Flask(__name__)

@app.route('/', methods= ['GET', 'POST'])
@app.route('/login', methods= ['GET', 'POST'])
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
            return redirect('/login')

        return view(**kwargs)

    return wrapped_view

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(hw12_db)
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM students")
        student_rows = cur.fetchall()

        cur.execute("SELECT * FROM quizzes")
        quiz_rows = cur.fetchall()
        

    return render_template('dashboard.html', student_rows = student_rows, quiz_rows = quiz_rows)

@app.route('/student/add', methods = ['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        last = request.form['student_last_name']
        first = request.form['student_first_name']
        conn = sqlite3.connect(hw12_db)
        cur = conn.cursor()
        with conn:
            try:
                cur.execute("INSERT INTO students VALUES(null,?,?)", [last,first])
                return redirect('/dashboard')
            except Error as e:
                flash(e)
                return redirect('/student/add')
        
    return render_template('add_student.html')

@app.route('/quiz/add', methods = ['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'POST':
        subject = request.form['quiz_subject']
        questions = request.form['quiz_questions']
        date = request.form['quiz_date']
        conn = sqlite3.connect(hw12_db)
        cur = conn.cursor()
        with conn:
            try:
                cur.execute("INSERT INTO quizzes VALUES(null,?,?,?)", [subject,questions,date])
                return redirect('/dashboard')
            except Error as e:
                flash(e)
                return redirect('/quiz/add')
        
    return render_template('add_quiz.html')

@app.route('/student/<ID>')
@login_required
def view_quiz_results(ID):
    conn = sqlite3.connect(hw12_db)
    cur = conn.cursor()
    with conn:
        try:
            cur.execute("""
                    SELECT students.student_first_name, students.student_last_name, student_results.quiz_id, student_results.quiz_score
                    FROM students
                    INNER JOIN student_results ON students.student_id = student_results.student_id
                    WHERE students.student_id=?""",ID)
            results = cur.fetchall()
            return render_template('quiz_results.html', quiz_result = results)
        except Error as e:
            flash(e)
            return render_template('quiz_results.html', quiz_result = None)

@app.route('/results/add', methods = ['GET', 'POST'])
@login_required
def add_results():
    if request.method == 'POST':
        student = request.form['student']
        quiz = request.form['quiz']
        score = request.form['quiz_score']
        conn = sqlite3.connect(hw12_db)
        cur = conn.cursor()
        with conn:
            try:
                cur.execute("INSERT INTO student_results VALUES(?,?,?)", [student,quiz,score])
                return redirect('/dashboard')
            except Error as e:
                flash(e)
                return redirect('/results/add')
    
    conn = sqlite3.connect(hw12_db)
    cur = conn.cursor()
    with conn:
        cur.execute("SELECT * FROM students")
        student_rows = cur.fetchall()

        cur.execute("SELECT * FROM quizzes")
        quiz_rows = cur.fetchall()

    return render_template('add_quiz_result.html', student_rows = student_rows, quiz_rows = quiz_rows)


if __name__ == '__main__':
    app.secret_key = 'sekrit'
    app.run()