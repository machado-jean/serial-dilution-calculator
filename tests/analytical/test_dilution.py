"""Analytically known cases for EQ-DIL-001."""

from decimal import Decimal

from antimicrobial_calculator.calculations import calculate_diluted_concentration
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


def test_eq_dil_001_calculates_known_twenty_to_two_hundred_microlitre_case() -> None:
    result = calculate_diluted_concentration(
        source_concentration=Concentration(
            Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
        ),
        source_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE),
        final_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
    )

    assert result.value == Decimal("100")
    assert result.unit is ConcentrationUnit.MICROGRAM_PER_MILLILITRE


def test_eq_dil_001_normalizes_mixed_volume_units() -> None:
    result = calculate_diluted_concentration(
        source_concentration=Concentration(
            Decimal("1"), ConcentrationUnit.MILLIGRAM_PER_MILLILITRE
        ),
        source_volume=Volume(Decimal("0.020"), VolumeUnit.MILLILITRE),
        final_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
    )

    assert result.value == Decimal("0.1")
    assert result.unit is ConcentrationUnit.MILLIGRAM_PER_MILLILITRE
