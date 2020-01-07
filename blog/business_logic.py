from .models import Users, Session
from datetime import datetime, timedelta
import random
import string


def do_login(login, password):
    try:
        user = Users.objects.get(login=login)
    except Users.DoesNotExist:
        return None
    if user.password != password:
        return None
    session = Session()
    session.key = generate_long_random_key(8)
    session.users = user
    session.expires = datetime.now() + timedelta(days=5)
    session.save()
    return session.key


def generate_long_random_key(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
