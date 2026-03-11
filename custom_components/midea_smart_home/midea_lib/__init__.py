"""
Midea Smart Home Library.

This library provides the core communication layer for Midea smart devices,
handling protocol encryption, packet construction, and device control.
"""

from .device import DeviceController
from .exceptions import MideaError

__all__ = ["DeviceController", "MideaError"]
