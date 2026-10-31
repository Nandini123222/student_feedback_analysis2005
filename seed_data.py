"""
seed_data.py
------------
Inserts sample feedback rows so the dashboard and reports
are populated immediately on first run.

Run once: python seed_data.py
"""

import random
from database import get_connection, init_db

def seed():
    init_db()
    conn = get_connection()

    courses = conn.execute("SELECT course_id FROM courses").fetchall()
    questions = conn.execute("SELECT question_id FROM feedback_questions").fetchall()

    # Check existing rows
    existing = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    if existing >= 30:
        print(f"[Seed] Already have {existing} feedback rows — skipping seed.")
        conn.close()
        return

    random.seed(42)
    rows = []
    for _ in range(80):
        course_id   = random.choice(courses)["course_id"]
        question_id = random.choice(questions)["question_id"]
        # Slightly positive distribution
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 40, 25])[0]
        rows.append((course_id, question_id, rating, None))

    conn.executemany(
        "INSERT INTO feedback (course_id, question_id, rating, comment_optional) VALUES (?,?,?,?)",
        rows
    )
    conn.commit()
    conn.close()
    print(f"[Seed] Inserted {len(rows)} sample feedback rows.")

if __name__ == "__main__":
    seed()
