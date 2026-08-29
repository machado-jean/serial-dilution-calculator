"""Unit and analytical conversion tests for the dimensional model."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.units import (
    Concentration,
    ConcentrationUnit,
    Mass,
    MassUnit,
    QuantityValidationError,
    Volume,
    VolumeUnit,
)


@pytest.mark.parametrize(
    ("quantity", "target_unit", "expected_value"),
    [
        (Mass(Decimal("1"), MassUnit.GRAM), MassUnit.MILLIGRAM, Decimal("1000")),
        (Mass(Decimal("1"), MassUnit.MILLIGRAM), MassUnit.MICROGRAM, Decimal("1000")),
        (Volume(Decimal("1"), VolumeUnit.LITRE), VolumeUnit.MILLILITRE, Decimal("1000")),
        (
            Volume(Decimal("1"), VolumeUnit.MILLILITRE),
            VolumeUnit.MICROLITRE,
            Decimal("1000"),
        ),
    ],
)
def test_mass_and_volume_conversions_are_exact(
    quantity: Mass | Volume,
    target_unit: MassUnit | VolumeUnit,
    expected_value: Decimal,
) -> None:
    converted = quantity.to(target_unit)  # type: ignore[arg-type]

    assert converted.value == expected_value
    assert converted.unit is target_unit


def test_milligram_per_millilitre_converts_to_microgram_per_millilitre() -> None:
    concentration = Concentration(
        Decimal("1.25"), ConcentrationUnit.MILLIGRAM_PER_MILLILITRE
    )

    converted = concentration.to(ConcentrationUnit.MICROGRAM_PER_MILLILITRE)

    assert converted.value == Decimal("1250")


def test_conversion_preserves_decimal_precision_without_rounding() -> None:
    volume = Volume(Decimal("0.0001"), VolumeUnit.MILLILITRE)

    assert volume.to(VolumeUnit.MICROLITRE).value == Decimal("0.1")


@pytest.mark.parametrize("invalid_value", [1, 1.0, "1"])
def test_quantity_rejects_non_decimal_values(invalid_value: object) -> None:
    with pytest.raises(QuantityValidationError, match="UNIT-001"):
        Mass(invalid_value, MassUnit.MILLIGRAM)  # type: ignore[arg-type]


def test_quantity_rejects_negative_values() -> None:
    with pytest.raises(QuantityValidationError, match="UNIT-003"):
        Volume(Decimal("-0.01"), VolumeUnit.MILLILITRE)


def test_quantity_rejects_a_unit_from_another_dimension() -> None:
    with pytest.raises(QuantityValidationError, match="UNIT-004"):
        Mass(Decimal("1"), VolumeUnit.MILLILITRE)  # type: ignore[arg-type]


def test_cross_dimension_addition_is_not_defined() -> None:
    mass = Mass(Decimal("1"), MassUnit.MILLIGRAM)
    volume = Volume(Decimal("1"), VolumeUnit.MILLILITRE)

    with pytest.raises(TypeError):
        _ = mass + volume  # type: ignore[operator]


def test_zero_is_a_valid_dimensional_quantity() -> None:
    concentration = Concentration(
        Decimal("0"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
    )

    assert concentration.value == Decimal("0")
