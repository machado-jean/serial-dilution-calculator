"""Experimental one-step planning for an infeasible direct dilution."""

from dataclasses import dataclass
from decimal import Decimal

from antimicrobial_calculator.calculations import calculate_required_source_volume
from antimicrobial_calculator.domain import PipetteConstraint
from antimicrobial_calculator.units import Concentration, Volume, VolumeUnit

from .pipetting import FeasibilityStatus, TransferFeasibility, evaluate_transfer_volume


class IntermediatePlanningError(ValueError):
    """Raised when the deterministic one-step plan cannot be constructed."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class DirectDilutionPlan:
    """A direct dilution whose source transfer meets laboratory constraints."""

    source_transfer_volume: Volume
    diluent_volume: Volume
    final_volume: Volume
    feasibility: TransferFeasibility


@dataclass(frozen=True, slots=True)
class IntermediateSolutionPlan:
    """An experimental, deterministic plan using one intermediate solution."""

    intermediate_concentration: Concentration
    intermediate_total_volume: Volume
    source_to_intermediate_volume: Volume
    diluent_for_intermediate_volume: Volume
    intermediate_to_final_volume: Volume
    diluent_for_final_volume: Volume
    direct_feasibility: TransferFeasibility
    source_to_intermediate_feasibility: TransferFeasibility
    intermediate_to_final_feasibility: TransferFeasibility
    classification: str = "EXPERIMENTAL"


def plan_dilution(
    source_concentration: Concentration,
    target_concentration: Concentration,
    final_volume: Volume,
    constraint: PipetteConstraint,
) -> DirectDilutionPlan | IntermediateSolutionPlan:
    """Plan a direct dilution or one intermediate step under a lab constraint."""
    _validate_inputs(source_concentration, target_concentration, final_volume, constraint)

    direct_source_volume = calculate_required_source_volume(
        source_concentration, target_concentration, final_volume
    )
    direct_feasibility = evaluate_transfer_volume(direct_source_volume, constraint)
    if direct_feasibility.is_feasible:
        return DirectDilutionPlan(
            source_transfer_volume=direct_source_volume,
            diluent_volume=_subtract_volumes(final_volume, direct_source_volume),
            final_volume=final_volume,
            feasibility=direct_feasibility,
        )

    minimum_volume = constraint.minimum_reliable_volume
    direct_microlitres = direct_source_volume.to(VolumeUnit.MICROLITRE).value
    minimum_microlitres = minimum_volume.to(VolumeUnit.MICROLITRE).value
    if direct_microlitres > minimum_microlitres:
        raise IntermediatePlanningError(
            "INT-001",
            "the direct transfer exceeds the configured maximum; one intermediate dilution cannot resolve this case",
        )
    if minimum_microlitres > final_volume.to(VolumeUnit.MICROLITRE).value:
        raise IntermediatePlanningError(
            "INT-002",
            "minimum_reliable_volume exceeds final_volume; no intermediate transfer can fit in the final preparation",
        )

    target_in_source_unit = target_concentration.to(source_concentration.unit)
    intermediate_concentration = Concentration(
        target_in_source_unit.value
        * final_volume.to(VolumeUnit.MICROLITRE).value
        / minimum_microlitres,
        source_concentration.unit,
    )
    intermediate_total_volume = _calculate_intermediate_total_volume(
        source_concentration, intermediate_concentration, minimum_volume
    )
    source_to_intermediate_feasibility = evaluate_transfer_volume(
        minimum_volume, constraint
    )
    intermediate_to_final_feasibility = evaluate_transfer_volume(minimum_volume, constraint)

    return IntermediateSolutionPlan(
        intermediate_concentration=intermediate_concentration,
        intermediate_total_volume=intermediate_total_volume,
        source_to_intermediate_volume=minimum_volume,
        diluent_for_intermediate_volume=_subtract_volumes(
            intermediate_total_volume, minimum_volume
        ),
        intermediate_to_final_volume=minimum_volume,
        diluent_for_final_volume=_subtract_volumes(final_volume, minimum_volume),
        direct_feasibility=direct_feasibility,
        source_to_intermediate_feasibility=source_to_intermediate_feasibility,
        intermediate_to_final_feasibility=intermediate_to_final_feasibility,
    )


def _validate_inputs(
    source_concentration: object,
    target_concentration: object,
    final_volume: object,
    constraint: object,
) -> None:
    if not isinstance(source_concentration, Concentration):
        raise IntermediatePlanningError("INT-003", "source_concentration must be a Concentration")
    if not isinstance(target_concentration, Concentration):
        raise IntermediatePlanningError("INT-004", "target_concentration must be a Concentration")
    if not isinstance(final_volume, Volume):
        raise IntermediatePlanningError("INT-005", "final_volume must be a Volume")
    if not isinstance(constraint, PipetteConstraint):
        raise IntermediatePlanningError("INT-006", "constraint must be a PipetteConstraint")


def _calculate_intermediate_total_volume(
    source_concentration: Concentration,
    intermediate_concentration: Concentration,
    minimum_volume: Volume,
) -> Volume:
    source_in_intermediate_unit = source_concentration.to(intermediate_concentration.unit)
    total_volume_value = (
        minimum_volume.to(VolumeUnit.MICROLITRE).value
        * source_in_intermediate_unit.value
        / intermediate_concentration.value
    )
    return Volume(total_volume_value, VolumeUnit.MICROLITRE).to(minimum_volume.unit)


def _subtract_volumes(total_volume: Volume, component_volume: Volume) -> Volume:
    total_microlitres = total_volume.to(VolumeUnit.MICROLITRE).value
    component_microlitres = component_volume.to(VolumeUnit.MICROLITRE).value
    if component_microlitres > total_microlitres:
        raise IntermediatePlanningError(
            "INT-007", "component volume cannot exceed total volume"
        )
    return Volume(
        total_microlitres - component_microlitres, VolumeUnit.MICROLITRE
    ).to(total_volume.unit)
