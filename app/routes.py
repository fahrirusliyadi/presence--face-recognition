from app import app

# Define your routes
@app.route('/')
def index():
    return "Face Recognition API"