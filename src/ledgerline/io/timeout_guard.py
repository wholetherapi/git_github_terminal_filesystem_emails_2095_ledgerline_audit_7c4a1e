"""Timeout helpers for ledger reader calls."""

from __future__ import annotations

import signal
import threading
from contextlib import contextmanager


class ReaderTimeout(Exception):
    """Raised when a ledger reader call exceeds its budget."""


@contextmanager
def reader_timeout(seconds: float = 30.0):
    """Apply a wall-clock guard around a reader call.

    Uses SIGALRM on the main thread and falls back to a timer thread elsewhere.
    """
    if threading.current_thread() is threading.main_thread() and hasattr(signal, "SIGALRM"):
        def _raise_timeout(signum, frame):  # noqa: ANN001
            raise ReaderTimeout(f"reader call exceeded {seconds:.0f}s")

        previous = signal.signal(signal.SIGALRM, _raise_timeout)
        signal.setitimer(signal.ITIMER_REAL, seconds)
        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)
    else:
        timer = threading.Timer(seconds, lambda: (_ for _ in ()).throw(ReaderTimeout("reader call timed out")))
        timer.start()
        try:
            yield
        finally:
            timer.cancel()
