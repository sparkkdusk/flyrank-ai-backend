from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection, initialize_database

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built with FastAPI for FlyRank Backend AI Engineering Internship",
    version="1.0"
)

initialize_database()


class TaskCreate(BaseModel):
    title: str


# Temporary in-memory storage for POST, PUT, DELETE.
# These will be replaced with SQLite in Stages 2 and 3.
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Upload to GitHub",
        "done": True
    }
]


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Stage 1: Read all tasks from SQLite
@app.get(
    "/tasks",
    description="Get all tasks"
)
def get_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]


# Stage 1: Read one task from SQLite
@app.get(
    "/tasks/{task_id}",
    description="Get a single task by ID"
)
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.post(
    "/tasks",
    status_code=201,
    description="Create a new task"
)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (task.title, 0)
    )

    connection.commit()

    new_task_id = cursor.lastrowid

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (new_task_id,)
    ).fetchone()

    connection.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.put(
    "/tasks/{task_id}",
    description="Update an existing task"
)
def update_task(task_id: int, updated_task: TaskCreate):

    if not updated_task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE tasks
        SET title = ?
        WHERE id = ?
        """,
        (updated_task.title, task_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    description="Delete a task"
)
def delete_task(task_id: int):

    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()

    connection.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return
