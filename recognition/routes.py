from app import app
from flask import jsonify, request
from recognition.utils import delete_face_data, get_face_encoding, predict_face, save_face_data


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
    
@app.route("/delete", methods=["DELETE"])
def delete():
    # Get JSON data from request
    data = request.get_json()
    
    # Check if the JSON data exists and has user_id
    if not data or 'user_id' not in data:
        return jsonify({ "error": "User ID is required in JSON body" }), 400

    user_id = data['user_id']
    delete_face_data(user_id)

    return jsonify({"message": f"User {user_id} deleted successfully!"}), 200