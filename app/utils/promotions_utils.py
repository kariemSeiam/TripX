import string
import random

def generate_promo_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
