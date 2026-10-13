import hashlib
import os

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import constant_time_compare, salted_hmac


AUTH_SESSION_KEY = "demoui_auth"
_RATE_LIMIT_KEY_PREFIX = "demoui_login_failures:"


def get_access_token():
    """Return the configured shared access token, failing closed when absent."""
    token = os.environ.get("TOKEN")
    if token is None or token == "":
        raise ImproperlyConfigured("TOKEN must contain a non-empty access token")
    return token


def _token_fingerprint(token):
    # The HMAC lets sessions be invalidated when TOKEN changes without exposing a
    # reusable password hash in Django's signed (but readable) session cookie.
    return salted_hmac("demoui.auth-token", token, secret=settings.SECRET_KEY).hexdigest()


def credentials_match(candidate):
    if not isinstance(candidate, str) or len(candidate) > 4096:
        return False
    return constant_time_compare(candidate, get_access_token())


def establish_authenticated_session(request):
    request.session.flush()
    request.session[AUTH_SESSION_KEY] = _token_fingerprint(get_access_token())
    request.session.set_expiry(settings.SESSION_COOKIE_AGE)


def clear_authenticated_session(request):
    request.session.flush()


def is_authenticated(request):
    marker = request.session.get(AUTH_SESSION_KEY, "")
    if not marker:
        return False
    return constant_time_compare(marker, _token_fingerprint(get_access_token()))


def _login_rate_limit_key(request):
    address = request.META.get("REMOTE_ADDR", "unknown")
    if getattr(settings, "TRUST_X_FORWARDED_FOR", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            address = forwarded.split(",", 1)[0].strip()
    address_hash = hashlib.sha256(address.encode("utf-8")).hexdigest()
    return f"{_RATE_LIMIT_KEY_PREFIX}{address_hash}"


def is_login_rate_limited(request):
    return cache.get(_login_rate_limit_key(request), 0) >= settings.LOGIN_ATTEMPT_LIMIT


def register_login_failure(request):
    key = _login_rate_limit_key(request)
    if cache.add(key, 1, timeout=settings.LOGIN_ATTEMPT_WINDOW_SECONDS):
        return 1
    try:
        return cache.incr(key)
    except ValueError:
        # The cache entry may expire between add() and incr().
        cache.set(key, 1, timeout=settings.LOGIN_ATTEMPT_WINDOW_SECONDS)
        return 1


def reset_login_failures(request):
    cache.delete(_login_rate_limit_key(request))
