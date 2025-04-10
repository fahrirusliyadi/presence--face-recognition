import cv2
import face_recognition
import numpy as np
import joblib
import os

from sklearn import svm

MODEL_PATH = 'recognition/model.pkl'

def get_face_encoding(image_source):
    """
    Generate face encoding from an image URL or uploaded file
    
    Args:
        image_source: URL of the image or file object
        
    Returns:
        numpy.ndarray: Face encoding found in the image
    """
    try:
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
            return None
        
        # If contains multiple faces:
        if len(face_locations) > 1:
            return None 
            
        # Generate encodings
        face_encoding = face_recognition.face_encodings(rgb_img, face_locations)[0]
        
        return face_encoding
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def load_data():
    if (os.path.exists(MODEL_PATH)):
        classifier, ids, encodings = joblib.load(MODEL_PATH)
    else:
        classifier = svm.SVC(gamma='scale')
        ids = []
        encodings = []

    return classifier, ids, encodings

def train_classifier(classifier, ids, encodings):
    # Train the classifier with the updated data
    if (len(encodings) > 1):
        classifier.fit(encodings, ids)
    
    # Save the updated classifier and data
    joblib.dump((classifier, ids, encodings), MODEL_PATH)

def save_face_data(id, encoding):
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
    classifier, ids, encodings = load_data()
    
    # Predict the class of the input encoding
    if (len(encodings) > 1):
        prediction = classifier.predict([encoding])

        # Calculate the distance to the closest known face
        distances = face_recognition.face_distance(encodings, encoding)
        best_match_index = np.argmin(distances)

        # Set a threshold for the distance
        threshold = 0.55
        if distances[best_match_index] > threshold:
            return None

        return prediction[0]
    else:
        return None
    
def delete_face_data(id):
    classifier, ids, encodings = load_data()

    # If the user exists, remove their encoding
    if id in ids:
        index = ids.index(id)
        del ids[index]
        del encodings[index]

        train_classifier(classifier, ids, encodings)
    else:
        print(f"User with ID {id} not found.")