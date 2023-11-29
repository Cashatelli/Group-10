# Rent-a-Car Web Application
Introduction
This is a simple web application for a car rental service, developed using Flask, a Python web framework. The application allows users to sign in, create an account, browse available cars, and make reservations.

## Installation
Before running the application, ensure that you have Python and pip installed on your machine. Then, install the required dependencies by running the following commands in your terminal:
    pip install Flask Flask-SQLAlchemy Flask-login Flask-mail

## Running the Application
To start the Rent-a-Car web application, follow these steps:
1. Open your terminal.
2. Navigate to the project directory.
3. Run the following command:
    python app.py
    The terminal will display "Running on http://127.0.0.1:5000".
4. Open your web browser and go to http://127.0.0.1:5000, or just hover over http://127.0.0.1.5000 and click the "Follow Link"

## Usage
Upon accessing the application, you can sign in if you have an account or create a new account. After signing in or creating an account, you will be redirected to the dashboard where you can browse available cars and make reservations. The application includes features such as filtering cars by location, make, type, and sorting by price per day. You can view and cancel your current reservations from the dashboard.

## Dependencies
- Flask: Web framework for Python
- Flask-SQLAlchemy: Flask extension for SQLAlchemy, a SQL toolkit and Object-Relational Mapping (ORM) library
- Flask-login: User session management for Flask
- Flask-mail: Flask extension for email handling