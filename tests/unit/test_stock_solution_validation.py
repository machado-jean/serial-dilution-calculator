"""Input validation tests for EQ-STOCK-001."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.calculations import (
    CalculationInputError,
    STOCK_SOLUTION_EQUATION_ID,
    calculate_required_powder_mass,
)
from antimicrobial_calculator.domain import Potency
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


VALID_CONCENTRATION = Concentration(
    Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
)
VALID_VOLUME = Volume(Decimal("1"), VolumeUnit.MILLILITRE)


def test_stock_solution_exposes_its_traceable_equation_identifier() -> None:
    assert STOCK_SOLUTION_EQUATION_ID == "EQ-STOCK-001"


def test_stock_solution_rejects_unknown_potency() -> None:
    with pytest.raises(CalculationInputError, match="STOCK-001"):
        calculate_required_powder_mass(VALID_CONCENTRATION, VALID_VOLUME, None)


@pytest.mark.parametrize(
    ("concentration", "volume", "error_code"),
    [
        (
            Concentration(Decimal("0"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
            VALID_VOLUME,
            "STOCK-005",
        ),
        (
            VALID_CONCENTRATION,
            Volume(Decimal("0"), VolumeUnit.MILLILITRE),
            "STOCK-006",
        ),
    ],
)
def test_stock_solution_rejects_zero_preparation_inputs(
    concentration: Concentration, volume: Volume, error_code: str
) -> None:
    with pytest.raises(CalculationInputError, match=error_code):
        calculate_required_powder_mass(concentration, volume, Potency(Decimal("1")))


def test_stock_solution_rejects_a_number_without_a_concentration_unit() -> None:
    with pytest.raises(CalculationInputError, match="STOCK-002"):
        calculate_required_powder_mass(  # type: ignore[arg-type]
            Decimal("1000"), VALID_VOLUME, Potency(Decimal("1"))
        )
