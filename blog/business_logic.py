from .models import Users, BlogSession
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
    session = BlogSession()
    session.key = generate_long_random_key(8)
    session.users = user
    session.expires = datetime.now() + timedelta(days=90)
    session.save()
    return session.key


def generate_long_random_key(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def get_user_session(request):
    try:
        session = BlogSession.objects.get(key=request.COOKIES['sessid'])
        user = Users.objects.get(user_id=session.users_id)
    except BlogSession.DoesNotExist:
        return 3
    except Users.DoesNotExist:
        return 3
    except KeyError:
        return 3
    return user
