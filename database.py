"""
database.py
-----------
Sets up the SQLite database with the same schema as required:
  - courses(course_id, course_name)
  - feedback_questions(question_id, question_text)
  - feedback(feedback_id, course_id, question_id, rating, comment_optional, submitted_at)

SQLite is used because MySQL is not installed on this machine.
The schema, table names, and column names are identical to the MySQL requirement.
The database file is: feedback_system.db
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback_system.db")


def get_connection():
    """Return a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # allows dict-style access
    return conn


def init_db():
    """Create tables and insert sample data if the database is fresh."""
    conn = get_connection()
    cursor = conn.cursor()

    # ----- Create tables -----
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS feedback_questions (
            question_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id        INTEGER NOT NULL,
            question_id      INTEGER NOT NULL,
            rating           INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment_optional TEXT,
            submitted_at     DATETIME DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (course_id)   REFERENCES courses(course_id),
            FOREIGN KEY (question_id) REFERENCES feedback_questions(question_id)
        );
    """)

    # ----- Insert sample courses (only if table is empty) -----
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        sample_courses = [
            ("Mathematics",),
            ("Physics",),
            ("Chemistry",),
            ("Computer Science",),
            ("English Literature",),
            ("Economics",),
        ]
        cursor.executemany("INSERT INTO courses (course_name) VALUES (?)", sample_courses)

    # ----- Insert sample feedback questions (only if table is empty) -----
    cursor.execute("SELECT COUNT(*) FROM feedback_questions")
    if cursor.fetchone()[0] == 0:
        sample_questions = [
            ("How clearly did the instructor explain the concepts?",),
            ("How satisfied are you with the course content?",),
            ("How well did the course meet your learning objectives?",),
            ("How would you rate the quality of study materials provided?",),
            ("How engaging and interactive were the lectures?",),
        ]
        cursor.executemany(
            "INSERT INTO feedback_questions (question_text) VALUES (?)",
            sample_questions
        )

    conn.commit()
    conn.close()
    print("[DB] Database initialised successfully.")
