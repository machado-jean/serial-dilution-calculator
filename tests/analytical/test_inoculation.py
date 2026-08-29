"""Analytically known cases for the inoculation correction equations."""

from decimal import Decimal

from antimicrobial_calculator.calculations import (
    calculate_final_concentration_after_inoculation,
    calculate_required_pre_inoculation_concentration,
)
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


def test_equal_volume_inoculation_halves_the_pre_inoculation_concentration() -> None:
    result = calculate_final_concentration_after_inoculation(
        Concentration(Decimal("8"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Volume(Decimal("100"), VolumeUnit.MICROLITRE),
        Volume(Decimal("100"), VolumeUnit.MICROLITRE),
    )

    assert result.value == Decimal("4")


def test_inverse_inoculation_correction_recovers_required_pre_inoculation_concentration() -> None:
    result = calculate_required_pre_inoculation_concentration(
        Concentration(Decimal("4"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Volume(Decimal("100"), VolumeUnit.MICROLITRE),
        Volume(Decimal("100"), VolumeUnit.MICROLITRE),
    )

    assert result.value == Decimal("8")


def test_unequal_volumes_use_the_configured_volume_ratio() -> None:
    result = calculate_final_concentration_after_inoculation(
        Concentration(Decimal("10"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Volume(Decimal("0.2"), VolumeUnit.MILLILITRE),
        Volume(Decimal("50"), VolumeUnit.MICROLITRE),
    )

    assert result.value == Decimal("8")
