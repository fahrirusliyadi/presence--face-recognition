from app import app
from flask import request
from recognition.utils import get_face_encoding, save_face_data


@app.route("/recognize/<id>", methods=["POST"])
def update_user(id):
    if 'image' not in request.files:
        return "Image URL is required", 400
    
    image = request.files['image']
    encoding = get_face_encoding(image)
    
    if encoding is None:
        return "No face found in the image", 400
    
    save_face_data(id, encoding)

    return f"User {id} updated successfully!"
