import sqlite3
import os
import datetime

DB_FILE = "kali_data.db"

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sessions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    ''')
    
    # Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        )
    ''')
    
    # Artifacts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            file_path TEXT NOT NULL,
            artifact_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        )
    ''')
    
    # Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    # Insert default settings if they don't exist
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('llm_model', 'llama3.2')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('temperature', '0.2')")
    
    # Insert default project and session if none exist
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO projects (name) VALUES ('Default Project')")
        project_id = cursor.lastrowid
        cursor.execute("INSERT INTO sessions (project_id, name) VALUES (?, 'General Chat')", (project_id,))
        
    conn.commit()
    conn.close()

# --- Projects ---
def get_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM projects ORDER BY created_at DESC")
    projects = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    conn.close()
    return projects

def create_project(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (name) VALUES (?)", (name,))
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return project_id

# --- Sessions ---
def get_sessions(project_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if project_id:
        cursor.execute("SELECT id, project_id, name FROM sessions WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
    else:
        cursor.execute("SELECT id, project_id, name FROM sessions ORDER BY created_at DESC")
    sessions = [{"id": row[0], "project_id": row[1], "name": row[2]} for row in cursor.fetchall()]
    conn.close()
    return sessions

def create_session(project_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (project_id, name) VALUES (?, ?)", (project_id, name))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

# --- Messages ---
def get_messages(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
    messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()
    return messages

def add_message(session_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
    conn.commit()
    conn.close()

# --- Artifacts ---
def get_artifacts(session_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if session_id:
        cursor.execute("SELECT id, session_id, file_path, artifact_type FROM artifacts WHERE session_id = ? ORDER BY created_at DESC", (session_id,))
    else:
        cursor.execute("SELECT id, session_id, file_path, artifact_type FROM artifacts ORDER BY created_at DESC")
    artifacts = [{"id": row[0], "session_id": row[1], "file_path": row[2], "type": row[3]} for row in cursor.fetchall()]
    conn.close()
    return artifacts

def add_artifact(session_id, file_path, artifact_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artifacts (session_id, file_path, artifact_type) VALUES (?, ?, ?)", (session_id, file_path, artifact_type))
    conn.commit()
    conn.close()

# --- Settings ---
def get_settings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM settings")
    settings = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return settings

def update_setting(key, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
