"""
App initialization module

This module initializes the Flask application, sets up error handlers,
and imports routes from different modules.

The application uses a modular structure with:
- app: Core application functionality and routes
- recognition: Face recognition logic and routes
"""
from flask import Flask, jsonify
from app.errors import AppError

app = Flask(__name__)

# Register error handlers
@app.errorhandler(AppError)
def handle_app_error(error):
    """
    Global error handler for application errors
    
    This handler catches all exceptions that inherit from AppError
    and returns a consistent JSON response format.
    
    Args:
        error (AppError): The error that was raised
        
    Returns:
        tuple: JSON response with error details and appropriate status code
    """
    error_type = type(error).__name__
    return jsonify({
        "message": error.message,
        "type": error_type
    }), error.status_code

# Import routes
from app import routes
from recognition import routes
