"""Planning and boundary tests for one-step intermediate dilution."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.calculations import (
    CalculationInputError,
    calculate_required_source_volume,
)
from antimicrobial_calculator.domain import PipetteConstraint
from antimicrobial_calculator.planning import (
    DirectDilutionPlan,
    IntermediatePlanningError,
    plan_dilution,
)
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


CONSTRAINT = PipetteConstraint(
    minimum_reliable_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE),
    maximum_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
)


def test_eq_dil_002_calculates_required_source_volume() -> None:
    result = calculate_required_source_volume(
        Concentration(Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Concentration(Decimal("100"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Volume(Decimal("200"), VolumeUnit.MICROLITRE),
    )

    assert result.value == Decimal("20")
    assert result.unit is VolumeUnit.MICROLITRE


def test_planner_returns_direct_plan_when_transfer_is_feasible() -> None:
    plan = plan_dilution(
        Concentration(Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Concentration(Decimal("100"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        Volume(Decimal("200"), VolumeUnit.MICROLITRE),
        CONSTRAINT,
    )

    assert isinstance(plan, DirectDilutionPlan)
    assert plan.source_transfer_volume.value == Decimal("20")
    assert plan.diluent_volume.value == Decimal("180")


def test_planner_rejects_when_minimum_cannot_fit_in_final_volume() -> None:
    with pytest.raises(IntermediatePlanningError, match="INT-002"):
        plan_dilution(
            Concentration(Decimal("10000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
            Concentration(Decimal("100"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
            Volume(Decimal("10"), VolumeUnit.MICROLITRE),
            CONSTRAINT,
        )


def test_required_source_volume_rejects_concentration_increase() -> None:
    with pytest.raises(CalculationInputError, match="DIL-012"):
        calculate_required_source_volume(
            Concentration(Decimal("100"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
            Concentration(Decimal("1000"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
            Volume(Decimal("200"), VolumeUnit.MICROLITRE),
        )
