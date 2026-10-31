"""
app.py
------
Main Flask application for the Student Feedback Analysis System.
Run with:  python app.py
Open:      http://127.0.0.1:5000
"""

import os
import io
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_file, jsonify
)
from database import get_connection, init_db
import analytics

app = Flask(__name__)
app.secret_key = "feedback_system_secret_2024"   # needed for flash messages

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "static", "charts")


# ---------------------------------------------------------------------------
# Initialise the database on startup
# ---------------------------------------------------------------------------

with app.app_context():
    init_db()
    os.makedirs(CHARTS_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Helper: fetch courses and questions for forms
# ---------------------------------------------------------------------------

def fetch_courses():
    conn = get_connection()
    rows = conn.execute("SELECT course_id, course_name FROM courses ORDER BY course_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_questions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT question_id, question_text FROM feedback_questions ORDER BY question_id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Route: Home / Feedback Submission Form
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    courses = fetch_courses()
    questions = fetch_questions()

    if request.method == "POST":
        course_id = request.form.get("course_id")
        question_id = request.form.get("question_id")
        rating = request.form.get("rating")
        comment = request.form.get("comment", "").strip()

        # ----- Validation -----
        errors = []
        if not course_id:
            errors.append("Please select a course.")
        if not question_id:
            errors.append("Please select a feedback question.")
        if not rating:
            errors.append("Please select a rating.")
        else:
            try:
                rating_int = int(rating)
                if rating_int < 1 or rating_int > 5:
                    errors.append("Rating must be between 1 and 5.")
            except ValueError:
                errors.append("Invalid rating value.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("index.html", courses=courses, questions=questions)

        # ----- Store in database -----
        try:
            conn = get_connection()
            conn.execute(
                """INSERT INTO feedback (course_id, question_id, rating, comment_optional)
                   VALUES (?, ?, ?, ?)""",
                (int(course_id), int(question_id), rating_int,
                 comment if comment else None)
            )
            conn.commit()
            conn.close()
            flash("Your feedback has been submitted successfully. Thank you!", "success")
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")

        return redirect(url_for("index"))

    return render_template("index.html", courses=courses, questions=questions)


# ---------------------------------------------------------------------------
# Route: Dashboard (statistics overview)
# ---------------------------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    course_averages = analytics.get_course_averages()
    question_averages = analytics.get_question_averages()
    response_counts = analytics.get_response_counts()
    rating_distribution = analytics.get_rating_distribution()

    # Generate comparison chart
    comparison_chart = analytics.generate_course_comparison_chart()

    # Generate per-course distribution charts
    dist_charts = {}
    for course_name in rating_distribution.keys():
        fname = analytics.generate_distribution_chart(course_name)
        if fname:
            dist_charts[course_name] = fname

    total_responses = sum(d["response_count"] for d in response_counts)

    return render_template(
        "dashboard.html",
        course_averages=course_averages,
        question_averages=question_averages,
        response_counts=response_counts,
        rating_distribution=rating_distribution,
        comparison_chart=comparison_chart,
        dist_charts=dist_charts,
        total_responses=total_responses,
        min_responses=analytics.MIN_RESPONSES,
    )


# ---------------------------------------------------------------------------
# Route: Reports page
# ---------------------------------------------------------------------------

@app.route("/reports")
def reports():
    report_data = analytics.get_aggregated_report()
    return render_template("reports.html", report_data=report_data,
                           min_responses=analytics.MIN_RESPONSES)


# ---------------------------------------------------------------------------
# Route: CSV Export
# ---------------------------------------------------------------------------

@app.route("/export-csv")
def export_csv():
    csv_bytes = analytics.export_report_csv()
    return send_file(
        io.BytesIO(csv_bytes),
        mimetype="text/csv",
        as_attachment=True,
        download_name="feedback_report.csv"
    )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
