🛠️ TaskLY API - Django REST Server

This is the TaskLY API, a RESTful backend server built with Django and Django REST Framework. It serves as the backend for the TaskLY task management application, handling tasks and user data through a clean and robust API.
🚀 Features

    CRUD Operations: Create, Read, Update, and Delete tasks.
    Task Management: Organize tasks by status (Pending, In Progress, Completed).
    RESTful API: Standardized endpoints for seamless integration.
    Authentication: Token-based authentication for secure API access.
    Database: Data persistence using PostgreSQL or SQLite.

📦 Installation and Setup

Follow these steps to set up and run the Django REST API server:
1. Clone the repository

git clone https://github.com/your-username/taskly-api.git  
cd taskly-api  

2. Create a virtual environment

It’s recommended to use a virtual environment to isolate dependencies.

python -m venv venv  
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows  

3. Install dependencies

Install all required packages from the requirements.txt file.

pip install -r requirements.txt  

4. Configure the database

By default, the API uses SQLite. To switch to PostgreSQL:

    Update the DATABASES section in settings.py.
    Install the PostgreSQL adapter:

    pip install psycopg2-binary  

5. Run migrations

Apply the database migrations.

python manage.py migrate  

6. Start the server

Run the development server:

python manage.py runserver  

The API will be available at:
http://127.0.0.1:8000/
