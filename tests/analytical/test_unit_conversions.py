"""Analytically known dimensional conversion cases."""

from decimal import Decimal

from antimicrobial_calculator.units import Concentration, ConcentrationUnit


def test_one_microgram_per_millilitre_equals_one_milligram_per_litre() -> None:
    concentration = Concentration(
        Decimal("1"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
    )

    converted = concentration.to(ConcentrationUnit.MILLIGRAM_PER_LITRE)

    assert converted.value == Decimal("1")
    assert converted.unit is ConcentrationUnit.MILLIGRAM_PER_LITRE
