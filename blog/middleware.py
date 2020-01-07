from datetime import datetime
from .models import Session
from django.utils.deprecation import MiddlewareMixin

class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            sessid = request.COOKIE.get('sessid')
            session = Session.objects.get(
                key=sessid,
                expires__gt=datetime.now(),
            )
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None
