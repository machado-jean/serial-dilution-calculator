"""Derived calculations for concentration correction after inoculation."""

from decimal import Decimal

from antimicrobial_calculator.units import Concentration, Volume, VolumeUnit

from .errors import CalculationInputError

FINAL_CONCENTRATION_EQUATION_ID = "EQ-INOC-001"
REQUIRED_PRE_INOCULATION_EQUATION_ID = "EQ-INOC-002"


def calculate_final_concentration_after_inoculation(
    pre_inoculation_concentration: Concentration,
    pre_inoculation_volume: Volume,
    inoculum_volume: Volume,
) -> Concentration:
    """Calculate ``C_final = C_pre × V_pre / (V_pre + V_inoculum)``."""
    _validate_inputs(
        pre_inoculation_concentration, pre_inoculation_volume, inoculum_volume
    )
    dilution_factor = _inoculation_dilution_factor(
        pre_inoculation_volume, inoculum_volume
    )
    return Concentration(
        pre_inoculation_concentration.value / dilution_factor,
        pre_inoculation_concentration.unit,
    )


def calculate_required_pre_inoculation_concentration(
    final_concentration: Concentration,
    pre_inoculation_volume: Volume,
    inoculum_volume: Volume,
) -> Concentration:
    """Calculate ``C_pre = C_final × (V_pre + V_inoculum) / V_pre``."""
    _validate_inputs(final_concentration, pre_inoculation_volume, inoculum_volume)
    dilution_factor = _inoculation_dilution_factor(
        pre_inoculation_volume, inoculum_volume
    )
    return Concentration(
        final_concentration.value * dilution_factor,
        final_concentration.unit,
    )


def _validate_inputs(
    concentration: object, pre_inoculation_volume: object, inoculum_volume: object
) -> None:
    if not isinstance(concentration, Concentration):
        raise CalculationInputError(
            "INOC-001", "concentration must be a Concentration with an explicit unit"
        )
    if not isinstance(pre_inoculation_volume, Volume):
        raise CalculationInputError(
            "INOC-002", "pre_inoculation_volume must be a Volume with an explicit unit"
        )
    if not isinstance(inoculum_volume, Volume):
        raise CalculationInputError(
            "INOC-003", "inoculum_volume must be a Volume with an explicit unit"
        )
    if concentration.value <= Decimal("0"):
        raise CalculationInputError("INOC-004", "concentration must be greater than zero")
    if pre_inoculation_volume.value <= Decimal("0"):
        raise CalculationInputError(
            "INOC-005", "pre_inoculation_volume must be greater than zero"
        )


def _inoculation_dilution_factor(
    pre_inoculation_volume: Volume, inoculum_volume: Volume
) -> Decimal:
    pre_inoculation_microlitres = pre_inoculation_volume.to(VolumeUnit.MICROLITRE).value
    inoculum_microlitres = inoculum_volume.to(VolumeUnit.MICROLITRE).value
    return (pre_inoculation_microlitres + inoculum_microlitres) / pre_inoculation_microlitres
