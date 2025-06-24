# database.py

import sqlite3
import os

DB_NAME = "keep_it_up.db"

# --- Helper to connect to the DB ---
def get_connection():
    return sqlite3.connect(DB_NAME)

# --- Initialize database (create tables if not exist) ---
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT
            )
        ''')
        conn.commit()

# --- Check if email already exists ---
def email_exists(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        return cursor.fetchone() is not None

# --- Create a new user ---
def create_user(email, password, name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", (email, password, name))
        conn.commit()


# --- Validate user credentials ---
def validate_login(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        return cursor.fetchone()
