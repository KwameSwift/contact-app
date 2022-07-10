import re

from helpers.status_codes import EmptyParameters, InvalidEmail

def validate_email(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if not re.match(pat,s):
      raise InvalidEmail()

def check_parameters(data, param):
   if not data:
      status_code = 309
      default_detail = {
        "status": "Error",
        "code": status_code,
        "detail": param + " is required",
      }
      raise EmptyParameters(default_detail)
   