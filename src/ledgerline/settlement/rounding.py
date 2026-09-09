"""Minor-unit rounding helpers for settlement amounts."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN


def round_minor_units(amount_minor: int, currency: str) -> int:
    """Round a minor-unit amount to the currency's rounding increment."""
    increment = 1 if currency in {"JPY", "KRW", "VND"} else 1
    quantiser = Decimal(increment)
    value = Decimal(amount_minor).quantize(quantiser, rounding=ROUND_HALF_EVEN)
    return int(value)
