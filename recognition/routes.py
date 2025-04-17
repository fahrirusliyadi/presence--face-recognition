from app import app
from flask import jsonify, request
from recognition.utils import delete_face_data, get_face_encoding, predict_face, save_face_data


@app.route("/update", methods=["POST"])
def update():
    if 'image' not in request.files:
        return jsonify({"message": "Image URL is required"}), 400
    
    if 'user_id' not in request.form:
        return jsonify({"message": "User ID is required"}), 400

    user_id = int(request.form.get('user_id'))
    image = request.files['image']
    encoding = get_face_encoding(image)
    
    if encoding is None:
        return jsonify({"message": "No face found in the image"}), 400
    
    save_face_data(user_id, encoding)

    return jsonify({"message": f"User {user_id} updated successfully!"}), 200

@app.route("/recognize", methods=["POST"])
def recognize():
    if 'image' not in request.files:
        return jsonify({"message": "Image URL is required"}), 400
    
    image = request.files['image']
    encoding = get_face_encoding(image)
    
    if encoding is None:
        return jsonify({"message": "No face found in the image"}), 400
    
    prediction = predict_face(encoding)
    
    if prediction is None:
        return jsonify({"message": "No matching face found"}), 400
    else:
        return jsonify({"data": int(prediction)}), 200
    
@app.route("/delete", methods=["DELETE"])
def delete():
    # Get JSON data from request
    data = request.get_json()
    
    # Check if the JSON data exists and has user_id
    if not data or 'user_id' not in data:
        return jsonify({ "message": "User ID is required in JSON body" }), 400

    user_id = int(data['user_id'])

    if delete_face_data(user_id):
        return jsonify({"message": f"User {user_id} deleted successfully!"}), 200
    
    return jsonify({"message": f"User {user_id} not found"}), 404