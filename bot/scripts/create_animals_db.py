# bot/scripts/create_animals_db.py
"""
Скрипт для создания базы данных животных.

Автор: MADAO81
Версия: 2.0
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "animals.db"


def init_db():
    """Создаёт таблицу животных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            scientific_name TEXT,
            habitat TEXT,
            diet TEXT,
            fun_fact TEXT,
            description TEXT,
            conservation_status TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ База данных животных создана: {DB_PATH}")


if __name__ == "__main__":
    init_db()