
import string
import random

def generate_referral_code(user_id):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{user_id}-{random_string}"
