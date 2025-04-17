from app import app
from flask import jsonify, request
from recognition.utils import delete_face_data, get_face_encoding, predict_face, save_face_data
from app.errors import MissingParameterError, ValidationError, ResourceNotFoundError


@app.route("/update", methods=["POST"])
def update():
    if 'image' not in request.files:
        raise MissingParameterError("Image URL")
    
    if 'user_id' not in request.form:
        raise MissingParameterError("User ID")

    user_id = int(request.form.get('user_id'))
    image = request.files['image']
    
    encoding = get_face_encoding(image)
    save_face_data(user_id, encoding)
    return jsonify({"message": f"User {user_id} updated successfully!"}), 200

@app.route("/recognize", methods=["POST"])
def recognize():
    if 'image' not in request.files:
        raise MissingParameterError("Image URL")
    
    image = request.files['image']
    
    encoding = get_face_encoding(image)
    prediction = predict_face(encoding)
    
    if prediction is None:
        raise ValidationError("No matching face found")
    
    return jsonify({"data": int(prediction)}), 200
    
@app.route("/delete", methods=["DELETE"])
def delete():
    # Get JSON data from request
    data = request.get_json()
    
    # Check if the JSON data exists and has user_id
    if not data or 'user_id' not in data:
        raise MissingParameterError("User ID in JSON body")

    user_id = int(data['user_id'])

    if delete_face_data(user_id):
        return jsonify({"message": f"User {user_id} deleted successfully!"}), 200
    
    raise ResourceNotFoundError(f"User {user_id} not found")