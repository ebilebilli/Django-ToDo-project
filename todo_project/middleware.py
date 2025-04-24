from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            return self.get_response(request)
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        if not request.user.is_authenticated and request.path != settings.LOGIN_URL:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return self.get_response(request)