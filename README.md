# FlyRank Internship — Backend AI Track

## Week 3 · Assignment A2 — Connecting CRUD to SQLite

A continuation of **Week 2 / Assignment A1**, migrating the CRUD API from in-memory storage to a persistent **SQLite database**.

### Tech Stack

* Python
* FastAPI
* SQLite (`sqlite3`)
* Uvicorn

### What Changed

**A1:**

```text
Client → FastAPI → In-memory list
```

**A2:**

```text
Client → FastAPI → SQLite (tasks.db)
```

The API endpoints remain the same, but data now survives server restarts.

### Database

The application automatically creates `tasks.db` and the `tasks` table if they don't exist.

The table contains:

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
title TEXT NOT NULL
done INTEGER NOT NULL DEFAULT 0
```

Three sample tasks are seeded only when the table is empty.

### API Endpoints

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| GET    | `/tasks`      | Get all tasks |
| GET    | `/tasks/{id}` | Get a task    |
| POST   | `/tasks`      | Create a task |
| PUT    | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

### Run Locally

```bash
git clone https://github.com/sparkkdusk/flyrank-week3-a2-crud-sqlite.git
cd flyrank-week3-a2-crud-sqlite

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### Key Concepts Practiced

* SQLite database & tables
* SQL CRUD operations
* Parameterized queries
* Data persistence
* Database seeding
* DB Browser for SQLite
* Git & GitHub


**FlyRank Internship · Backend Track · Week 3 · Assignment A2**
