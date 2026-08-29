"""Laboratory-specific pipetting constraints."""

from dataclasses import dataclass
from decimal import Decimal

from antimicrobial_calculator.units import Volume, VolumeUnit


class LaboratoryConstraintError(ValueError):
    """Raised when a laboratory constraint is internally inconsistent."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class PipetteConstraint:
    """Configurable reliable minimum and optional maximum pipette volume."""

    minimum_reliable_volume: Volume
    maximum_volume: Volume | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.minimum_reliable_volume, Volume):
            raise LaboratoryConstraintError(
                "LAB-001",
                "minimum_reliable_volume must be a Volume with an explicit unit",
            )
        if self.maximum_volume is not None and not isinstance(self.maximum_volume, Volume):
            raise LaboratoryConstraintError(
                "LAB-002", "maximum_volume must be a Volume or None"
            )

        minimum_microlitres = self.minimum_reliable_volume.to(
            VolumeUnit.MICROLITRE
        ).value
        if minimum_microlitres <= Decimal("0"):
            raise LaboratoryConstraintError(
                "LAB-003", "minimum_reliable_volume must be greater than zero"
            )

        if self.maximum_volume is not None:
            maximum_microlitres = self.maximum_volume.to(VolumeUnit.MICROLITRE).value
            if maximum_microlitres < minimum_microlitres:
                raise LaboratoryConstraintError(
                    "LAB-004",
                    "maximum_volume cannot be below minimum_reliable_volume",
                )
