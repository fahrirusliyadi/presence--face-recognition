"""
Custom exception classes for face recognition errors.
"""

from app.errors import AppError

class RecognitionError(AppError):
    """Base class for all face recognition related errors"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="Terjadi kesalahan selama proses pengenalan wajah"):
        super().__init__(message)

class MultipleFacesError(RecognitionError):
    """Exception raised when multiple faces are detected in the image"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="Terdeteksi banyak wajah dalam gambar"):
        super().__init__(message)

class NoFaceError(RecognitionError):
    """Exception raised when no face is detected in the image"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="Tidak ada wajah yang terdeteksi dalam gambar"):
        super().__init__(message)