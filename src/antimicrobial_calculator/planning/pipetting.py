"""Operational evaluation of calculated transfer volumes."""

from dataclasses import dataclass
from enum import StrEnum

from antimicrobial_calculator.domain import PipetteConstraint
from antimicrobial_calculator.units import Volume, VolumeUnit


class PlanningInputError(ValueError):
    """Raised when a planning operation does not receive a valid domain input."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


class FeasibilityStatus(StrEnum):
    """Operational state of a transfer under the configured laboratory limits."""

    INFO = "INFO"
    CAUTION = "CAUTION"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class TransferFeasibility:
    """A traceable feasibility result for one transfer volume."""

    transfer_volume: Volume
    status: FeasibilityStatus
    message: str
    warnings: tuple[str, ...] = ()

    @property
    def is_feasible(self) -> bool:
        """Whether the configured limits permit the transfer."""
        return self.status is not FeasibilityStatus.INVALID


def evaluate_transfer_volume(
    transfer_volume: Volume, constraint: PipetteConstraint
) -> TransferFeasibility:
    """Evaluate a transfer against laboratory-specific pipette limits."""
    if not isinstance(transfer_volume, Volume):
        raise PlanningInputError(
            "PLAN-001", "transfer_volume must be a Volume with an explicit unit"
        )
    if not isinstance(constraint, PipetteConstraint):
        raise PlanningInputError(
            "PLAN-002", "constraint must be a PipetteConstraint"
        )

    transfer_microlitres = transfer_volume.to(VolumeUnit.MICROLITRE).value
    minimum_microlitres = constraint.minimum_reliable_volume.to(
        VolumeUnit.MICROLITRE
    ).value

    if transfer_microlitres < minimum_microlitres:
        return TransferFeasibility(
            transfer_volume=transfer_volume,
            status=FeasibilityStatus.INVALID,
            message="Volume de transferência abaixo do mínimo confiável configurado.",
            warnings=(
                "Avalie uma solução intermediária ou uma configuração de pipetagem diferente.",
            ),
        )

    if constraint.maximum_volume is not None:
        maximum_microlitres = constraint.maximum_volume.to(VolumeUnit.MICROLITRE).value
        if transfer_microlitres > maximum_microlitres:
            return TransferFeasibility(
                transfer_volume=transfer_volume,
                status=FeasibilityStatus.INVALID,
                message="Volume de transferência acima da capacidade máxima configurada.",
            )

    if transfer_microlitres == minimum_microlitres:
        return TransferFeasibility(
            transfer_volume=transfer_volume,
            status=FeasibilityStatus.CAUTION,
            message="Volume de transferência exatamente no mínimo confiável configurado.",
            warnings=(
                "A transferência é aceita pela configuração, mas está no limite operacional.",
            ),
        )

    warnings = ()
    if constraint.maximum_volume is None:
        warnings = (
            "A capacidade máxima não foi configurada e não foi avaliada.",
        )
    return TransferFeasibility(
        transfer_volume=transfer_volume,
        status=FeasibilityStatus.INFO,
        message="Volume de transferência aceito pela configuração laboratorial.",
        warnings=warnings,
    )
