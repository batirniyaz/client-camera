# Client-Camera Application

## Description
Welcome to the Client-Camera application repository. This application is designed to manage and analyze client data captured through cameras. It provides detailed reports and insights on client demographics and behaviors. The application is built with a robust backend using FastAPI and SQLAlchemy, ensuring efficient data handling and processing.

## Features
- **Client Management:** Add, update, and delete client information.
- **Daily Reports:** Generate daily reports on client demographics and behaviors.
- **Attendance Tracking:** Track client attendance and calculate late arrivals and early departures.
- **Responsive Design:** Accessible on various devices.
- **API Endpoints:** Expose RESTful API endpoints for client and report management.
- **Authentication:** Secure user authentication using JWT.
- **Error Handling:** Comprehensive error handling and logging.

## Technologies Used
- **Python:** Core programming language.
- **FastAPI:** Web framework for building APIs.
- **SQLAlchemy:** ORM for database interactions.
- **PostgreSQL:** Database for storing client data.
- **Asyncpg:** PostgreSQL driver for asynchronous operations.
- **Uvicorn:** ASGI server for running FastAPI applications.
- **Pydantic:** Data validation and settings management.
- **Docker:** Containerization for deployment.

## Installation
To run the application locally, follow these steps:

### Prepare the Environment
1. Clone the repository:
    ```bash
    git clone https://github.com/batirniyaz/client-camera.git
    ```
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    - For Linux systems:
      ```bash
      source venv/bin/activate
      ```
    - For Windows:
      ```bash
      venv\Scripts\activate
      ```
4. Go to the root directory:
    ```bash
    cd client-camera
    ```
5. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Run the Application
1. Run the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```
2. Open a web browser and go to:
    ```
    http://localhost:8000
    ```

## Contributors
- **Batirniyaz Muratbaev:** Full Stack Developer

# Thank You for Visiting my GitHub Page!