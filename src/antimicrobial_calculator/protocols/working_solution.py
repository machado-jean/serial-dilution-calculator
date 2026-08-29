"""Protocol-level composition of inoculation and working-solution calculations."""

from dataclasses import dataclass

from antimicrobial_calculator.calculations import (
    FINAL_CONCENTRATION_EQUATION_ID,
    REQUIRED_PRE_INOCULATION_EQUATION_ID,
    calculate_required_pre_inoculation_concentration,
)
from antimicrobial_calculator.calculations.working_solution import (
    EQUATION_ID as WORKING_SOLUTION_EQUATION_ID,
    calculate_required_working_concentration,
)
from antimicrobial_calculator.domain.calculation_graph import CalculationGraph, CalculationStep
from antimicrobial_calculator.units import Concentration

from .microdilution import MicrodilutionProtocol


@dataclass(frozen=True, slots=True)
class WorkingSolutionRequirement:
    target_final_concentration: Concentration
    required_pre_inoculation_concentration: Concentration
    required_working_concentration: Concentration
    protocol: MicrodilutionProtocol
    calculation_graph: CalculationGraph


def calculate_working_solution_requirement(
    target_final_concentration: Concentration, protocol: MicrodilutionProtocol
) -> WorkingSolutionRequirement:
    """Build a traceable requirement from final target through working solution."""
    required_pre = calculate_required_pre_inoculation_concentration(
        target_final_concentration,
        protocol.pre_inoculation_volume,
        protocol.inoculum_volume,
    )
    required_working = calculate_required_working_concentration(
        required_pre,
        protocol.antimicrobial_volume,
        protocol.pre_inoculation_volume,
    )
    graph = CalculationGraph().with_step(
        CalculationStep(
            operation_id="required-pre-inoculation-concentration",
            classification="DERIVED",
            equation_id=REQUIRED_PRE_INOCULATION_EQUATION_ID,
            inputs=(
                f"concentração final: {target_final_concentration.value} {target_final_concentration.unit}",
                f"volume pré-inoculação: {protocol.pre_inoculation_volume.value} {protocol.pre_inoculation_volume.unit}",
                f"volume de inóculo: {protocol.inoculum_volume.value} {protocol.inoculum_volume.unit}",
            ),
            result=f"concentração pré-inoculação: {required_pre.value} {required_pre.unit}",
        )
    ).with_step(
        CalculationStep(
            operation_id="required-working-concentration",
            classification="DERIVED",
            equation_id=WORKING_SOLUTION_EQUATION_ID,
            inputs=(
                f"concentração pré-inoculação: {required_pre.value} {required_pre.unit}",
                f"volume antimicrobiano: {protocol.antimicrobial_volume.value} {protocol.antimicrobial_volume.unit}",
                f"volume pré-inoculação: {protocol.pre_inoculation_volume.value} {protocol.pre_inoculation_volume.unit}",
            ),
            result=f"concentração de trabalho: {required_working.value} {required_working.unit}",
        )
    )
    return WorkingSolutionRequirement(
        target_final_concentration,
        required_pre,
        required_working,
        protocol,
        graph,
    )
