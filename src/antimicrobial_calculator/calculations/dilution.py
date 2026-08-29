"""Derived calculations for volumetric dilution."""

from decimal import Decimal

from antimicrobial_calculator.units import (
    Concentration,
    ConcentrationUnit,
    Volume,
    VolumeUnit,
)

from .errors import CalculationInputError

EQUATION_ID = "EQ-DIL-001"
REQUIRED_SOURCE_VOLUME_EQUATION_ID = "EQ-DIL-002"


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


def calculate_required_source_volume(
    source_concentration: Concentration,
    target_concentration: Concentration,
    final_volume: Volume,
) -> Volume:
    """Calculate ``V₁ = (C₂ × V₂) / C₁`` for a volumetric dilution."""
    if not isinstance(source_concentration, Concentration):
        raise CalculationInputError(
            "DIL-007",
            "source_concentration must be a Concentration with an explicit unit",
        )
    if not isinstance(target_concentration, Concentration):
        raise CalculationInputError(
            "DIL-008",
            "target_concentration must be a Concentration with an explicit unit",
        )
    if not isinstance(final_volume, Volume):
        raise CalculationInputError(
            "DIL-009", "final_volume must be a Volume with an explicit unit"
        )

    source_micrograms_per_millilitre = source_concentration.to(
        ConcentrationUnit.MICROGRAM_PER_MILLILITRE
    ).value
    target_micrograms_per_millilitre = target_concentration.to(
        ConcentrationUnit.MICROGRAM_PER_MILLILITRE
    ).value

    if source_micrograms_per_millilitre <= Decimal("0"):
        raise CalculationInputError(
            "DIL-010", "source_concentration must be greater than zero"
        )
    if target_micrograms_per_millilitre <= Decimal("0"):
        raise CalculationInputError(
            "DIL-011", "target_concentration must be greater than zero"
        )
    if target_micrograms_per_millilitre > source_micrograms_per_millilitre:
        raise CalculationInputError(
            "DIL-012",
            "target_concentration cannot exceed source_concentration in a dilution",
        )
    if final_volume.value <= Decimal("0"):
        raise CalculationInputError(
            "DIL-013", "final_volume must be greater than zero"
        )

    source_volume_value = (
        target_micrograms_per_millilitre
        * final_volume.to(VolumeUnit.MICROLITRE).value
        / source_micrograms_per_millilitre
    )
    source_volume_microlitres = Volume(source_volume_value, VolumeUnit.MICROLITRE)
    return source_volume_microlitres.to(final_volume.unit)
