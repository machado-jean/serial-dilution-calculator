"""Validation tests for the active-fraction domain type."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.domain import Potency, PotencyValidationError


@pytest.mark.parametrize("invalid_value", [Decimal("0"), Decimal("-0.01"), Decimal("1.01")])
def test_potency_rejects_values_outside_the_active_fraction_interval(
    invalid_value: Decimal,
) -> None:
    with pytest.raises(PotencyValidationError):
        Potency(invalid_value)


def test_potency_rejects_non_decimal_values() -> None:
    with pytest.raises(PotencyValidationError, match="POT-001"):
        Potency(0.80)  # type: ignore[arg-type]
