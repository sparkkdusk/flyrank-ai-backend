import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


def create_table():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

    connection.commit()
    connection.close()


def seed_tasks():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) AS count FROM tasks"
        )

        result = cursor.fetchone()

        if result["count"] == 0:
            cursor.executemany(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                """,
                [
                    ("Learn FastAPI", False),
                    ("Build CRUD API", False),
                    ("Upload to GitHub", True)
                ]
            )

    connection.commit()
    connection.close()


def initialize_database():
    create_table()
    seed_tasks()