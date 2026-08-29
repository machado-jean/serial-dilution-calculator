"""Immutable dimensional quantities using exact decimal conversion factors."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .errors import QuantityValidationError


class MassUnit(StrEnum):
    MICROGRAM = "µg"
    MILLIGRAM = "mg"
    GRAM = "g"


class VolumeUnit(StrEnum):
    MICROLITRE = "µL"
    MILLILITRE = "mL"
    LITRE = "L"


class ConcentrationUnit(StrEnum):
    MICROGRAM_PER_MILLILITRE = "µg/mL"
    MILLIGRAM_PER_MILLILITRE = "mg/mL"
    MILLIGRAM_PER_LITRE = "mg/L"


_MASS_TO_MICROGRAMS: dict[MassUnit, Decimal] = {
    MassUnit.MICROGRAM: Decimal("1"),
    MassUnit.MILLIGRAM: Decimal("1000"),
    MassUnit.GRAM: Decimal("1000000"),
}
_VOLUME_TO_MICROLITRES: dict[VolumeUnit, Decimal] = {
    VolumeUnit.MICROLITRE: Decimal("1"),
    VolumeUnit.MILLILITRE: Decimal("1000"),
    VolumeUnit.LITRE: Decimal("1000000"),
}
_CONCENTRATION_TO_MICROGRAMS_PER_MILLILITRE: dict[ConcentrationUnit, Decimal] = {
    ConcentrationUnit.MICROGRAM_PER_MILLILITRE: Decimal("1"),
    ConcentrationUnit.MILLIGRAM_PER_MILLILITRE: Decimal("1000"),
    ConcentrationUnit.MILLIGRAM_PER_LITRE: Decimal("1"),
}


def _validate_value(value: Decimal) -> None:
    if not isinstance(value, Decimal):
        raise QuantityValidationError(
            "UNIT-001",
            "quantity values must be decimal.Decimal; convert input explicitly before use",
        )
    if not value.is_finite():
        raise QuantityValidationError("UNIT-002", "quantity values must be finite")
    if value < Decimal("0"):
        raise QuantityValidationError("UNIT-003", "quantity values cannot be negative")


def _validate_unit(unit: object, expected_type: type[StrEnum], dimension: str) -> None:
    if not isinstance(unit, expected_type):
        raise QuantityValidationError(
            "UNIT-004",
            f"{dimension} requires a unit from {expected_type.__name__}",
        )


@dataclass(frozen=True, slots=True)
class Mass:
    """A non-negative mass with an explicit supported unit."""

    value: Decimal
    unit: MassUnit

    def __post_init__(self) -> None:
        _validate_value(self.value)
        _validate_unit(self.unit, MassUnit, "mass")

    def to(self, unit: MassUnit) -> "Mass":
        """Return this mass in ``unit`` without applying rounding."""
        _validate_unit(unit, MassUnit, "mass")
        micrograms = self.value * _MASS_TO_MICROGRAMS[self.unit]
        return Mass(micrograms / _MASS_TO_MICROGRAMS[unit], unit)


@dataclass(frozen=True, slots=True)
class Volume:
    """A non-negative volume with an explicit supported unit."""

    value: Decimal
    unit: VolumeUnit

    def __post_init__(self) -> None:
        _validate_value(self.value)
        _validate_unit(self.unit, VolumeUnit, "volume")

    def to(self, unit: VolumeUnit) -> "Volume":
        """Return this volume in ``unit`` without applying rounding."""
        _validate_unit(unit, VolumeUnit, "volume")
        microlitres = self.value * _VOLUME_TO_MICROLITRES[self.unit]
        return Volume(microlitres / _VOLUME_TO_MICROLITRES[unit], unit)


@dataclass(frozen=True, slots=True)
class Concentration:
    """A non-negative mass concentration with an explicit supported unit."""

    value: Decimal
    unit: ConcentrationUnit

    def __post_init__(self) -> None:
        _validate_value(self.value)
        _validate_unit(self.unit, ConcentrationUnit, "concentration")

    def to(self, unit: ConcentrationUnit) -> "Concentration":
        """Return this concentration in ``unit`` without applying rounding."""
        _validate_unit(unit, ConcentrationUnit, "concentration")
        micrograms_per_millilitre = (
            self.value * _CONCENTRATION_TO_MICROGRAMS_PER_MILLILITRE[self.unit]
        )
        return Concentration(
            micrograms_per_millilitre
            / _CONCENTRATION_TO_MICROGRAMS_PER_MILLILITRE[unit],
            unit,
        )
