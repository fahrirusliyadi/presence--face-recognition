"""
Face Recognition API Server

A Flask-based REST API for face recognition and user management.
This server provides endpoints to register, recognize, and delete user faces.

To run the application:
    python app.py

The server will start in debug mode on http://127.0.0.1:5000/
"""
from app import app

if __name__ == "__main__":
    app.run(debug=True)