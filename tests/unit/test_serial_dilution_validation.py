"""Validation tests for the serial-dilution mathematical model."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.calculations import (
    CalculationInputError,
    SERIAL_DILUTION_EQUATION_ID,
    generate_serial_dilution_series,
)
from antimicrobial_calculator.domain import (
    DilutionFactor,
    DilutionFactorValidationError,
)
from antimicrobial_calculator.units import Concentration, ConcentrationUnit


INITIAL_CONCENTRATION = Concentration(
    Decimal("64"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
)


def test_serial_dilution_exposes_traceable_equation_identifier() -> None:
    assert SERIAL_DILUTION_EQUATION_ID == "EQ-SER-001"


@pytest.mark.parametrize("value", [Decimal("1"), Decimal("0"), Decimal("-2")])
def test_dilution_factor_must_be_greater_than_one(value: Decimal) -> None:
    with pytest.raises(DilutionFactorValidationError, match="SER-003"):
        DilutionFactor(value)


@pytest.mark.parametrize("number_of_concentrations", [0, -1, 1.5, True])
def test_serial_dilution_rejects_invalid_series_sizes(
    number_of_concentrations: object,
) -> None:
    with pytest.raises(CalculationInputError):
        generate_serial_dilution_series(
            INITIAL_CONCENTRATION,
            DilutionFactor(Decimal("2")),
            number_of_concentrations,  # type: ignore[arg-type]
        )


def test_serial_dilution_rejects_zero_initial_concentration() -> None:
    with pytest.raises(CalculationInputError, match="SER-007"):
        generate_serial_dilution_series(
            Concentration(Decimal("0"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
            DilutionFactor(Decimal("2")),
            4,
        )
