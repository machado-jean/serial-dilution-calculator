"""Formatting of validated calculation results; no scientific calculations occur here."""

from antimicrobial_calculator.domain import CalculationGraph
from antimicrobial_calculator.plates import WellConcentration
from antimicrobial_calculator.protocols.serial_plate import SerialPlatePlan
from antimicrobial_calculator.protocols.working_solution import WorkingSolutionRequirement


def generate_technical_report(
    calculation_graph: CalculationGraph,
    plate_map: tuple[WellConcentration, ...] = (),
) -> str:
    """Format a technical trace and optional plate map from supplied results."""
    if not isinstance(calculation_graph, CalculationGraph):
        raise TypeError("calculation_graph must be a CalculationGraph")
    lines = ["# Relatório Técnico", "", "## Trilhas de cálculo", ""]
    for step in calculation_graph.steps:
        equation = step.equation_id or "Sem equação"
        lines.extend(
            [
                f"### {step.operation_id}",
                f"Classificação: {step.classification}",
                f"Equação: {equation}",
                *step.inputs,
                f"Resultado: {step.result}",
            ]
        )
        if step.warnings:
            lines.append("Avisos: " + "; ".join(step.warnings))
        lines.append("")
    if plate_map:
        lines.extend(["## Mapa de concentrações", ""])
        lines.extend(
            f"- {item.position.identifier}: {item.concentration.value} {item.concentration.unit}"
            for item in plate_map
        )
    return "\n".join(lines)


def generate_working_solution_report(
    requirement: WorkingSolutionRequirement,
    plate_map: tuple[WellConcentration, ...] = (),
) -> str:
    """Format a report from an existing working-solution requirement only."""
    if not isinstance(requirement, WorkingSolutionRequirement):
        raise TypeError("requirement must be a WorkingSolutionRequirement")
    summary = "\n".join(
        [
            "# Resumo Técnico",
            "",
            f"Protocolo: {requirement.protocol.name}",
            (
                "Concentração final-alvo: "
                f"{requirement.target_final_concentration.value} "
                f"{requirement.target_final_concentration.unit}"
            ),
            (
                "Concentração pré-inoculação requerida: "
                f"{requirement.required_pre_inoculation_concentration.value} "
                f"{requirement.required_pre_inoculation_concentration.unit}"
            ),
            (
                "Concentração de trabalho requerida: "
                f"{requirement.required_working_concentration.value} "
                f"{requirement.required_working_concentration.unit}"
            ),
            "",
            "## Instruções de preparo configuradas",
            "",
            (
                "Para o preparo pré-inoculação, combinar "
                f"{requirement.protocol.antimicrobial_volume.value} "
                f"{requirement.protocol.antimicrobial_volume.unit} da solução de trabalho "
                f"com {requirement.protocol.medium_volume.value} "
                f"{requirement.protocol.medium_volume.unit} de meio."
            ),
            (
                "Adicionar "
                f"{requirement.protocol.inoculum_volume.value} "
                f"{requirement.protocol.inoculum_volume.unit} de inóculo ao volume pré-inoculação "
                "conforme a configuração do protocolo."
            ),
            "",
        ]
    )
    return summary + generate_technical_report(requirement.calculation_graph, plate_map)


def generate_serial_plate_report(plan: SerialPlatePlan) -> str:
    """Format an existing serial-plate plan without recalculating its values."""
    if not isinstance(plan, SerialPlatePlan):
        raise TypeError("plan must be a SerialPlatePlan")
    lines = [
        "# Resumo Técnico",
        "",
        f"Protocolo: {plan.protocol.name}",
        (
            "Concentração final-alvo no primeiro poço: "
            f"{plan.initial_final_target.value} {plan.initial_final_target.unit}"
        ),
        (
            "Concentração inicial pré-inoculação: "
            f"{plan.initial_pre_inoculation_concentration.value} "
            f"{plan.initial_pre_inoculation_concentration.unit}"
        ),
        (
            "Concentração de trabalho necessária: "
            f"{plan.required_working_concentration.value} "
            f"{plan.required_working_concentration.unit}"
        ),
        "",
        "## Instruções físicas configuradas",
        "",
        (
            f"Adicionar {plan.protocol.antimicrobial_volume.value} "
            f"{plan.protocol.antimicrobial_volume.unit} da solução de trabalho e "
            f"{plan.protocol.first_well_medium_volume.value} "
            f"{plan.protocol.first_well_medium_volume.unit} de meio no primeiro poço da série."
        ),
        (
            f"Pré-carregar {plan.protocol.preloaded_medium_volume.value} "
            f"{plan.protocol.preloaded_medium_volume.unit} de meio em cada poço subsequente da série."
        ),
    ]
    for step in plan.transfer_steps:
        if step.destination is None:
            lines.append(
                f"Após homogeneizar {step.source.identifier}, descartar "
                f"{step.volume.value} {step.volume.unit}."
            )
        else:
            lines.append(
                f"Transferir {step.volume.value} {step.volume.unit} de "
                f"{step.source.identifier} para {step.destination.identifier} e homogeneizar."
            )
    lines.extend(
        [
            (
                f"Adicionar {plan.protocol.inoculum_volume.value} "
                f"{plan.protocol.inoculum_volume.unit} de inóculo a cada poço de teste."
            ),
            "",
        ]
    )
    return "\n".join(lines) + generate_technical_report(
        plan.calculation_graph, plan.final_concentration_map
    )
