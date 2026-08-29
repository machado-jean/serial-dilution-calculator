"""Canonical laboratory protocol for a physical serial dilution on a plate."""

from dataclasses import dataclass
from decimal import Decimal

from antimicrobial_calculator.calculations import (
    FINAL_CONCENTRATION_EQUATION_ID,
    REQUIRED_PRE_INOCULATION_EQUATION_ID,
    SERIAL_DILUTION_EQUATION_ID,
    WORKING_SOLUTION_EQUATION_ID,
    calculate_final_concentration_after_inoculation,
    calculate_required_pre_inoculation_concentration,
    calculate_required_working_concentration,
    generate_serial_dilution_series,
)
from antimicrobial_calculator.domain import CalculationGraph, CalculationStep, DilutionFactor
from antimicrobial_calculator.plates import (
    SerialDilutionLayout,
    WellConcentration,
    WellPosition,
    map_concentrations_to_plate_row,
)
from antimicrobial_calculator.units import Concentration, Volume, VolumeUnit

from .microdilution import ProtocolConfigurationError


@dataclass(frozen=True, slots=True)
class SerialPlateProtocol:
    """Configurable physical volumes for a serial dilution performed in wells."""

    name: str
    first_well_initial_volume: Volume
    antimicrobial_volume: Volume
    first_well_medium_volume: Volume
    serial_transfer_volume: Volume
    preloaded_medium_volume: Volume
    inoculum_volume: Volume

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ProtocolConfigurationError("SERPROT-001", "name must be a non-empty string")
        values = (
            self.first_well_initial_volume,
            self.antimicrobial_volume,
            self.first_well_medium_volume,
            self.serial_transfer_volume,
            self.preloaded_medium_volume,
            self.inoculum_volume,
        )
        if not all(isinstance(value, Volume) for value in values):
            raise ProtocolConfigurationError("SERPROT-002", "all protocol volumes must be Volume objects")
        if any(value.value <= Decimal("0") for value in values):
            raise ProtocolConfigurationError("SERPROT-003", "all protocol volumes must be greater than zero")
        if self.serial_transfer_volume.to(VolumeUnit.MICROLITRE).value >= self.first_well_initial_volume.to(VolumeUnit.MICROLITRE).value:
            raise ProtocolConfigurationError(
                "SERPROT-004", "serial_transfer_volume must be smaller than first_well_initial_volume"
            )
        first_well_preparation_microlitres = (
            self.antimicrobial_volume.to(VolumeUnit.MICROLITRE).value
            + self.first_well_medium_volume.to(VolumeUnit.MICROLITRE).value
        )
        if first_well_preparation_microlitres != self.first_well_initial_volume.to(VolumeUnit.MICROLITRE).value:
            raise ProtocolConfigurationError(
                "SERPROT-005",
                "antimicrobial_volume plus first_well_medium_volume must equal first_well_initial_volume",
            )
        if self.remaining_pre_inoculation_volume.to(VolumeUnit.MICROLITRE).value != self.preloaded_medium_volume.to(VolumeUnit.MICROLITRE).value:
            raise ProtocolConfigurationError(
                "SERPROT-006",
                "preloaded_medium_volume must equal the volume remaining after transfer",
            )

    @property
    def remaining_pre_inoculation_volume(self) -> Volume:
        first_microlitres = self.first_well_initial_volume.to(VolumeUnit.MICROLITRE).value
        transfer_microlitres = self.serial_transfer_volume.to(VolumeUnit.MICROLITRE).value
        return Volume(first_microlitres - transfer_microlitres, VolumeUnit.MICROLITRE).to(
            self.first_well_initial_volume.unit
        )

    @property
    def final_well_volume(self) -> Volume:
        total_microlitres = (
            self.remaining_pre_inoculation_volume.to(VolumeUnit.MICROLITRE).value
            + self.inoculum_volume.to(VolumeUnit.MICROLITRE).value
        )
        return Volume(total_microlitres, VolumeUnit.MICROLITRE).to(
            self.first_well_initial_volume.unit
        )


def default_serial_plate_protocol() -> SerialPlateProtocol:
    """Return the editable canonical preset for the described physical workflow."""
    return SerialPlateProtocol(
        name="Default Laboratory Serial Plate",
        first_well_initial_volume=Volume(Decimal("200"), VolumeUnit.MICROLITRE),
        antimicrobial_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE),
        first_well_medium_volume=Volume(Decimal("180"), VolumeUnit.MICROLITRE),
        serial_transfer_volume=Volume(Decimal("100"), VolumeUnit.MICROLITRE),
        preloaded_medium_volume=Volume(Decimal("100"), VolumeUnit.MICROLITRE),
        inoculum_volume=Volume(Decimal("100"), VolumeUnit.MICROLITRE),
    )


@dataclass(frozen=True, slots=True)
class SerialTransferStep:
    source: WellPosition
    destination: WellPosition | None
    volume: Volume
    action: str


@dataclass(frozen=True, slots=True)
class SerialPlatePlan:
    protocol: SerialPlateProtocol
    initial_final_target: Concentration
    initial_pre_inoculation_concentration: Concentration
    required_working_concentration: Concentration
    pre_inoculation_map: tuple[WellConcentration, ...]
    final_concentration_map: tuple[WellConcentration, ...]
    preloaded_medium_wells: tuple[WellPosition, ...]
    transfer_steps: tuple[SerialTransferStep, ...]
    calculation_graph: CalculationGraph


def plan_serial_plate(
    initial_final_target: Concentration,
    dilution_factor: DilutionFactor,
    layout: SerialDilutionLayout,
    row: str,
    protocol: SerialPlateProtocol,
) -> SerialPlatePlan:
    """Build concentrations and physical transfer instructions for one plate row."""
    if not isinstance(protocol, SerialPlateProtocol):
        raise ProtocolConfigurationError("SERPROT-007", "protocol must be a SerialPlateProtocol")
    initial_pre = calculate_required_pre_inoculation_concentration(
        initial_final_target,
        protocol.remaining_pre_inoculation_volume,
        protocol.inoculum_volume,
    )
    required_working = calculate_required_working_concentration(
        initial_pre,
        protocol.antimicrobial_volume,
        protocol.first_well_initial_volume,
    )
    pre_series = generate_serial_dilution_series(
        initial_pre, dilution_factor, layout.number_of_columns
    )
    final_series = tuple(
        calculate_final_concentration_after_inoculation(
            concentration,
            protocol.remaining_pre_inoculation_volume,
            protocol.inoculum_volume,
        )
        for concentration in pre_series
    )
    pre_map = map_concentrations_to_plate_row(pre_series, layout, row)
    final_map = map_concentrations_to_plate_row(final_series, layout, row)
    positions = tuple(item.position for item in pre_map)
    transfers = tuple(
        SerialTransferStep(positions[index], positions[index + 1], protocol.serial_transfer_volume, "transfer")
        for index in range(len(positions) - 1)
    ) + (
        SerialTransferStep(positions[-1], None, protocol.serial_transfer_volume, "discard"),
    )
    graph = CalculationGraph().with_step(
        CalculationStep(
            operation_id="initial-pre-inoculation-concentration",
            classification="DERIVED",
            equation_id=REQUIRED_PRE_INOCULATION_EQUATION_ID,
            inputs=(
                f"concentração final inicial: {initial_final_target.value} {initial_final_target.unit}",
                f"volume restante antes da inoculação: {protocol.remaining_pre_inoculation_volume.value} {protocol.remaining_pre_inoculation_volume.unit}",
                f"volume de inóculo: {protocol.inoculum_volume.value} {protocol.inoculum_volume.unit}",
            ),
            result=f"concentração inicial pré-inoculação: {initial_pre.value} {initial_pre.unit}",
        )
    ).with_step(
        CalculationStep(
            operation_id="initial-working-solution-concentration",
            classification="DERIVED",
            equation_id=WORKING_SOLUTION_EQUATION_ID,
            inputs=(
                f"concentração inicial pré-inoculação: {initial_pre.value} {initial_pre.unit}",
                f"volume de solução antimicrobiana: {protocol.antimicrobial_volume.value} {protocol.antimicrobial_volume.unit}",
                f"volume inicial no primeiro poço: {protocol.first_well_initial_volume.value} {protocol.first_well_initial_volume.unit}",
            ),
            result=f"concentração de trabalho necessária: {required_working.value} {required_working.unit}",
        )
    ).with_step(
        CalculationStep(
            operation_id="serial-plate-transfer-configuration",
            classification="LAB-CONSTRAINT",
            equation_id=None,
            inputs=(
                f"volume inicial no primeiro poço: {protocol.first_well_initial_volume.value} {protocol.first_well_initial_volume.unit}",
                f"solução antimicrobiana no primeiro poço: {protocol.antimicrobial_volume.value} {protocol.antimicrobial_volume.unit}",
                f"meio no primeiro poço: {protocol.first_well_medium_volume.value} {protocol.first_well_medium_volume.unit}",
                f"transferência seriada: {protocol.serial_transfer_volume.value} {protocol.serial_transfer_volume.unit}",
                f"meio pré-carregado: {protocol.preloaded_medium_volume.value} {protocol.preloaded_medium_volume.unit}",
            ),
            result="Cada poço de teste fica com o volume pré-inoculação configurado antes da adição do inóculo.",
            warnings=("O último poço requer descarte do volume de transferência após a mistura.",),
        )
    ).with_step(
        CalculationStep(
            operation_id="final-concentration-series",
            classification="DERIVED",
            equation_id=FINAL_CONCENTRATION_EQUATION_ID,
            inputs=(f"fator de diluição: {dilution_factor.value}",),
            result="Concentrações finais mapeadas para os poços selecionados.",
        )
    )
    return SerialPlatePlan(
        protocol,
        initial_final_target,
        initial_pre,
        required_working,
        pre_map,
        final_map,
        positions[1:],
        transfers,
        graph,
    )
