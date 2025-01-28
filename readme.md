# FastAPI Project with SQLite, SQLAlchemy, and Pydantic

This project is a simple FastAPI application that uses SQLite as the database, SQLAlchemy for ORM, and Pydantic for data validation.


### Database Migrations

1. **Initialize Alembic:**
    ```sh
    alembic init alembic
    ```

2. **Create a new migration:**
    ```sh
    alembic revision --autogenerate -m "Initial migration"
    ```

3. **Apply the migration:**
    ```sh
    alembic upgrade head
    ```
