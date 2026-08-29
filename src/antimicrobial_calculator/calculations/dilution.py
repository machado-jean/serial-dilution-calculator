"""Derived calculations for volumetric dilution."""

from decimal import Decimal

from antimicrobial_calculator.units import Concentration, Volume, VolumeUnit

from .errors import CalculationInputError

EQUATION_ID = "EQ-DIL-001"


def calculate_diluted_concentration(
    source_concentration: Concentration,
    source_volume: Volume,
    final_volume: Volume,
) -> Concentration:
    """Calculate ``C₂ = (C₁ × V₁) / V₂`` for a volumetric dilution.

    The final volume includes the transferred source volume. The result is
    expressed in the same concentration unit as ``source_concentration``.
    """
    _validate_inputs(source_concentration, source_volume, final_volume)

    source_volume_microlitres = source_volume.to(VolumeUnit.MICROLITRE).value
    final_volume_microlitres = final_volume.to(VolumeUnit.MICROLITRE).value

    if source_volume_microlitres <= Decimal("0"):
        raise CalculationInputError(
            "DIL-001",
            "source_volume must be greater than zero; provide the transferred volume",
        )
    if final_volume_microlitres <= Decimal("0"):
        raise CalculationInputError(
            "DIL-002",
            "final_volume must be greater than zero; provide the total final volume",
        )
    if source_volume_microlitres > final_volume_microlitres:
        raise CalculationInputError(
            "DIL-003",
            "source_volume cannot exceed final_volume in a dilution",
        )

    result_value = (
        source_concentration.value
        * source_volume_microlitres
        / final_volume_microlitres
    )
    return Concentration(result_value, source_concentration.unit)


def _validate_inputs(
    source_concentration: object,
    source_volume: object,
    final_volume: object,
) -> None:
    if not isinstance(source_concentration, Concentration):
        raise CalculationInputError(
            "DIL-004",
            "source_concentration must be a Concentration with an explicit unit",
        )
    if not isinstance(source_volume, Volume):
        raise CalculationInputError(
            "DIL-005",
            "source_volume must be a Volume with an explicit unit",
        )
    if not isinstance(final_volume, Volume):
        raise CalculationInputError(
            "DIL-006",
            "final_volume must be a Volume with an explicit unit",
        )
