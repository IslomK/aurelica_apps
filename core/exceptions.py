from rest_framework.exceptions import APIException


class BaseError(APIException):
    status_code = None
    error_type = None

    def __init__(self, message=None):
        self.detail = {
            'status': 'error',
            'error_id': self.error_type,
            'message': message
        }


class InternalServiceError(BaseError):
    status_code = 500


class BadRequest(BaseError):
    status_code = 400


class NotFoundError(BaseError):
    status_code = 404
