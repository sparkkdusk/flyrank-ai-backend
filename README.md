# FlyRank Internship — Backend AI Track

## Week 1 · Assignment A3 — Containerize Your Stack

A task CRUD API built with **Python, FastAPI, and PostgreSQL**, with the complete application and database running in Docker using Docker Compose.

This assignment continues the storage evolution:

```text
A1 → In-memory storage
A2 → SQLite
A3 → PostgreSQL in Docker
```

The API endpoints remain the same while the storage layer changes.

---

## Tech Stack

* Python 3.10+
* FastAPI
* PostgreSQL
* psycopg
* Docker
* Docker Compose
* Uvicorn
* python-dotenv

---

## Architecture

```text
Client
   │
   ▼
FastAPI API Container
   │
   │ DATABASE_URL
   ▼
PostgreSQL Container
   │
   ▼
postgres_data volume
```

Inside the Docker Compose network, the API connects to PostgreSQL using:

```text
db:5432
```

The PostgreSQL data is stored in a Docker volume so that tasks survive container restarts.

---

## Database

The application automatically creates the `tasks` table if it does not already exist.

### `tasks` table

| Column  | Type               | Description       |
| ------- | ------------------ | ----------------- |
| `id`    | SERIAL PRIMARY KEY | Unique task ID    |
| `title` | TEXT               | Task title        |
| `done`  | BOOLEAN            | Completion status |

Three example tasks are inserted only when the table is empty.

Example:

```text
1  Learn FastAPI       false
2  Build CRUD API      false
3  Upload to GitHub    true
```

---

## Environment Variables

The database connection is configured through `.env`.

Create a local `.env` file:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

The `.env` file is ignored by Git and must **never** be committed.

A `.env.example` file is included in the repository:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tasks
```

When Docker Compose runs the application, it uses the PostgreSQL service name:

```text
postgresql://postgres:dev@db:5432/tasks
```

---

## Running the Application

### Prerequisites

Install:

* Docker Desktop
* Git

No local PostgreSQL installation is required for the Dockerized stack.

### Start the complete application

From the project directory:

```bash
docker compose up --build
```

This starts:

```text
api → FastAPI application
db  → PostgreSQL database
```

The API is available at:

```text
http://127.0.0.1:3000
```

Swagger documentation:

```text
http://127.0.0.1:3000/docs
```

### Run in the background

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

---

## API Endpoints

| Method | Endpoint      | Description   | Success |
| ------ | ------------- | ------------- | ------- |
| GET    | `/tasks`      | Get all tasks | 200     |
| GET    | `/tasks/{id}` | Get one task  | 200     |
| POST   | `/tasks`      | Create a task | 201     |
| PUT    | `/tasks/{id}` | Update a task | 200     |
| DELETE | `/tasks/{id}` | Delete a task | 204     |

Unknown task IDs return:

```text
404 Not Found
```

Invalid or empty task titles return:

```text
400 Bad Request
```

---

## Example API Requests

### Get all tasks

```bash
curl -i http://localhost:3000/tasks
```

Example response:

```text
HTTP/1.1 200 OK

[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Build CRUD API",
    "done": false
  },
  {
    "id": 3,
    "title": "Upload to GitHub",
    "done": true
  }
]
```

### Get one task

```bash
curl -i http://localhost:3000/tasks/1
```

### Create a task

```bash
curl -i -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Dockerize the API\"}"
```

Expected status:

```text
201 Created
```

### Update a task

```bash
curl -i -X PUT http://localhost:3000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn Docker\",\"done\":true}"
```

Expected status:

```text
200 OK
```

### Delete a task

```bash
curl -i -X DELETE http://localhost:3000/tasks/1
```

Expected status:

```text
204 No Content
```

---

## Persistence

PostgreSQL uses a Docker named volume:

```text
postgres_data
```

This means the database data survives container restarts.

For example:

```bash
docker compose down
docker compose up -d
```

Previously created tasks remain in the database.

The volume should **not** be removed when testing persistence.

---

## Database Verification

The PostgreSQL database can be inspected from inside the database container.

Open a PostgreSQL shell:

```bash
docker compose exec db psql -U postgres -d tasks
```

List tables:

```sql
\dt
```

View tasks:

```sql
SELECT * FROM tasks;
```

Example:

```text
 id |       title        | done
----+--------------------+------
  1 | Learn FastAPI      | f
  2 | Build CRUD API     | f
  3 | Upload to GitHub   | t
```

### Database Screenshot

The database screenshot below shows the `tasks` table and its stored rows.
![alt text](image-1.png)

## Parameterized Queries

All database queries use parameterized values rather than directly inserting user input into SQL.

For example:

```python
cursor.execute(
    "SELECT * FROM tasks WHERE id = %s",
    (task_id,)
)
```

This keeps user-provided values separate from the SQL statement and helps prevent SQL injection.

---

## Project Structure

```text
PythonCode/
│
├── main.py
├── database.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env.example
├── .gitignore
├── README.md
└── ...
```

The actual `.env` file is intentionally excluded from Git.

---

## What I Practiced

* Docker images and containers
* PostgreSQL
* Docker Compose
* Docker volumes
* Environment variables and `.env` secrets
* FastAPI
* PostgreSQL CRUD operations
* Parameterized SQL queries
* Database seeding
* Data persistence
* Git and GitHub

---

## Storage Evolution

The same task API has now used three different storage systems:

```text
A1
FastAPI → In-memory list

A2
FastAPI → SQLite

A3
FastAPI → PostgreSQL
          ↑
       Docker
```

The API behaviour stays the same while the storage implementation changes.

This demonstrates that storage can be treated as an implementation detail behind the API.

---

**FlyRank Internship · Backend AI Track · Week 1 · Assignment A3**
