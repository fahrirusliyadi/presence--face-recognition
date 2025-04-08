from app import app
from flask import jsonify, request
from recognition.utils import get_face_encoding, predict_face, save_face_data


@app.route("/recognize/<id>", methods=["POST"])
def recognize(id):
    if 'image' not in request.files:
        return "Image URL is required", 400
    
    image = request.files['image']
    encoding = get_face_encoding(image)
    
    if encoding is None:
        return "No face found in the image", 400
    
    save_face_data(id, encoding)

    return f"User {id} updated successfully!"

@app.route("/predict", methods=["POST"])
def predict():
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
    