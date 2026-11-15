"""Logging helpers for the Midea Smart Home integration.

Provides adapter factories that prepend a stable context prefix (such as
``[device_name]`` or ``[cloud]``) to every log line so a line can be traced
back to its origin without scattering id/module parameters through the
format strings. The device id is still carried by HA's thread name
(``MideaConnection-<id>``), so it is not repeated in the prefix.
"""

import logging
from typing import Any, MutableMapping


class PrefixLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that prepends a fixed prefix to every message."""

    def process(
        self, msg: str, kwargs: MutableMapping[str, Any]
    ) -> tuple[str, MutableMapping[str, Any]]:
        extra = self.extra or {}
        return f"{extra['prefix']} {msg}", kwargs

def prefix_logger(logger: logging.Logger, prefix: str) -> PrefixLoggerAdapter:
    """Return a logger adapter that prepends ``prefix`` to every message."""
    return PrefixLoggerAdapter(logger, {"prefix": prefix})

def device_logger(
    logger: logging.Logger, name: str, device_id: int
) -> PrefixLoggerAdapter:
    """Return a logger adapter prefixed with ``[name]``.

    The device id is intentionally omitted here: HA already names the device
    connection thread ``MideaConnection-<id>``, so repeating the id would
    only clutter the line.
    """
    return PrefixLoggerAdapter(logger, {"prefix": f"[{name or 'unknown'}]"})
