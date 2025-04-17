from app import app
from flask import jsonify

# Define your routes
@app.route('/')
def index():
    return jsonify({"message": "Face Recognition API"})