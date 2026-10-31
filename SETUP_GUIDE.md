# 🪟 Windows Setup Guide
## Student Feedback Analysis System — Quick Start for Beginners

Follow these steps **in order**. Each step has a checkmark so you know where you are.

---

## PART 1 — Install Python

### [ ] Step 1: Check if Python is already installed

1. Press the **Windows key** on your keyboard
2. Type `cmd` and press Enter (Command Prompt opens)
3. Type this and press Enter:
   ```
   python --version
   ```
4. If you see `Python 3.10.x` or higher → **Python is already installed, skip to Part 2**
5. If you see an error → continue to Step 2

---

### [ ] Step 2: Download Python

Open your browser and go to:

> **https://www.python.org/downloads/**

Click the big yellow button: **"Download Python 3.x.x"**

---

### [ ] Step 3: Install Python

1. Open the downloaded file (e.g., `python-3.12.0-amd64.exe`)
2. ✅ **CHECK THIS BOX FIRST:** `Add Python to PATH` (very important!)
3. Click **Install Now**
4. Wait for it to finish
5. Click **Close**

---

### [ ] Step 4: Verify Python installed correctly

1. Close any Command Prompt windows that were open
2. Open a new Command Prompt (Windows key → type `cmd` → Enter)
3. Type:
   ```
   python --version
   ```
4. You should see: `Python 3.12.0` (or similar)

✅ **Python is ready!**

---

## PART 2 — Set Up the Project

### [ ] Step 5: Extract the ZIP file

1. Find the file `StudentFeedbackSystem.zip`
2. Right-click on it
3. Select **Extract All...**
4. Choose where to save it (Desktop is fine)
5. Click **Extract**

You now have a folder called `StudentFeedbackSystem`.

---

### [ ] Step 6: Open Command Prompt inside the project folder

1. Open the `StudentFeedbackSystem` folder in File Explorer
2. Click on the **address bar** at the top of the window
   (it shows something like `C:\Users\YourName\Desktop\StudentFeedbackSystem`)
3. **Delete** what's in the address bar
4. Type exactly: `cmd`
5. Press **Enter**

A black Command Prompt window will open. You should see your folder path on the left side.

---

### [ ] Step 7: Install Python packages

In the Command Prompt window, type this exactly and press Enter:

```
pip install -r requirements.txt
```

⏳ Wait for it to finish (may take 1–3 minutes depending on your internet speed).

When done, you should see text like: `Successfully installed Flask-3.x Pandas-2.x ...`

---

### [ ] Step 8: Load sample data (recommended for first run)

Type this and press Enter:

```
python seed_data.py
```

You should see:
```
[DB] Database initialised successfully.
[Seed] Inserted 80 sample feedback rows.
```

---

## PART 3 — Run the Website

### [ ] Step 9: Start the server

Type this and press Enter:

```
python app.py
```

You should see:
```
[DB] Database initialised successfully.
 * Running on http://127.0.0.1:5000
```

⚠️ **Keep this Command Prompt window open.** Do not close it while using the website.

---

### [ ] Step 10: Open the website

1. Open any browser (Chrome, Edge, Firefox)
2. In the address bar, type:
   ```
   http://127.0.0.1:5000
   ```
3. Press Enter

🎉 **The website should open!**

---

## PART 4 — Using the Website

| Page | What to do |
|---|---|
| **Submit Feedback** (homepage) | Select course → select question → pick rating 1–5 → click Submit |
| **Dashboard** | View charts and average ratings (needs at least 5 responses per course) |
| **Reports** | View full aggregated report table |
| **Export CSV** | Click to download the report as an Excel-compatible file |

---

## Stopping the Website

When you're done, click on the Command Prompt window and press:

```
Ctrl + C
```

The server stops. The website will be offline until you run `python app.py` again.

---

## Starting Again Later

Next time, just:

1. Open Command Prompt inside the `StudentFeedbackSystem` folder (repeat Step 6)
2. Run `python app.py`
3. Go to `http://127.0.0.1:5000`

You do **not** need to install packages again.
You do **not** need to run `seed_data.py` again.

---

## Something Not Working?

See **README.md → Common Errors and Fixes** for solutions to the most common problems.

---

*This guide is written for Windows users with no technical background.*
*All steps are safe — nothing here modifies your system settings.*
