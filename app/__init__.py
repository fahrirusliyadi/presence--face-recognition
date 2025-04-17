from flask import Flask, jsonify
from app.errors import AppError

app = Flask(__name__)

# Register error handlers
@app.errorhandler(AppError)
def handle_app_error(error):
    error_type = type(error).__name__
    return jsonify({
        "message": error.message,
        "type": error_type
    }), error.status_code

# Import routes
from app import routes
from recognition import routes
