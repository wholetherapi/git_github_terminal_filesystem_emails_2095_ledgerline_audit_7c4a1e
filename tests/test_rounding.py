from ledgerline.settlement.rounding import round_minor_units


def test_zero_decimal_currency_keeps_minor_units():
    assert round_minor_units(1200, "JPY") == 1200


def test_standard_currency_rounds_to_one():
    assert round_minor_units(1201, "EUR") == 1201
