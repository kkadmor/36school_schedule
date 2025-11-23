import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Teachers (
                name TEXT PRIMARY KEY,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()
    finally:
        conn.close()

def get_email_by_name(name: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM Teachers WHERE name = ?', (name,))
        result = cursor.fetchone()
        return result['email'] if result else None
    finally:
        conn.close()

def add_teacher(name: str, email: str):
    conn = get_db_connection()
    try:
        conn.execute('INSERT OR REPLACE INTO Teachers (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
    finally:
        conn.close()

def delete_teacher_by_name(name: str):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM Teachers WHERE name = ?', (name,))
        conn.commit()
    finally:
        conn.close()

def get_all_teachers():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name, email FROM Teachers ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

init_db()