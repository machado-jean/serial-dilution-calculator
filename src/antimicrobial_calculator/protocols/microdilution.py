"""Configurable laboratory protocol volumes for microdilution preparation."""

from dataclasses import dataclass
from decimal import Decimal

from antimicrobial_calculator.units import Volume, VolumeUnit


class ProtocolConfigurationError(ValueError):
    """Raised when a laboratory protocol configuration is invalid."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class MicrodilutionProtocol:
    """Configurable preparation and inoculation volumes for one protocol."""

    name: str
    antimicrobial_volume: Volume
    medium_volume: Volume
    inoculum_volume: Volume

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ProtocolConfigurationError("PROT-001", "name must be a non-empty string")
        for field_name, value in (
            ("antimicrobial_volume", self.antimicrobial_volume),
            ("medium_volume", self.medium_volume),
            ("inoculum_volume", self.inoculum_volume),
        ):
            if not isinstance(value, Volume):
                raise ProtocolConfigurationError(
                    "PROT-002", f"{field_name} must be a Volume with an explicit unit"
                )
            if value.value <= Decimal("0"):
                raise ProtocolConfigurationError(
                    "PROT-003", f"{field_name} must be greater than zero"
                )

    @property
    def pre_inoculation_volume(self) -> Volume:
        """Return antimicrobial plus medium volume in antimicrobial-volume units."""
        total_microlitres = (
            self.antimicrobial_volume.to(VolumeUnit.MICROLITRE).value
            + self.medium_volume.to(VolumeUnit.MICROLITRE).value
        )
        return Volume(total_microlitres, VolumeUnit.MICROLITRE).to(
            self.antimicrobial_volume.unit
        )


def default_laboratory_microdilution_protocol() -> MicrodilutionProtocol:
    """Return the editable initial laboratory preset, not a universal method."""
    return MicrodilutionProtocol(
        name="Default Laboratory Microdilution",
        antimicrobial_volume=Volume(Decimal("20"), VolumeUnit.MICROLITRE),
        medium_volume=Volume(Decimal("180"), VolumeUnit.MICROLITRE),
        inoculum_volume=Volume(Decimal("100"), VolumeUnit.MICROLITRE),
    )
