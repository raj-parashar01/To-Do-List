# To-Do-List
# 📝 To-Do List Application

A simple and lightweight To-Do List web application built using Python, SQLite, HTML, and CSS. It allows users to create, manage, and track daily tasks seamlessly.

---

## 🚀 Features

- **Add Tasks:** Quickly add new tasks to your list.
- **Task Persistence:** Stores tasks in a local SQLite database (`tasks.db`) and text backup (`tasks.txt`).
- **Clean UI:** Responsive and minimalist interface styled with custom CSS.
- **Task Management:** Mark tasks as completed or remove them once finished.

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite (`tasks.db`)
- **Frontend:** HTML5, CSS3 (`templates/index.html`, `static/style.css`)

---

## 📂 Project Structure

```text
To-Do List/
│
├── static/
│   └── style.css          # Custom styling
├── templates/
│   └── index.html         # Webpage layout
├── app.py                 # Main application logic
├── main.py                # Entry point / alternate runner
├── tasks.db               # SQLite database file
└── tasks.txt              # Task log / text backup
