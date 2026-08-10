import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def seed_tasks():
    connection = get_connection()

    result = connection.execute(
        "SELECT COUNT(*) AS count FROM tasks"
    ).fetchone()

    if result["count"] == 0:
        connection.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Upload to GitHub", 1)
            ]
        )

        connection.commit()

    connection.close()


def initialize_database():
    create_table()
    seed_tasks()