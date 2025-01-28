# FastAPI Project with SQLite, SQLAlchemy, and Pydantic

This project is a simple FastAPI application that uses SQLite as the database, SQLAlchemy for ORM, and Pydantic for data validation.

## Project Structure

- `app.py`: Main application file containing the FastAPI setup, database models, and CRUD operations.
- `alembic/env.py`: Alembic configuration for database migrations.
- `.devcontainer/devcontainer.json`: Dev container configuration for VS Code.

## Setup Instructions

### Prerequisites

- Python 3.12 or later
- Docker (for development container)

### Development Environment

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd python-3
    ```

2. **Open in VS Code with Dev Containers:**
    - Open the project folder in VS Code.
    - Use the `Remote - Containers` extension to open the folder in a dev container.

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    uvicorn app:app --reload
    ```

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

## Usage

### API Endpoints

- **Create User:**
    ```sh
    POST /api/users/
    {
        "email": "user@example.com",
        "full_name": "John Doe",
        "password": "password123"
    }
    ```

- **Get User:**
    ```sh
    GET /api/users/{user_id}
    ```

### Example Requests

- **Create User:**
    ```sh
    curl -X POST "http://localhost:8000/api/users/" -H "Content-Type: application/json" -d '{"email":"user@example.com","full_name":"John Doe","password":"password123"}'
    ```

- **Get User:**
    ```sh
    curl -X GET "http://localhost:8000/api/users/1"
    ```

## License

This project is licensed under the MIT License.