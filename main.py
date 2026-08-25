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
    done: bool = False


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


# GET all tasks
@app.get(
    "/tasks",
    description="Get all tasks"
)
def get_tasks():

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tasks"
        )

        rows = cursor.fetchall()

    connection.close()

    return rows


# GET one task
@app.get(
    "/tasks/{task_id}",
    description="Get a single task by ID"
)
def get_task(task_id: int):

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tasks WHERE id = %s",
            (task_id,)
        )

        row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return row


# CREATE task
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

    with connection.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING *
            """,
            (task.title, task.done)
        )

        row = cursor.fetchone()

    connection.commit()
    connection.close()

    return row


# UPDATE task
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

    with connection.cursor() as cursor:

        cursor.execute(
            """
            UPDATE tasks
            SET title = %s,
                done = %s
            WHERE id = %s
            RETURNING *
            """,
            (
                updated_task.title,
                updated_task.done,
                task_id
            )
        )

        row = cursor.fetchone()

    if row is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.commit()
    connection.close()

    return row


# DELETE task
@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    description="Delete a task"
)
def delete_task(task_id: int):

    connection = get_connection()

    with connection.cursor() as cursor:

        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        deleted = cursor.rowcount

    connection.commit()
    connection.close()

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return