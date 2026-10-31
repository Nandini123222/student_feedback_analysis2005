# 🎓 Student Feedback Analysis System

A simple, anonymous student feedback web application.
Built with Python Flask + SQLite. No MySQL installation needed.

---

## 📋 Table of Contents

1. [What This Project Does](#what-this-project-does)
2. [Required Software](#required-software)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [Project Folder Structure](#project-folder-structure)
5. [How to Start the Website](#how-to-start-the-website)
6. [Website Pages](#website-pages)
7. [How to Stop the Server](#how-to-stop-the-server)
8. [Common Errors and Fixes](#common-errors-and-fixes)
9. [Database Information](#database-information)
10. [Privacy Features](#privacy-features)

---

## What This Project Does

This is a **Student Feedback Analysis System** where students can:

- Submit **anonymous feedback** about courses (no name or roll number needed)
- Select a **course** and a **feedback question**
- Give a **rating from 1 to 5**
- Add an **optional comment** (stored privately, never shown publicly)

Teachers / admins can then view:

- **Course-wise average ratings**
- **Question-wise average ratings**
- **Rating distribution charts**
- **Course comparison charts**
- **Aggregated feedback reports**
- **CSV export** of the report

---

## Required Software

> **Note:** This project uses **SQLite** as its database. SQLite is built into Python — you do NOT need to install MySQL or any separate database software.

### 1. Python 3.10 or newer (Required)

**Download:** https://www.python.org/downloads/

- Click the yellow **"Download Python 3.x.x"** button
- Run the installer
- ✅ **Important:** On the first screen, check the box that says **"Add Python to PATH"** before clicking Install Now

**How to check if Python is already installed:**
Open Command Prompt and type:
```
python --version
```
If you see something like `Python 3.11.5`, Python is already installed.

---

### That's it — no other software needed!

All other requirements (Flask, Pandas, NumPy, Matplotlib) are Python packages installed automatically using `pip`.

---

## Step-by-Step Installation

### Step 1 — Download and install Python

Go to https://www.python.org/downloads/ and install Python 3.10 or newer.
Remember to check **"Add Python to PATH"** during installation.

---

### Step 2 — Extract the ZIP file

Right-click the ZIP file → **Extract All** → choose a folder (for example, your Desktop).

You should now have a folder called `StudentFeedbackSystem`.

---

### Step 3 — Open Command Prompt in the project folder

**Easy method:**
1. Open the `StudentFeedbackSystem` folder in File Explorer
2. Click on the address bar at the top (where it shows the folder path)
3. Type `cmd` and press Enter
4. A black Command Prompt window will open inside the project folder

---

### Step 4 — Install all Python packages

In the Command Prompt window, type this command exactly and press Enter:

```
pip install -r requirements.txt
```

Wait for it to finish. It will download and install Flask, Pandas, NumPy, Matplotlib, and other packages.

You should see messages ending with `Successfully installed ...`

---

### Step 5 — Load sample data (optional but recommended)

To see the dashboard with charts immediately, run this once:

```
python seed_data.py
```

You should see:
```
[DB] Database initialised successfully.
[Seed] Inserted 80 sample feedback rows.
```

This step is optional. If you skip it, the database will still be created automatically — you just won't have sample data to view on the dashboard until you submit some feedback manually.

---

### Step 6 — Start the website

```
python app.py
```

You should see:
```
[DB] Database initialised successfully.
* Running on http://127.0.0.1:5000
```

---

### Step 7 — Open in your browser

Open any browser (Chrome, Edge, Firefox) and go to:

```
http://127.0.0.1:5000
```

The website will open. 🎉

---

## Project Folder Structure

```
StudentFeedbackSystem/
│
├── app.py                 ← Main program (run this to start the website)
├── database.py            ← Database setup (creates tables automatically)
├── analytics.py           ← Statistics and chart generation
├── seed_data.py           ← Loads sample feedback data (run once)
├── database_setup.sql     ← MySQL schema (for future MySQL migration only)
├── requirements.txt       ← List of Python packages to install
├── README.md              ← This file
├── SETUP_GUIDE.md         ← Simple one-page setup guide
│
├── templates/             ← HTML pages
│   ├── base.html          ← Common navigation and layout
│   ├── index.html         ← Feedback submission form
│   ├── dashboard.html     ← Charts and statistics
│   └── reports.html       ← Aggregated report table
│
└── static/
    ├── css/
    │   └── style.css      ← Website styling
    └── charts/            ← Auto-generated chart images (created on first run)
```

**Files created automatically (not in ZIP):**
- `feedback_system.db` — SQLite database file (created when you first run `app.py`)
- `static/charts/*.png` — Chart images (generated when you visit the dashboard)

---

## How to Start the Website

Every time you want to run the project:

1. Open Command Prompt inside the `StudentFeedbackSystem` folder
2. Run:
   ```
   python app.py
   ```
3. Open browser → `http://127.0.0.1:5000`

---

## Website Pages

| Address | Page |
|---|---|
| `http://127.0.0.1:5000/` | **Feedback Form** — Submit anonymous feedback |
| `http://127.0.0.1:5000/dashboard` | **Dashboard** — Charts and statistics |
| `http://127.0.0.1:5000/reports` | **Reports** — Aggregated feedback report |
| `http://127.0.0.1:5000/export-csv` | **CSV Export** — Download report as a spreadsheet |

---

## How to Stop the Server

In the Command Prompt window where `python app.py` is running, press:

```
Ctrl + C
```

The server will stop. The website will no longer be accessible until you run `python app.py` again.

---

## Common Errors and Fixes

---

### ❌ Error: `python` is not recognized

**What it looks like:**
```
'python' is not recognized as an internal or external command
```

**Fix:**
Python was not added to PATH during installation.

**Solution A (easiest):** Uninstall Python and reinstall it.
During installation, check ✅ **"Add Python to PATH"** before clicking Install Now.

**Solution B:** Try typing `py` instead of `python`:
```
py app.py
py -m pip install -r requirements.txt
```

---

### ❌ Error: `pip` is not recognized

**What it looks like:**
```
'pip' is not recognized as an internal or external command
```

**Fix:** Try this instead:
```
python -m pip install -r requirements.txt
```

---

### ❌ Error: `No module named 'flask'` or similar

**What it looks like:**
```
ModuleNotFoundError: No module named 'flask'
```

**Fix:** You haven't installed the packages yet. Run:
```
pip install -r requirements.txt
```

---

### ❌ Error: `Address already in use` or `Port 5000`

**What it looks like:**
```
OSError: [Errno 98] Address already in use
```

**Fix:** Another program is already using port 5000, or the server is already running.

- Close any other Command Prompt windows running `python app.py`
- Or restart your computer and try again

---

### ❌ The website is blank or shows an error page

**Fix:** Make sure you ran `python app.py` first and you can see the message:
```
* Running on http://127.0.0.1:5000
```
Then open the browser and go to `http://127.0.0.1:5000`

---

### ❌ Dashboard shows "No data available"

**Fix:** Either submit some feedback using the form, or run the sample data script:
```
python seed_data.py
```

Then refresh the dashboard page.

---

### ❌ Charts are not showing on the dashboard

**Fix:** Visit the dashboard once — charts are generated on the first visit.
Make sure the `static/charts/` folder exists (it is included in the ZIP).
If charts still don't appear, try refreshing the page (Ctrl + R).

---

## Database Information

This project uses **SQLite**, which is built into Python. No separate database software needs to be installed.

The database is stored as a single file: `feedback_system.db`

It is created **automatically** the first time you run `python app.py`.

**Database tables:**

| Table | Columns |
|---|---|
| `courses` | course_id, course_name |
| `feedback_questions` | question_id, question_text |
| `feedback` | feedback_id, course_id, question_id, rating, comment_optional, submitted_at |

**Want to use MySQL instead?**
A `database_setup.sql` file is included. See the comments inside that file for migration instructions.

---

## Privacy Features

- ❌ No student names collected
- ❌ No roll numbers collected
- ✅ All feedback is anonymous
- ✅ Ratings are validated (must be 1 to 5)
- ✅ Individual comments are **never** displayed publicly
- ✅ Aggregated reports are **suppressed** for groups with fewer than 5 responses

---

*Student Feedback Analysis System — Beginner Project*
