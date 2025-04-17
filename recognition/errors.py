"""
Custom exception classes for face recognition errors.
"""

from app.errors import AppError

class RecognitionError(AppError):
    """Base class for all face recognition related errors"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="An error occurred during face recognition"):
        super().__init__(message)

class MultipleFacesError(RecognitionError):
    """Exception raised when multiple faces are detected in the image"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="Multiple faces detected in the image"):
        super().__init__(message)

class NoFaceError(RecognitionError):
    """Exception raised when no face is detected in the image"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="No face detected in the image"):
        super().__init__(message)