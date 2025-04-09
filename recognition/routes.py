from app import app
from flask import jsonify, request
from recognition.utils import get_face_encoding, predict_face, save_face_data


@app.route("/update", methods=["POST"])
def update():
    if 'image' not in request.files:
        return "Image URL is required", 400
    
    if 'user_id' not in request.form:
        return "User ID is required", 400

    user_id = request.form.get('user_id')
    image = request.files['image']
    encoding = get_face_encoding(image)
    
    if encoding is None:
        return "No face found in the image", 400
    
    save_face_data(user_id, encoding)

    return f"User {user_id} updated successfully!"

@app.route("/recognize", methods=["POST"])
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "Image URL is required"}), 400
    
    image = request.files['image']
    encoding = get_face_encoding(image)
    
    if encoding is None:
        return jsonify({"error": "No face found in the image"}), 400
    
    prediction = predict_face(encoding)
    
    if prediction is None:
        return jsonify({"error": "No matching face found"}), 400
    else:
        return jsonify({"data": prediction}), 200
    