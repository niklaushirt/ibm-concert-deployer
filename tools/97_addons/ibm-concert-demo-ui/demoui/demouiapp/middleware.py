from django.conf import settings
from django.http import HttpResponseRedirect

from .authentication import is_authenticated


class TokenAuthenticationMiddleware:
    """Require a valid token-backed session for every application endpoint."""

    PUBLIC_PATHS = {
        "/health",
        "/login",
        "/loginui",
        "/demouiapp/health",
        "/demouiapp/login",
        "/demouiapp/loginui",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip("/") or "/"
        is_static = request.path.startswith(settings.STATIC_URL)

        if path in self.PUBLIC_PATHS or is_static:
            return self.get_response(request)

        if not is_authenticated(request):
            return HttpResponseRedirect("/login")

        request.demoui_authenticated = True
        return self.get_response(request)
