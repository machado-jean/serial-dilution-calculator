"""Analytically known cases for EQ-SER-001."""

from decimal import Decimal

from antimicrobial_calculator.calculations import generate_serial_dilution_series
from antimicrobial_calculator.domain import DilutionFactor
from antimicrobial_calculator.units import Concentration, ConcentrationUnit


def test_twofold_series_returns_known_concentrations_including_initial_position() -> None:
    series = generate_serial_dilution_series(
        Concentration(Decimal("64"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        DilutionFactor(Decimal("2")),
        4,
    )

    assert tuple(item.value for item in series) == (
        Decimal("64"),
        Decimal("32"),
        Decimal("16"),
        Decimal("8"),
    )


def test_configurable_factor_is_not_limited_to_twofold_series() -> None:
    series = generate_serial_dilution_series(
        Concentration(Decimal("81"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        DilutionFactor(Decimal("3")),
        3,
    )

    assert tuple(item.value for item in series) == (
        Decimal("81"),
        Decimal("27"),
        Decimal("9"),
    )
