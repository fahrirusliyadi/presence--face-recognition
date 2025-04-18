from app import app
from flask import jsonify, request
from recognition.errors import NoFaceError
from recognition.utils import delete_face_data, get_face_encoding, predict_face, save_face_data
from app.errors import MissingParameterError, ResourceNotFoundError


@app.route("/update", methods=["POST"])
def update():
    """
    Update or add a user's face data to the recognition system.
    
    Request:
        - Method: POST
        - Form parameters:
            - user_id: Unique identifier for the user
        - Files:
            - image: User's face image file
            
    Returns:
        - 200: JSON response with success message
        
    Raises:
        - MissingParameterError: If user_id or image is missing
        - NoFaceError: If no face is detected in the image
        - MultipleFacesError: If multiple faces are detected in the image
    """
    if 'image' not in request.files:
        raise MissingParameterError("URL Gambar")
    
    if 'user_id' not in request.form:
        raise MissingParameterError("ID Pengguna")

    user_id = int(request.form.get('user_id'))
    image = request.files['image']
    
    encoding = get_face_encoding(image)
    save_face_data(user_id, encoding)
    return jsonify({"message": f"Pengguna {user_id} berhasil diperbarui!"}), 200

@app.route("/recognize", methods=["POST"])
def recognize():
    """
    Recognize a user from their face image.
    
    Request:
        - Method: POST
        - Files:
            - image: Face image to be recognized
            
    Returns:
        - 200: JSON response with the recognized user_id in the data field
        
    Raises:
        - MissingParameterError: If image is missing
        - ValidationError: If no matching face is found
        - NoFaceError: If no face is detected in the image
        - MultipleFacesError: If multiple faces are detected in the image
    """
    if 'image' not in request.files:
        raise MissingParameterError("URL Gambar")
    
    image = request.files['image']
    
    encoding = get_face_encoding(image)
    prediction = predict_face(encoding)
    
    if prediction is None:
        raise NoFaceError("Tidak ada wajah yang cocok ditemukan")
    
    return jsonify({"data": int(prediction)}), 200
    
@app.route("/delete", methods=["DELETE"])
def delete():
    """
    Delete a user's face data from the recognition system.
    
    Request:
        - Method: DELETE
        - JSON body:
            - user_id: Unique identifier of the user to delete
            
    Returns:
        - 200: JSON response with success message
        
    Raises:
        - MissingParameterError: If user_id is missing
        - ResourceNotFoundError: If the specified user is not found
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Check if the JSON data exists and has user_id
    if not data or 'user_id' not in data:
        raise MissingParameterError("ID Pengguna dalam body JSON")

    user_id = int(data['user_id'])

    if delete_face_data(user_id):
        return jsonify({"message": f"Pengguna {user_id} berhasil dihapus!"}), 200
    
    raise ResourceNotFoundError(f"Pengguna {user_id} tidak ditemukan")