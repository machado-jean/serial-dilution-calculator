"""Analytically known case for the one-step intermediate planner."""

from decimal import Decimal

from antimicrobial_calculator.domain import PipetteConstraint
from antimicrobial_calculator.planning import IntermediateSolutionPlan, plan_dilution
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


def test_one_step_intermediate_plan_for_a_two_microlitre_direct_transfer() -> None:
    plan = plan_dilution(
        source_concentration=Concentration(
            Decimal("10000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
        ),
        target_concentration=Concentration(
            Decimal("100"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE
        ),
        final_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
        constraint=PipetteConstraint(
            minimum_reliable_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE)
        ),
    )

    assert isinstance(plan, IntermediateSolutionPlan)
    assert plan.intermediate_concentration.value == Decimal("1000")
    assert plan.intermediate_total_volume.value == Decimal("200")
    assert plan.source_to_intermediate_volume.value == Decimal("20")
    assert plan.diluent_for_intermediate_volume.value == Decimal("180")
    assert plan.intermediate_to_final_volume.value == Decimal("20")
    assert plan.diluent_for_final_volume.value == Decimal("180")
