# Social Media API Endpoints with FastAPI

This project demonstrates the creation of social media API endpoints using FastAPI. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Features

- User authentication and authorization
- Create, read, update, and delete (CRUD) operations for posts
- Commenting on posts
- Like and unlike functionality for posts
- Following and unfollowing users

## Requirements

- Python 3.6+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn (for running the server)
- Alembic (for database migrations)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/anjali200403/social-media-api.git
    cd social-media-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    alembic upgrade head
    ```

## Running the Application

To run the application, use Uvicorn:

```bash
uvicorn main:app --reload
