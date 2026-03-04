# FastAPI Scalable Starter

Production-ready baseline for a user API with:
- Layered architecture (`routers` -> `services` -> `models`)
- Centralized settings via environment variables
- SQLite default with configurable `DATABASE_URL`
- Secure password hashing (PBKDF2)
- CRUD APIs with validation and pagination

## Project Structure

- `fontend/main.py` - app bootstrap, routers, handlers
- `fontend/core/config.py` - app/database settings
- `fontend/core/security.py` - password hashing helpers
- `fontend/database.py` - SQLAlchemy engine/session/base
- `fontend/models/` - ORM models
- `fontend/schemas/` - request/response contracts
- `fontend/services/` - business logic layer
- `fontend/routers/` - API endpoints

## Run Locally

1. Activate environment:
	- `source testenv/bin/activate`
2. Install dependencies:
	- `pip install -r requirements.txt`
3. Start API:
	- `uvicorn fontend.main:app --reload`
4. Open docs:
	- `http://127.0.0.1:8000/docs`

## Environment Variables

- `APP_NAME` (default: `FastTime API`)
- `APP_VERSION` (default: `1.0.0`)
- `DEBUG` (`true` or `false`, default: `false`)
- `DATABASE_URL` (optional, defaults to local SQLite file `test.db`)

Example:

```bash
export APP_NAME="FastTime API"
export APP_VERSION="1.0.0"
export DEBUG="true"
export DATABASE_URL="sqlite:////absolute/path/to/test.db"
```

## PostgreSQL Setup

Use PostgreSQL by setting `DATABASE_URL`:

```bash
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_db"
```

Also supported and auto-converted by the app:
- `postgres://...`
- `postgresql://...`

You can copy `.env.example` values into your shell before starting the server.

## Run with Docker Compose (API + PostgreSQL)

Start everything:

```bash
docker compose up --build
```

API docs:
- `http://127.0.0.1:8000/docs`

Stop everything:

```bash
docker compose down
```

Stop and remove DB volume (fresh database):

```bash
docker compose down -v
```

## Endpoints

- `GET /health`
- `GET /users?skip=0&limit=20`
- `GET /users/{user_id}`
- `POST /users`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`
