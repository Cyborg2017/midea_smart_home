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
