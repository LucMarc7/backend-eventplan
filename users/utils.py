import random
import string
from django.contrib.auth.models import User

def generate_code_username(username):
    """
    Génère un nom d'utilisateur unique en ajoutant un code à 2 chiffres.
    """
    base_username = username
    while True:
        code = ''.join(random.choices(string.digits, k=2))
        new_username = f"{base_username}{code}"
        if not User.objects.filter(username=new_username).exists():
            return new_username