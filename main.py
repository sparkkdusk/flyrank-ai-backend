from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import initialize_database

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built with FastAPI for FlyRank Backend AI Engineering Internship",
    version="1.0"
)

initialize_database()

class TaskCreate(BaseModel):
    title: str


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


@app.get(
    "/tasks",
    description="Get all tasks"
)
def get_tasks():
    return tasks


@app.get(
    "/tasks/{task_id}",
    description="Get a single task by ID"
)
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )



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

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task





@app.put(
    "/tasks/{task_id}",
    description="Update an existing task"
)
def update_task(task_id: int, updated_task: TaskCreate):

    for task in tasks:
        if task["id"] == task_id:

            task["title"] = updated_task.title

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    description="Delete a task"
)
def delete_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )