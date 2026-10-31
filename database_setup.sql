-- ============================================================
-- database_setup.sql
-- MySQL equivalent schema for Student Feedback Analysis System
-- NOTE: This project currently uses SQLite (feedback_system.db)
--       because MySQL is not installed on this machine.
--       To migrate to MySQL later:
--         1. Install MySQL Server
--         2. Create a database: CREATE DATABASE feedback_db;
--         3. Run this file: mysql -u root -p feedback_db < database_setup.sql
--         4. Update database.py to use mysql.connector instead of sqlite3
-- ============================================================

CREATE DATABASE IF NOT EXISTS feedback_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE feedback_db;

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id   INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(200) NOT NULL UNIQUE
);

-- Feedback questions table
CREATE TABLE IF NOT EXISTS feedback_questions (
    question_id   INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL
);

-- Feedback table (anonymous, no student identifiers)
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id      INT AUTO_INCREMENT PRIMARY KEY,
    course_id        INT NOT NULL,
    question_id      INT NOT NULL,
    rating           TINYINT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment_optional TEXT,
    submitted_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_course   FOREIGN KEY (course_id)   REFERENCES courses(course_id),
    CONSTRAINT fk_question FOREIGN KEY (question_id) REFERENCES feedback_questions(question_id)
);

-- Sample data
INSERT IGNORE INTO courses (course_name) VALUES
    ('Mathematics'),
    ('Physics'),
    ('Chemistry'),
    ('Computer Science'),
    ('English Literature'),
    ('Economics');

INSERT IGNORE INTO feedback_questions (question_text) VALUES
    ('How clearly did the instructor explain the concepts?'),
    ('How satisfied are you with the course content?'),
    ('How well did the course meet your learning objectives?'),
    ('How would you rate the quality of study materials provided?'),
    ('How engaging and interactive were the lectures?');
