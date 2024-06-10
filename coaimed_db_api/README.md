# COAIMED_DB

This project is a Flask application named `coaimed_db`, providing an API to manage a PostgreSQL database. 
It includes models for activities, exercises, sensors, and users.

## Prerequisites

1. Python 3.8
2. `pip`

## Setup Instructions

### Step 1: Set Up the Flask Application

### Clone the repository:

```sh
git clone https://github.com/yourusername/your-repo.git
cd your-repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql://myuser:mypassword@localhost/mydatabase'
```

### Step 2: Run the Flask Application
```sh
source venv/bin/activate
export DATABASE_URL='postgresql://myuser:mypassword@localhost/mydatabase'
export FLASK_APP=coaimed_db
flask run --host=0.0.0.0 --port=5000
```

# API Endpoints

This document outlines the endpoints available in the API.

## Users

- **GET /users**: Retrieve a list of all users.
- **GET /users/<id>**: Retrieve a specific user by ID.
- **POST /users**: Create a new user.
- **PUT /users/<id>**: Update a specific user by ID.
- **DELETE /users/<id>**: Delete a specific user by ID.

## Exercises

- **GET /exercises**: Retrieve a list of all exercises.
- **GET /exercises/<id>**: Retrieve a specific exercise by ID.
- **POST /exercises**: Create a new exercise.
- **PUT /exercises/<id>**: Update a specific exercise by ID.
- **DELETE /exercises/<id>**: Delete a specific exercise by ID.

## Sensors

- **GET /sensors**: Retrieve a list of all sensors.
- **GET /sensors/<id>**: Retrieve a specific sensor by ID.
- **POST /sensors**: Create a new sensor.
- **PUT /sensors/<id>**: Update a specific sensor by ID.
- **DELETE /sensors/<id>**: Delete a specific sensor by ID.

## Activities

- **GET /activities**: Retrieve a list of all activities.
- **GET /activities/<id>**: Retrieve a specific activity by ID.
- **POST /activities**: Create a new activity.
- **PUT /activities/<id>**: Update a specific activity by ID.
- **DELETE /activities/<id>**: Delete a specific activity by ID.

Each endpoint supports the specified HTTP methods for performing CRUD (Create, Read, Update, Delete) operations on the corresponding resource.

