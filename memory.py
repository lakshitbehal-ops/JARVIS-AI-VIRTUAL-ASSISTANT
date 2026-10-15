import sqlite3
from datetime import datetime

DB_NAME = "jarvis_memory.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_memory(memory):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memories (memory, created_at) VALUES (?, ?)",
        (memory, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def get_memories():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT memory FROM memories ORDER BY id DESC LIMIT 10"
    )

    memories = [row[0] for row in cursor.fetchall()]

    conn.close()

    return memories