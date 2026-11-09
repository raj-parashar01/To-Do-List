
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import json

app = Flask(__name__)

DATABASE = "tasks.db"
OLD_FILE = "tasks.txt"


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database and table
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Import old tasks.txt only once
    imported = conn.execute(
        "SELECT value FROM settings WHERE key = ?",
        ("legacy_imported",)
    ).fetchone()

    if imported is None:
        if os.path.exists(OLD_FILE):
            with open(OLD_FILE, "r", encoding="utf-8") as file:
                content = file.read().strip()

            if content:
                try:
                    old_tasks = json.loads(content)
                    if not isinstance(old_tasks, list):
                        old_tasks = content.splitlines()
                except json.JSONDecodeError:
                    old_tasks = content.splitlines()

                for item in old_tasks:
                    if isinstance(item, str):
                        title = item.strip()
                        completed = 0
                    elif isinstance(item, dict):
                        title = str(item.get("title", "")).strip()
                        completed = int(bool(item.get("completed", False)))
                    else:
                        continue

                    if title:
                        conn.execute(
                            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
                            (title, completed)
                        )

        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?)",
            ("legacy_imported", "yes")
        )

    conn.commit()
    conn.close()


# View all tasks
@app.route("/")
def home():
    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# Add task
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("task", "").strip()

    if title:
        conn = get_db_connection()

        conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )

        conn.commit()
        conn.close()

    return redirect(url_for("home"))


# Edit task
@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    title = request.form.get("task", "").strip()

    if title:
        conn = get_db_connection()

        conn.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (title, task_id)
        )

        conn.commit()
        conn.close()

    return redirect(url_for("home"))


# Delete task
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# Mark completed / pending
@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_db_connection()

    conn.execute("""
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
