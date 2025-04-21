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
  - Planned automatic cleanup for items in the trash bin after 30 days (using Celery Beat, under development).
- **RESTful API**:
  - Comprehensive API endpoints for all functionalities.
  - Pagination for note and label lists.
  - Secure access with JWT authentication and custom permissions (`HeHasPermission`).
- **Modern Architecture**:
  - Uses Django REST Framework and Simple JWT for authentication.
  - Modular code structure with serializers, custom permissions, and pagination.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Authentication**: Simple JWT (JSON Web Tokens)
- **Database**: SQLite (default, can be configured for PostgreSQL or others)
- **Python Libraries**: `djangorestframework`, `djangorestframework-simplejwt`

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

# Available Endpoints:
# /api/register/                  POST    Register new user
# /api/token/                     POST    Obtain JWT tokens
# /api/token/refresh/             POST    Refresh access token
# /api/logout/                    POST    Log out
# /api/notes/                     GET     List all notes
# /api/notes/<note_id>/           GET,PATCH Get/update note
# /api/notes/create/              POST    Create new note
# /api/notes/<note_id>/trash/     POST    Move note to trash
# /api/labels/<label_id>/notes/   GET     Get notes by label
# /api/labels/                    GET     List all labels
# /api/labels/<label_id>/         GET,PATCH Get/update label
# /api/labels/create/             POST    Create new label
# /api/labels/<label_id>/trash/   POST    Move label to trash
# /api/trash/notes/               GET     List trashed notes
# /api/trash/notes/<note_id>/     GET,POST Get/restore trashed note
# /api/trash/labels/              GET     List trashed labels
# /api/trash/labels/<label_id>/   GET,POST Get/restore trashed label

# Contributing:
# 1. Fork the repository
# 2. Create new branch (git checkout -b feature/YourFeatureName)
# 3. Commit changes (git commit -m 'Add some feature')
# 4. Push to branch (git push origin feature/YourFeatureName)
# 5. Open pull request

# License: MIT
# Contact: ebilebilli3@gmail.com | GitHub: ebilebilli