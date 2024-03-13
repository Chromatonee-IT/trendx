import uuid

def generate_ref_code():
    code = str(uuid.uuid4())[:12].replace("-", "").upper()
    return code

def generate_email_verification_code():
    code = str(uuid.uuid4())[:13]
    return code

import random

def generate_unique_code():
  digits = "0123456789"
  otp = ""
  for _ in range(8):
    otp += random.choice(digits)
  return otp
