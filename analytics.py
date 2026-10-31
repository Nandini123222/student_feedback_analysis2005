"""
analytics.py
------------
Pure functions for computing feedback statistics.
Uses Pandas and NumPy — no ML, no sentiment analysis.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-GUI backend (works without a display)
import matplotlib.pyplot as plt
import os
import io

from database import get_connection

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "static", "charts")
MIN_RESPONSES = 5              # suppress reports with fewer responses (privacy)


# ---------------------------------------------------------------------------
# Helper: load all feedback into a DataFrame
# ---------------------------------------------------------------------------

def load_feedback_df():
    """Return a DataFrame of all feedback rows joined with course / question names."""
    conn = get_connection()
    query = """
        SELECT
            f.feedback_id,
            c.course_name,
            q.question_text,
            f.rating,
            f.submitted_at
        FROM feedback f
        JOIN courses c ON f.course_id = c.course_id
        JOIN feedback_questions q ON f.question_id = q.question_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ---------------------------------------------------------------------------
# 1. Course-wise average ratings
# ---------------------------------------------------------------------------

def get_course_averages():
    """
    Returns a list of dicts:
        [{'course_name': ..., 'avg_rating': ..., 'response_count': ...}, ...]
    Courses with fewer than MIN_RESPONSES entries are excluded (privacy).
    """
    df = load_feedback_df()
    if df.empty:
        return []

    grouped = (
        df.groupby("course_name")["rating"]
        .agg(avg_rating="mean", response_count="count")
        .reset_index()
    )
    grouped = grouped[grouped["response_count"] >= MIN_RESPONSES]
    grouped["avg_rating"] = grouped["avg_rating"].round(2)
    return grouped.to_dict(orient="records")


# ---------------------------------------------------------------------------
# 2. Question-wise average ratings
# ---------------------------------------------------------------------------

def get_question_averages():
    """
    Returns a list of dicts:
        [{'question_text': ..., 'avg_rating': ..., 'response_count': ...}, ...]
    Questions with fewer than MIN_RESPONSES entries are excluded.
    """
    df = load_feedback_df()
    if df.empty:
        return []

    grouped = (
        df.groupby("question_text")["rating"]
        .agg(avg_rating="mean", response_count="count")
        .reset_index()
    )
    grouped = grouped[grouped["response_count"] >= MIN_RESPONSES]
    grouped["avg_rating"] = grouped["avg_rating"].round(2)
    return grouped.to_dict(orient="records")


# ---------------------------------------------------------------------------
# 3. Overall response counts per course
# ---------------------------------------------------------------------------

def get_response_counts():
    """Returns total feedback count per course (all, not privacy-filtered)."""
    df = load_feedback_df()
    if df.empty:
        return []
    counts = (
        df.groupby("course_name")["rating"]
        .count()
        .reset_index()
        .rename(columns={"rating": "response_count"})
    )
    return counts.to_dict(orient="records")


# ---------------------------------------------------------------------------
# 4. Rating distribution (1-5) per course
# ---------------------------------------------------------------------------

def get_rating_distribution():
    """
    Returns a dict: { course_name: {1: n, 2: n, 3: n, 4: n, 5: n} }
    Only courses with >= MIN_RESPONSES responses are included.
    """
    df = load_feedback_df()
    if df.empty:
        return {}

    result = {}
    for course, group in df.groupby("course_name"):
        if len(group) < MIN_RESPONSES:
            continue
        dist = {i: int((group["rating"] == i).sum()) for i in range(1, 6)}
        result[course] = dist
    return result


# ---------------------------------------------------------------------------
# 5. Chart: rating distribution per course  (bar chart)
# ---------------------------------------------------------------------------

def generate_distribution_chart(course_name):
    """
    Generates a bar chart of rating distribution for a single course.
    Saves to static/charts/dist_<safe_name>.png and returns the filename.
    Returns None if fewer than MIN_RESPONSES responses exist.
    """
    df = load_feedback_df()
    course_df = df[df["course_name"] == course_name]
    if len(course_df) < MIN_RESPONSES:
        return None

    ratings = np.arange(1, 6)
    counts = [(course_df["rating"] == r).sum() for r in ratings]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(ratings, counts, color="#4A90D9", edgecolor="white", width=0.6)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Number of Responses", fontsize=12)
    ax.set_title(f"Rating Distribution – {course_name}", fontsize=14)
    ax.set_xticks(ratings)
    ax.set_ylim(0, max(counts) + 2 if max(counts) > 0 else 5)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(count), ha="center", va="bottom", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    safe_name = course_name.replace(" ", "_").replace("/", "-")
    filename = f"dist_{safe_name}.png"
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return filename


# ---------------------------------------------------------------------------
# 6. Chart: course comparison bar chart (average ratings)
# ---------------------------------------------------------------------------

def generate_course_comparison_chart():
    """
    Generates a horizontal bar chart comparing average ratings across courses.
    Returns filename string or None if not enough data.
    """
    data = get_course_averages()
    if not data:
        return None

    courses = [d["course_name"] for d in data]
    averages = [d["avg_rating"] for d in data]

    fig, ax = plt.subplots(figsize=(8, max(4, len(courses) * 0.7 + 1)))
    y_pos = np.arange(len(courses))
    bars = ax.barh(y_pos, averages, color="#5CB85C", edgecolor="white", height=0.55)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(courses, fontsize=11)
    ax.set_xlabel("Average Rating (out of 5)", fontsize=12)
    ax.set_title("Course Comparison – Average Ratings", fontsize=14)
    ax.set_xlim(0, 5.5)
    for bar, avg in zip(bars, averages):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{avg}", va="center", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    filename = "course_comparison.png"
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return filename


# ---------------------------------------------------------------------------
# 7. Aggregated feedback report (for CSV export)
# ---------------------------------------------------------------------------

def get_aggregated_report():
    """
    Returns a list of dicts representing the full aggregated report:
    course, question, avg_rating, response_count.
    Only groups with >= MIN_RESPONSES responses included.
    """
    df = load_feedback_df()
    if df.empty:
        return []

    grouped = (
        df.groupby(["course_name", "question_text"])["rating"]
        .agg(avg_rating="mean", response_count="count")
        .reset_index()
    )
    grouped = grouped[grouped["response_count"] >= MIN_RESPONSES]
    grouped["avg_rating"] = grouped["avg_rating"].round(2)
    return grouped.to_dict(orient="records")


# ---------------------------------------------------------------------------
# 8. CSV export helper (returns CSV bytes)
# ---------------------------------------------------------------------------

def export_report_csv():
    """Returns the aggregated report as CSV bytes (for Flask send_file)."""
    data = get_aggregated_report()
    if not data:
        df_empty = pd.DataFrame(
            columns=["course_name", "question_text", "avg_rating", "response_count"]
        )
        return df_empty.to_csv(index=False).encode("utf-8")

    df = pd.DataFrame(data)
    df.rename(columns={
        "course_name": "Course",
        "question_text": "Question",
        "avg_rating": "Average Rating",
        "response_count": "Response Count"
    }, inplace=True)
    return df.to_csv(index=False).encode("utf-8")
