"""Derived calculations for potency-aware stock-solution preparation."""

from decimal import Decimal

from antimicrobial_calculator.domain import Potency
from antimicrobial_calculator.units import (
    Concentration,
    ConcentrationUnit,
    Mass,
    MassUnit,
    Volume,
    VolumeUnit,
)

from .errors import CalculationInputError

EQUATION_ID = "EQ-STOCK-001"


def calculate_required_powder_mass(
    target_concentration: Concentration,
    final_volume: Volume,
    potency: Potency | None,
) -> Mass:
    """Calculate ``M_powder = (C_target × V_final) / P``.

    The returned mass is expressed in micrograms and can be converted by the
    dimensional model for presentation or laboratory planning.
    """
    _validate_inputs(target_concentration, final_volume, potency)

    target_micrograms_per_millilitre = target_concentration.to(
        ConcentrationUnit.MICROGRAM_PER_MILLILITRE
    ).value
    final_millilitres = final_volume.to(VolumeUnit.MILLILITRE).value

    if target_micrograms_per_millilitre <= Decimal("0"):
        raise CalculationInputError(
            "STOCK-005",
            "target_concentration must be greater than zero for stock preparation",
        )
    if final_millilitres <= Decimal("0"):
        raise CalculationInputError(
            "STOCK-006",
            "final_volume must be greater than zero for stock preparation",
        )

    powder_micrograms = (
        target_micrograms_per_millilitre * final_millilitres / potency.active_fraction
    )
    return Mass(powder_micrograms, MassUnit.MICROGRAM)


def _validate_inputs(
    target_concentration: object,
    final_volume: object,
    potency: object,
) -> None:
    if not isinstance(target_concentration, Concentration):
        raise CalculationInputError(
            "STOCK-002",
            "target_concentration must be a Concentration with an explicit unit",
        )
    if not isinstance(final_volume, Volume):
        raise CalculationInputError(
            "STOCK-003",
            "final_volume must be a Volume with an explicit unit",
        )
    if potency is None:
        raise CalculationInputError(
            "STOCK-001",
            "potency is required; provide a documented active fraction instead of assuming 100%",
        )
    if not isinstance(potency, Potency):
        raise CalculationInputError(
            "STOCK-004",
            "potency must be a Potency object with a documented active fraction",
        )
