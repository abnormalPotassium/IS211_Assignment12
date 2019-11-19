DROP TABLE IF EXISTS students;
CREATE TABLE students
( 
	student_id INTEGER PRIMARY KEY,
    student_last_name varchar(255) NOT NULL,
    student_first_name varchar(255) NOT NULL
);

DROP TABLE IF EXISTS quizzes;
CREATE TABLE quizzes
(
	quiz_id INTEGER PRIMARY KEY,
    quiz_subject varchar(255) NOT NULL,
    quiz_questions int NOT NULL,
    quiz_date date NOT NULL
);

DROP TABLE IF EXISTS student_results;
CREATE TABLE student_results
(
    student_id INT,
    quiz_id INT,
    quiz_score INT,
    FOREIGN KEY (student_id)
        REFERENCES students(student_id),
    FOREIGN KEY (quiz_id)
        REFERENCES quizzes(quiz_id)
);