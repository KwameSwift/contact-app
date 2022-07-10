from rest_framework.exceptions import APIException

class EmptyParameters(APIException):
    status_code = 309
    default_detail = {
        "status": "Error",
        "detail": "Empty parameter",
    }

class InvalidEmail(APIException):
    status_code = 310
    default_detail = {
        "status": "Error",
        "detail": "Invalid email",
    }

class UserDoesNotExist(APIException):
    status_code = 312
    default_detail = {
        "status": "Error",
        "detail": "User does not exist",
    }


class ContactAlreadyExists(APIException):
    status_code = 311
    default_detail = {
        "status": "Error",
        "detail": "Phone number already exists",
    }

class RecordDoesNotExist(APIException):
    status_code = 313
    default_detail = {
        "status": "Error",
        "detail": "Record does not exist",
    }

class UserAlreadyExists(APIException):
    status_code = 313
    default_detail = {
        "status": "Error",
        "detail": "User already exists with same email"
    }

class KeyError(APIException):
    status_code = 318
    default_detail = {
        "status": "Error", 
        "detail": "Key error"
        }


