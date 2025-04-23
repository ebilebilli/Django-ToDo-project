# Django To-Do REST API

This is a Django-based RESTful To-Do application that allows users to create, manage, and organize their tasks through a modern API. Users can register, log in, create notes, assign labels, pin important notes, mark tasks as completed, and manage deleted items in a trash bin. The application uses Django REST Framework (DRF) and JWT for secure authentication.

## Features

- **User Authentication**:
  - Register new users with username, email, and password.
  - Log in to receive JWT access and refresh tokens.
  - Log out to invalidate tokens (client-side token removal).
- **Note Management**:
  - Create, update, and delete notes with content and optional labels.
  - Pin up to 10 important notes for quick access.
  - Mark notes as completed or incomplete.
  - Filter notes by labels.
- **Label Management**:
  - Create, update, and delete labels for organizing notes.
- **Trash Bin**:
  - Move notes and labels to a trash bin for temporary storage.
  - Restore notes or labels from the trash bin.
  - The periodic task for cleaning up trash (notes and labels older than 30 days) is defined in the Celery Beat schedule.

- **RESTful API**:
  - Comprehensive API endpoints for all functionalities.
  - Pagination for note and label lists.
  - Secure access with JWT authentication and custom permissions (`HeHasPermission`).
**API Documentation**:
  - Interactive Swagger (OpenAPI) documentation for exploring and testing API endpoints.
- **Modern Architecture**:
  - Uses Django REST Framework and Simple JWT for authentication.
  - Modular code structure with serializers, custom permissions, and pagination.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Authentication**: Simple JWT (JSON Web Tokens)
- **Database**: SQLite (default, can be configured for PostgreSQL or others)
- **Python Libraries**: `djangorestframework`, `djangorestframework-simplejwt`, `python-dotenv`, `celery`, `redis`, `django-celery-beat`
- **Task Queue**: Celery (for asynchronous task processing)
- **Message Broker**: Redis (in-memory data store for Celery)
- **Scheduler**: Celery Beat (for periodic tasks)
- **Containerization**: Docker and Docker Compose (for simplified deployment and development)



## Task Scheduling and Asynchronous Processing

To handle periodic tasks, the project integrates **Celery** with **Redis** as the message broker and **Celery Beat** for scheduling. This setup is used to automatically delete notes and labels in the trash that are older than 30 days. While the project is lightweight and does not heavily rely on asynchronous processing, Celery ensures efficient handling of scheduled cleanup tasks.

### Technologies Added
- **Celery**: Distributed task queue for asynchronous task processing.
- **Redis**: In-memory data store used as the message broker for Celery.
- **Celery Beat**: Scheduler for running periodic tasks.

## Setup Instructions

### Prerequisites
- **Docker**: Install Docker and Docker Compose to run the application in containers.
- **Python**: If running locally without Docker, Python 3.8+ is required.
- **Redis**: Required for Celery (included in Docker setup).


# Installation
git clone https://github.com/ebilebilli/django-todo-api.git
cd django-todo-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Optional
python manage.py runserver

# API will be available at http://localhost:8000

# Usage Examples (using curl):

# User Registration
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "strongpassword123"}'

# User Login
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "strongpassword123"}'

# Create Note (replace <access_token> with actual token)
curl -X POST http://localhost:8000/api/notes/create/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"context": "Buy groceries", "label": 1}'

# Pin Note
curl -X PATCH http://localhost:8000/api/notes/1/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"is_pinned": true}'

# Move Note to Trash
curl -X POST http://localhost:8000/api/notes/1/trash/ \
-H "Authorization: Bearer <access_token>"

# Create Label
curl -X POST http://localhost:8000/api/labels/create/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"title": "Work"}'

# View Trashed Notes
curl -X GET http://localhost:8000/api/trash/notes/ \
-H "Authorization: Bearer <access_token>"

# Restore Note
curl -X POST http://localhost:8000/api/trash/notes/1/ \
-H "Authorization: Bearer <access_token>"
## Available Endpoints

All API endpoints are prefixed with `/api/v1/`. Account-related endpoints are under `/api/v1/accounts/`, while note and label-related endpoints are under `/api/v1/app/`. Below is a list of available endpoints:

- `/api/v1/accounts/register/`             POST    Register new user
- `/api/v1/accounts/token/`               POST    Obtain JWT tokens
- `/api/v1/accounts/token/refresh/`       POST    Refresh access token
- `/api/v1/accounts/logout/`              POST    Log out
- `/api/v1/app/notes/`                    GET     List all notes
- `/api/v1/app/notes/<int:note_id>/`      GET,PATCH Get or update note details
- `/api/v1/app/notes/<int:note_id>/`      PATCH   Change pin status
- `/api/v1/app/notes/create/`             POST    Create new note
- `/api/v1/app/notes/<int:note_id>/trash/` POST   Move note to trash
- `/api/v1/app/labels/<int:label_id>/notes/` GET  Get notes by label
- `/api/v1/app/labels/`                   GET     List all labels
- `/api/v1/app/labels/<int:label_id>/`    GET,PATCH Get or update label
- `/api/v1/app/labels/create/`            POST    Create new label
- `/api/v1/app/labels/<int:label_id>/trash/` POST Move label to trash
- `/api/v1/app/trash/notes/`              GET     List trashed notes
- `/api/v1/app/trash/notes/<int:note_id>/` GET,POST Get or restore trashed note
- `/api/v1/app/trash/labels/`             GET     List trashed labels
- `/api/v1/app/trash/labels/<int:label_id>/` GET,POST Get or restore trashed label
- `/swagger/`                             GET     Interactive Swagger API documentation

# Contributing:
# 1. Fork the repository
# 2. Create new branch (git checkout -b feature/YourFeatureName)
# 3. Commit changes (git commit -m 'Add some feature')
# 4. Push to branch (git push origin feature/YourFeatureName)
# 5. Open pull request

# License: MIT
# Contact: ebilebilli3@gmail.com | GitHub: ebilebilli