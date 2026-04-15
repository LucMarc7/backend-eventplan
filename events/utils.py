from .models import Mariage
import random
import string


def generate_mariage_code():
    code = ''.join(random.choices(string.digits, k=6))
    while Mariage.objects.filter(event_code=code).exists():
        code = ''.join(random.choices(string.digits, k=6))
    return code
