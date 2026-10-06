"""Minor-unit rounding helpers for settlement amounts."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN

ZERO_DECIMAL = {"JPY", "KRW", "VND", "CLP"}
THREE_DECIMAL = {"BHD", "KWD", "OMR"}


def round_minor_units(amount_minor: int, currency: str) -> int:
    """Normalise minor units for zero-decimal and three-decimal currencies."""
    if currency in ZERO_DECIMAL:
        return int(amount_minor)
    if currency in THREE_DECIMAL:
        return int(Decimal(amount_minor).quantize(Decimal("10"), rounding=ROUND_HALF_EVEN))
    return int(Decimal(amount_minor).quantize(Decimal("1"), rounding=ROUND_HALF_EVEN))


def split_half_cent_tie(amount_minor: int) -> tuple[int, int]:
    """Split a half-cent tie into settle and carry portions."""
    if amount_minor % 2 == 0:
        return amount_minor // 2, 0
    return amount_minor // 2, 1
