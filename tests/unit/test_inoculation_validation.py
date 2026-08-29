"""Input validation tests for inoculation correction."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.calculations import (
    CalculationInputError,
    FINAL_CONCENTRATION_EQUATION_ID,
    REQUIRED_PRE_INOCULATION_EQUATION_ID,
    calculate_final_concentration_after_inoculation,
)
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Mass, MassUnit, Volume, VolumeUnit


VALID_CONCENTRATION = Concentration(
    Decimal("8"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
)
VALID_PRE_VOLUME = Volume(Decimal("100"), VolumeUnit.MICROLITRE)


def test_inoculation_exposes_traceable_equation_identifiers() -> None:
    assert FINAL_CONCENTRATION_EQUATION_ID == "EQ-INOC-001"
    assert REQUIRED_PRE_INOCULATION_EQUATION_ID == "EQ-INOC-002"


def test_inoculation_rejects_zero_pre_inoculation_volume() -> None:
    with pytest.raises(CalculationInputError, match="INOC-005"):
        calculate_final_concentration_after_inoculation(
            VALID_CONCENTRATION,
            Volume(Decimal("0"), VolumeUnit.MICROLITRE),
            VALID_PRE_VOLUME,
        )


def test_inoculation_rejects_an_input_without_volume_dimension() -> None:
    with pytest.raises(CalculationInputError, match="INOC-003"):
        calculate_final_concentration_after_inoculation(  # type: ignore[arg-type]
            VALID_CONCENTRATION,
            VALID_PRE_VOLUME,
            Mass(Decimal("100"), MassUnit.MICROGRAM),
        )


def test_zero_inoculum_is_an_explicit_mathematical_boundary_case() -> None:
    result = calculate_final_concentration_after_inoculation(
        VALID_CONCENTRATION,
        VALID_PRE_VOLUME,
        Volume(Decimal("0"), VolumeUnit.MICROLITRE),
    )

    assert result.value == VALID_CONCENTRATION.value
