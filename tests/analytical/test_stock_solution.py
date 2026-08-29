"""Analytically known cases for EQ-STOCK-001."""

from decimal import Decimal

from antimicrobial_calculator.calculations import calculate_required_powder_mass
from antimicrobial_calculator.domain import Potency
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, MassUnit, Volume, VolumeUnit


def test_eq_stock_001_corrects_required_mass_for_active_fraction() -> None:
    result = calculate_required_powder_mass(
        target_concentration=Concentration(
            Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
        ),
        final_volume=Volume(Decimal("1"), VolumeUnit.MILLILITRE),
        potency=Potency(Decimal("0.80")),
    )

    assert result.value == Decimal("1250")
    assert result.unit is MassUnit.MICROGRAM


def test_eq_stock_001_normalizes_mixed_units() -> None:
    result = calculate_required_powder_mass(
        target_concentration=Concentration(
            Decimal("2"), ConcentrationUnit.MILLIGRAM_PER_MILLILITRE
        ),
        final_volume=Volume(Decimal("500"), VolumeUnit.MICROLITRE),
        potency=Potency(Decimal("0.50")),
    )

    assert result.to(MassUnit.MILLIGRAM).value == Decimal("2")
