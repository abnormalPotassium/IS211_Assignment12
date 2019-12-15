import sqlite3
from sqlite3 import Error
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
hw12_db = os.path.join(THIS_FOLDER, 'hw12.db')
hw_schema = os.path.join(THIS_FOLDER, 'schema.sql')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def define_table(db_file,script):
    conn = sqlite3.connect(db_file)
    with conn:
        cur = conn.cursor()

        qry = open(script,'r').read()
        cur.executescript(qry)

def load_table(db_file):
    conn = sqlite3.connect(db_file)
    with conn:
        cur = conn.cursor()

        students = (
            ('Smith', 'John')
        )

        quizzes = (
            ('Python Basics', 5, 'February, 5th, 2015')
        )

        student_results = (
            (1, 1, 85)
        )

        cur.execute("INSERT INTO students VALUES(null,?,?)", students)
        cur.execute("INSERT INTO quizzes VALUES(null,?,?,?)", quizzes)
        cur.execute("INSERT INTO student_results VALUES(?,?,?)", student_results)

if __name__ == '__main__':
    create_connection(hw12_db)
    define_table(hw12_db, hw_schema)
    load_table(hw12_db)