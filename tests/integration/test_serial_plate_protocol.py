"""Integration tests for the canonical physical serial-plate workflow."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.domain import DilutionFactor
from antimicrobial_calculator.plates import SerialDilutionLayout
from antimicrobial_calculator.protocols import (
    ProtocolConfigurationError,
    SerialPlateProtocol,
    default_serial_plate_protocol,
    plan_serial_plate,
)
from antimicrobial_calculator.reporting import generate_serial_plate_report
from antimicrobial_calculator.units import Concentration, ConcentrationUnit, Volume, VolumeUnit


def test_canonical_serial_plate_preserves_expected_final_concentrations() -> None:
    plan = plan_serial_plate(
        Concentration(Decimal("4"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        DilutionFactor(Decimal("2")),
        SerialDilutionLayout(1, 4),
        "A",
        default_serial_plate_protocol(),
    )

    assert plan.initial_pre_inoculation_concentration.value == Decimal("8")
    assert plan.required_working_concentration.value == Decimal("80")
    assert tuple(item.concentration.value for item in plan.pre_inoculation_map) == (
        Decimal("8"),
        Decimal("4"),
        Decimal("2"),
        Decimal("1"),
    )
    assert tuple(item.concentration.value for item in plan.final_concentration_map) == (
        Decimal("4"),
        Decimal("2"),
        Decimal("1"),
        Decimal("0.5"),
    )
    assert tuple(item.identifier for item in plan.preloaded_medium_wells) == (
        "A2",
        "A3",
        "A4",
    )
    assert tuple(
        (step.source.identifier, step.destination.identifier if step.destination else None, step.action)
        for step in plan.transfer_steps
    ) == (
        ("A1", "A2", "transfer"),
        ("A2", "A3", "transfer"),
        ("A3", "A4", "transfer"),
        ("A4", None, "discard"),
    )
    assert all(step.volume.value == Decimal("100") for step in plan.transfer_steps)


def test_serial_plate_report_uses_existing_plan_without_recalculation() -> None:
    plan = plan_serial_plate(
        Concentration(Decimal("4"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE),
        DilutionFactor(Decimal("2")),
        SerialDilutionLayout(1, 2),
        "A",
        default_serial_plate_protocol(),
    )

    report = generate_serial_plate_report(plan)

    assert "Concentração inicial pré-inoculação: 8 µg/mL" in report
    assert "Concentração de trabalho necessária: 80 µg/mL" in report
    assert "Adicionar 20 µL da solução de trabalho e 180 µL de meio no primeiro poço da série." in report
    assert "Transferir 100 µL de A1 para A2 e homogeneizar." in report
    assert "Após homogeneizar A2, descartar 100 µL." in report
    assert "Adicionar 100 µL de inóculo a cada poço de teste." in report
    assert "A1: 4 µg/mL" in report
    assert "EQ-INOC-002" in report


def test_protocol_rejects_mismatched_remaining_and_preloaded_volumes() -> None:
    with pytest.raises(ProtocolConfigurationError, match="SERPROT-006"):
        SerialPlateProtocol(
            name="Inconsistente",
            first_well_initial_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
            antimicrobial_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE),
            first_well_medium_volume=Volume(Decimal("180"), VolumeUnit.MICROLITRE),
            serial_transfer_volume=Volume(Decimal("100"), VolumeUnit.MICROLITRE),
            preloaded_medium_volume=Volume(Decimal("50"), VolumeUnit.MICROLITRE),
            inoculum_volume=Volume(Decimal("100"), VolumeUnit.MICROLITRE),
        )
