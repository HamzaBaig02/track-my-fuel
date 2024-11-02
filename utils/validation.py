import re

def clean_number_input(value,precision=2):
    new_value = 0.0 if abs(value) < 1e-10 else value
    return round(new_value,precision)

def is_valid_email(email):
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_pattern, email) is not None