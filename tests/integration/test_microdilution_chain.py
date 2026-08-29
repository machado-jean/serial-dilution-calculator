"""End-to-end scientific chain from final target to mapped plate concentrations."""

from decimal import Decimal

from antimicrobial_calculator.calculations import generate_serial_dilution_series
from antimicrobial_calculator.domain import DilutionFactor
from antimicrobial_calculator.plates import SerialDilutionLayout, map_concentrations_to_plate_row
from antimicrobial_calculator.protocols import (
    calculate_working_solution_requirement,
    default_laboratory_microdilution_protocol,
)
from antimicrobial_calculator.reporting import generate_working_solution_report
from antimicrobial_calculator.units import Concentration, ConcentrationUnit


def test_final_target_to_working_solution_to_plate_map_chain() -> None:
    target = Concentration(Decimal("4"), ConcentrationUnit.MICROGRAM_PER_MILLILITRE)
    requirement = calculate_working_solution_requirement(
        target, default_laboratory_microdilution_protocol()
    )
    series = generate_serial_dilution_series(target, DilutionFactor(Decimal("2")), 4)
    plate_map = map_concentrations_to_plate_row(
        series, SerialDilutionLayout(1, 4), "A"
    )

    report = generate_working_solution_report(requirement, plate_map)

    assert requirement.required_working_concentration.value == Decimal("60")
    assert tuple(item.position.identifier for item in plate_map) == ("A1", "A2", "A3", "A4")
    assert "EQ-INOC-002" in report
    assert "EQ-WORK-001" in report
    assert "A1: 4 µg/mL" in report
    assert "Concentração de trabalho requerida: 60.0 µg/mL" in report
    assert "20 µL da solução de trabalho com 180 µL de meio" in report
