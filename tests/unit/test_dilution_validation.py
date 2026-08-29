"""Input validation tests for EQ-DIL-001."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.calculations import (
    CalculationInputError,
    EQUATION_ID,
    calculate_diluted_concentration,
)
from antimicrobial_calculator.units import (
    Concentration,
    ConcentrationUnit,
    Mass,
    MassUnit,
    Volume,
    VolumeUnit,
)


SOURCE_CONCENTRATION = Concentration(
    Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
)


def test_dilution_exposes_its_traceable_equation_identifier() -> None:
    assert EQUATION_ID == "EQ-DIL-001"


@pytest.mark.parametrize(
    ("source_volume", "final_volume", "error_code"),
    [
        (Decimal("0"), Decimal("200"), "DIL-001"),
        (Decimal("20"), Decimal("0"), "DIL-002"),
        (Decimal("201"), Decimal("200"), "DIL-003"),
    ],
)
def test_dilution_rejects_physically_invalid_volumes(
    source_volume: Decimal, final_volume: Decimal, error_code: str
) -> None:
    with pytest.raises(CalculationInputError, match=error_code):
        calculate_diluted_concentration(
            SOURCE_CONCENTRATION,
            Volume(source_volume, VolumeUnit.MICROLITRE),
            Volume(final_volume, VolumeUnit.MICROLITRE),
        )


def test_dilution_rejects_a_number_without_a_concentration_unit() -> None:
    with pytest.raises(CalculationInputError, match="DIL-004"):
        calculate_diluted_concentration(  # type: ignore[arg-type]
            Decimal("1000"),
            Volume(Decimal("20"), VolumeUnit.MICROLITRE),
            Volume(Decimal("200"), VolumeUnit.MICROLITRE),
        )


def test_dilution_rejects_a_non_volume_source_input() -> None:
    with pytest.raises(CalculationInputError, match="DIL-005"):
        calculate_diluted_concentration(  # type: ignore[arg-type]
            SOURCE_CONCENTRATION,
            Mass(Decimal("20"), MassUnit.MICROGRAM),
            Volume(Decimal("200"), VolumeUnit.MICROLITRE),
        )
