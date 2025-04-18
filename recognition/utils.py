import cv2
import face_recognition
import numpy as np
import joblib
import os

from sklearn import svm
from recognition.errors import MultipleFacesError, NoFaceError
from app.errors import AppError

MODEL_PATH = 'recognition/model.pkl'

def get_face_encoding(image_source):
    """
    Generate face encoding from an image URL or uploaded file
    
    Args:
        image_source: URL of the image or file object
        
    Returns:
        numpy.ndarray: Face encoding found in the image
        
    Raises:
        NoFaceError: When no face is detected in the image
        MultipleFacesError: When multiple faces are detected in the image
        AppError: Base class for all application errors
    """
    # Read image from uploaded file
    file_bytes = image_source.read()
    np_array = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    # Convert from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Find face locations
    face_locations = face_recognition.face_locations(rgb_img)
    
    # If no faces found
    if not face_locations:
        raise NoFaceError()
    
    # If contains multiple faces:
    if len(face_locations) > 1:
        raise MultipleFacesError()
        
    # Generate encodings
    face_encoding = face_recognition.face_encodings(rgb_img, face_locations)[0]
    
    return face_encoding

def load_data():
    """
    Load face recognition model data from disk or initialize a new model.
    
    Returns:
        tuple: A tuple containing:
            - classifier (sklearn.svm.SVC): SVM classifier for face recognition
            - ids (list): List of user IDs corresponding to face encodings
            - encodings (list): List of face encodings used for training
    """
    if (os.path.exists(MODEL_PATH)):
        classifier, ids, encodings = joblib.load(MODEL_PATH)
    else:
        classifier = svm.SVC(gamma='scale')
        ids = []
        encodings = []

    return classifier, ids, encodings

def train_classifier(classifier, ids, encodings):
    """
    Train the SVM classifier with face encodings and save the model to disk.
    
    Args:
        classifier (sklearn.svm.SVC): SVM classifier to train
        ids (list): List of user IDs corresponding to face encodings
        encodings (list): List of face encodings to train the classifier with
        
    Note:
        Training is only performed when there are at least 2 face encodings.
        The trained model and data are saved to disk at MODEL_PATH.
    """
    # Train the classifier with the updated data
    if (len(encodings) > 1):
        classifier.fit(encodings, ids)
    
    # Save the updated classifier and data
    joblib.dump((classifier, ids, encodings), MODEL_PATH)

def save_face_data(id, encoding):
    """
    Save or update a user's face encoding in the recognition model.
    
    Args:
        id: User identifier
        encoding (numpy.ndarray): Face encoding to save
        
    Note:
        If the user ID already exists, their face encoding will be updated.
        Otherwise, a new entry will be added to the model.
        The model is automatically retrained and saved after the update.
    """
    classifier, ids, encodings = load_data()
    
    # If the user already exists, update their encoding
    if id in ids:
        index = ids.index(id)
        encodings[index] = encoding
    else:
        ids.append(id)
        encodings.append(encoding)

    train_classifier(classifier, ids, encodings)

def predict_face(encoding):
    """
    Predict the identity of a face from its encoding.
    
    Args:
        encoding (numpy.ndarray): Face encoding to identify
        
    Returns:
        Union[str, None]: User ID of the recognized face, or None if:
            - The face is not recognized (distance above threshold)
            - There are not enough samples to perform prediction
            - No match is found
            
    Note:
        Uses face distance to verify the match quality with a threshold of 0.6.
        Lower distances indicate better matches.
    """
    classifier, ids, encodings = load_data()
    
    # Predict the class of the input encoding
    if (len(encodings) > 1):
        prediction = classifier.predict([encoding])
        predicted_id = prediction[0]
        
        # Get the index of the predicted ID
        predicted_index = ids.index(predicted_id)
        
        # Calculate the distance only for the predicted face
        distance = face_recognition.face_distance([encodings[predicted_index]], encoding)[0]

        print(f"Predicted ID: {predicted_id}, Distance: {distance}")
        
        # Set a threshold for the distance
        # Lower distances indicate better matches
        threshold = 0.5
        if distance > threshold:
            return None

        return predicted_id
    else:
        return None
    
def delete_face_data(id):
    """
    Remove a user's face data from the recognition model.
    
    Args:
        id: User identifier to remove
        
    Returns:
        bool: True if the user was found and deleted, False if the user was not found
        
    Note:
        If the user is found and deleted, the model is automatically retrained
        and saved with the updated data.
    """
    classifier, ids, encodings = load_data()

    # If the user exists, remove their encoding
    if id in ids:
        index = ids.index(id)
        del ids[index]
        del encodings[index]

        train_classifier(classifier, ids, encodings)
        
        return True
    else:
        return False