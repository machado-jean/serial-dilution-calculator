"""Tests for laboratory-specific pipetting constraints."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.domain import (
    LaboratoryConstraintError,
    PipetteConstraint,
)
from antimicrobial_calculator.planning import (
    FeasibilityStatus,
    PlanningInputError,
    evaluate_transfer_volume,
)
from antimicrobial_calculator.units import Mass, MassUnit, Volume, VolumeUnit


CONSTRAINT = PipetteConstraint(
    minimum_reliable_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE),
    maximum_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
)


@pytest.mark.parametrize(
    ("transfer_value", "expected_status"),
    [
        (Decimal("25"), FeasibilityStatus.INFO),
        (Decimal("20"), FeasibilityStatus.CAUTION),
        (Decimal("19.9"), FeasibilityStatus.INVALID),
        (Decimal("201"), FeasibilityStatus.INVALID),
    ],
)
def test_transfer_feasibility_respects_configured_limits(
    transfer_value: Decimal, expected_status: FeasibilityStatus
) -> None:
    result = evaluate_transfer_volume(
        Volume(transfer_value, VolumeUnit.MICROLITRE), CONSTRAINT
    )

    assert result.status is expected_status
    assert result.is_feasible is (expected_status is not FeasibilityStatus.INVALID)


def test_transfer_at_minimum_emits_an_operational_warning() -> None:
    result = evaluate_transfer_volume(
        Volume(Decimal("0.020"), VolumeUnit.MILLILITRE), CONSTRAINT
    )

    assert result.status is FeasibilityStatus.CAUTION
    assert result.warnings


def test_missing_maximum_is_reported_as_not_evaluated() -> None:
    constraint_without_maximum = PipetteConstraint(
        minimum_reliable_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE)
    )

    result = evaluate_transfer_volume(
        Volume(Decimal("500"), VolumeUnit.MICROLITRE), constraint_without_maximum
    )

    assert result.status is FeasibilityStatus.INFO
    assert "não foi configurada" in result.warnings[0]


@pytest.mark.parametrize(
    ("minimum", "maximum", "error_code"),
    [
        (Decimal("0"), Decimal("200"), "LAB-003"),
        (Decimal("20"), Decimal("19"), "LAB-004"),
    ],
)
def test_constraint_rejects_inconsistent_volume_limits(
    minimum: Decimal, maximum: Decimal, error_code: str
) -> None:
    with pytest.raises(LaboratoryConstraintError, match=error_code):
        PipetteConstraint(
            minimum_reliable_volume=Volume(minimum, VolumeUnit.MICROLITRE),
            maximum_volume=Volume(maximum, VolumeUnit.MICROLITRE),
        )


def test_transfer_evaluation_rejects_a_non_volume_input() -> None:
    with pytest.raises(PlanningInputError, match="PLAN-001"):
        evaluate_transfer_volume(  # type: ignore[arg-type]
            Mass(Decimal("20"), MassUnit.MICROGRAM), CONSTRAINT
        )
