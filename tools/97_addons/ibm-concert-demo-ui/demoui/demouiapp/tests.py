import os
from unittest.mock import patch

from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from .authentication import (
    clear_authenticated_session,
    credentials_match,
    establish_authenticated_session,
    is_authenticated,
    is_login_rate_limited,
    register_login_failure,
)
from .middleware import TokenAuthenticationMiddleware


@override_settings(
    SECRET_KEY="test-only-signing-key",
    LOGIN_ATTEMPT_LIMIT=3,
    LOGIN_ATTEMPT_WINDOW_SECONDS=60,
)
class TokenAuthenticationTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()

    def request(self, path="/"):
        request = self.factory.get(path, REMOTE_ADDR="192.0.2.10")
        request.session = SessionStore()
        return request

    @patch.dict(os.environ, {"TOKEN": "correct horse battery staple"})
    def test_credentials_require_exact_token(self):
        self.assertTrue(credentials_match("correct horse battery staple"))
        self.assertFalse(credentials_match("wrong"))
        self.assertFalse(credentials_match("correct horse battery staple "))

    @patch.dict(os.environ, {"TOKEN": "first-token"})
    def test_sessions_are_per_browser_and_logout_clears_only_current_session(self):
        first = self.request()
        second = self.request()

        establish_authenticated_session(first)
        self.assertTrue(is_authenticated(first))
        self.assertFalse(is_authenticated(second))

        clear_authenticated_session(first)
        self.assertFalse(is_authenticated(first))

    def test_rotating_token_invalidates_existing_session(self):
        request = self.request()
        with patch.dict(os.environ, {"TOKEN": "old-token"}):
            establish_authenticated_session(request)
            self.assertTrue(is_authenticated(request))

        with patch.dict(os.environ, {"TOKEN": "new-token"}):
            self.assertFalse(is_authenticated(request))

    @patch.dict(os.environ, {"TOKEN": "configured-token"})
    def test_failed_attempts_are_rate_limited(self):
        request = self.request()
        self.assertFalse(is_login_rate_limited(request))
        for _ in range(3):
            register_login_failure(request)
        self.assertTrue(is_login_rate_limited(request))

    @patch.dict(os.environ, {"TOKEN": "configured-token"})
    def test_middleware_protects_pages_but_keeps_health_public(self):
        middleware = TokenAuthenticationMiddleware(lambda request: HttpResponse("ok"))

        protected_response = middleware(self.request("/"))
        self.assertEqual(protected_response.status_code, 302)
        self.assertEqual(protected_response.url, "/login")

        health_response = middleware(self.request("/health"))
        self.assertEqual(health_response.status_code, 200)
