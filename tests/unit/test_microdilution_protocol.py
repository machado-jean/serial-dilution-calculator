"""Tests for configurable protocol volumes and working-solution requirements."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.protocols import (
    MicrodilutionProtocol,
    ProtocolConfigurationError,
    calculate_working_solution_requirement,
    default_laboratory_microdilution_protocol,
)
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


def test_initial_preset_is_explicit_and_calculates_its_pre_inoculation_volume() -> None:
    protocol = default_laboratory_microdilution_protocol()

    assert protocol.name == "Default Laboratory Microdilution"
    assert protocol.pre_inoculation_volume.value == Decimal("200")
    assert protocol.pre_inoculation_volume.unit is VolumeUnit.MICROLITRE


def test_working_solution_requirement_uses_configured_protocol_volumes() -> None:
    requirement = calculate_working_solution_requirement(
        Concentration(Decimal("4"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        default_laboratory_microdilution_protocol(),
    )

    assert requirement.required_pre_inoculation_concentration.value == Decimal("6")
    assert requirement.required_working_concentration.value == Decimal("60")
    assert len(requirement.calculation_graph.steps) == 2


def test_changing_protocol_volumes_changes_required_working_concentration() -> None:
    protocol = MicrodilutionProtocol(
        "Custom",
        Volume(Decimal("50"), VolumeUnit.MICROLITRE),
        Volume(Decimal("150"), VolumeUnit.MICROLITRE),
        Volume(Decimal("50"), VolumeUnit.MICROLITRE),
    )

    requirement = calculate_working_solution_requirement(
        Concentration(Decimal("4"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        protocol,
    )

    assert requirement.required_pre_inoculation_concentration.value == Decimal("5")
    assert requirement.required_working_concentration.value == Decimal("20")


def test_protocol_rejects_zero_configured_volume() -> None:
    with pytest.raises(ProtocolConfigurationError, match="PROT-003"):
        MicrodilutionProtocol(
            "Invalid",
            Volume(Decimal("0"), VolumeUnit.MICROLITRE),
            Volume(Decimal("180"), VolumeUnit.MICROLITRE),
            Volume(Decimal("100"), VolumeUnit.MICROLITRE),
        )
