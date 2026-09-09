"""Timeout helpers for ledger reader calls."""

from __future__ import annotations

import socket
from contextlib import contextmanager


class ReaderTimeout(Exception):
    """Raised when a ledger reader call exceeds its budget."""


@contextmanager
def reader_timeout(seconds: float = 30.0):
    """Apply a coarse wall-clock guard around a reader call."""
    previous = socket.getdefaulttimeout()
    socket.setdefaulttimeout(seconds)
    try:
        yield
    finally:
        socket.setdefaulttimeout(previous)
