# database.py
import sqlite3

DB_NAME = "keep_it_up.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT
            )
        ''')
        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                due_date TEXT,
                time TEXT,
                notify_days INTEGER,
                notify_hours INTEGER,
                completed INTEGER DEFAULT 0,
                subtasks TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # ✅ Add this for subtasks support:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subtasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                subtask TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

def email_exists(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        return cursor.fetchone() is not None

def create_user(email, password, name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", (email, password, name))
        conn.commit()

def validate_login(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user and user[3] == password:
            return {"id": user[0], "name": user[1], "email": user[2]}
        return None

def add_task(user_id, task):
    subtasks_str = "\n".join(task["subtasks"])
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (
                user_id, name, description, category, due_date, time,
                subtasks, notify_days, notify_hours, completed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            task["name"],
            task["description"],
            task["category"],
            task["due_date"],
            task["time"],
            subtasks_str,
            task["notify_days"],
            task["notify_hours"],
            int(task["completed"])
        ))
        conn.commit()

def delete_task(task_id):
    """Deletes a task and all its subtasks by task_id."""
    conn = sqlite3.connect("keep_it_up.db")
    c = conn.cursor()
    c.execute("DELETE FROM subtasks WHERE task_id = ?", (task_id,))
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_all_tasks(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            subtasks = row[7].split("\n") if row[7] else []
            tasks.append({
                "id": row[0],
                "user_id": row[1],
                "name": row[2],
                "description": row[3],
                "category": row[4],
                "due_date": row[5],
                "time": row[6],
                "subtasks": subtasks,
                "notify_days": row[8],
                "notify_hours": row[9],
                "completed": bool(row[10])
            })
        return tasks

def update_task_completion(task_id, completed):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))
        conn.commit()
def update_task(task_id, updated_task):
    import sqlite3
    conn = sqlite3.connect("keep_it_up.db")
    c = conn.cursor()

    # Update main task fields
    c.execute("""
        UPDATE tasks SET
            name = ?,
            description = ?,
            category = ?,
            due_date = ?,
            time = ?,
            completed = ?
        WHERE id = ?
    """, (
        updated_task["name"],
        updated_task["description"],
        updated_task["category"],
        updated_task["due_date"],
        updated_task["time"],
        int(updated_task.get("completed", False)),
        task_id
    ))

    # Clear and re-insert subtasks
    c.execute("DELETE FROM subtasks WHERE task_id = ?", (task_id,))
    for subtask in updated_task.get("subtasks", []):
        c.execute("INSERT INTO subtasks (task_id, subtask) VALUES (?, ?)", (task_id, subtask))

    conn.commit()
    conn.close()
