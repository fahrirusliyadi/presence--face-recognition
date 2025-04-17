"""
Application-wide custom exception classes.
"""

class AppError(Exception):
    """Base class for all application errors"""
    status_code = 500  # Default to 500 Internal Server Error
    
    def __init__(self, message="An error occurred in the application"):
        self.message = message
        super().__init__(self.message)

class ValidationError(AppError):
    """Error raised when request validation fails"""
    status_code = 400  # Bad Request
    
    def __init__(self, message="Invalid request data"):
        super().__init__(message)

class MissingParameterError(ValidationError):
    """Error raised when a required parameter is missing"""
    status_code = 400  # Bad Request
    
    def __init__(self, parameter_name):
        super().__init__(f"{parameter_name} is required")

class ResourceNotFoundError(AppError):
    """Error raised when a requested resource is not found"""
    status_code = 404  # Not Found
    
    def __init__(self, message="Resource not found"):
        super().__init__(message)