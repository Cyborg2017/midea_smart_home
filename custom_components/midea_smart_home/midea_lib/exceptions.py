"""Midea Smart Home library exceptions."""

from __future__ import annotations


class MideaError(Exception):
    """Base class for midea errors."""


class CannotAuthenticate(MideaError):
    """Exception raised when credentials are incorrect."""


class DataUnexpectedLength(MideaError):
    """Exception raised when data length is less or more than expected."""


class DataSignDoesntMatch(MideaError):
    """Exception raised when data sign is not matching."""


class ElementMissing(MideaError):
    """Exception raised when a element is missing."""


class MessageWrongFormat(MideaError):
    """Exception raised when message format is wrong."""

# Midea cloud API error codes, mapped to stable user-facing slugs.
# NOTE: match by code only, never by message text (messages vary by
# region/endpoint, e.g. 65027 returns Chinese).
CLOUD_ERROR_KEYS: dict[int, str] = {
    1106: "invalid_auth",            # username or password is incorrect
    3101: "invalid_auth",            # wrong password
    3102: "invalid_auth",            # account or password error
    3106: "cloud_session_expired",   # login session invalid, re-login needed
    3144: "cloud_session_expired",   # session invalid (empty loginId)
    3301: "invalid_cloud_server",    # app key invalid for this cloud
    7610: "account_locked",          # too many failures, locked ~5 minutes
    65027: "too_many_logged_in_devices",
    3201: "device_not_registered",   # device bound to another account
    1002: "cloud_error",             # missing/illegal parameter
    3004: "cloud_error",             # request rejected / endpoint disabled
    40404: "cloud_error",            # endpoint deprecated or migrated
    9999: "cloud_error",             # transient "system error"
}

# Transient cloud errors worth retrying with backoff before giving up.
TRANSIENT_CLOUD_ERROR_CODES = frozenset({9999})


class CloudLoginError(MideaError):
    """Exception raised when cloud login fails with a known error code.

    Carries the raw cloud ``code``/``message`` plus a stable
    ``error_key`` slug that config flows can map to a translated
    form error.
    """

    def __init__(self, code: int, message: str = "") -> None:
        self.code = code
        self.message = message
        self.error_key = CLOUD_ERROR_KEYS.get(code, "cloud_error")
        super().__init__(f"cloud error {code}: {message}")
