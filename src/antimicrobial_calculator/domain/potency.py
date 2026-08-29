"""Active-material fraction used for potency-aware calculations."""

from dataclasses import dataclass
from decimal import Decimal


class PotencyValidationError(ValueError):
    """Raised when a potency fraction is not physically meaningful."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class Potency:
    """The active-material mass fraction of a powder, in the interval ``(0, 1]``."""

    active_fraction: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.active_fraction, Decimal):
            raise PotencyValidationError(
                "POT-001",
                "active_fraction must be decimal.Decimal; convert input explicitly before use",
            )
        if not self.active_fraction.is_finite():
            raise PotencyValidationError("POT-002", "active_fraction must be finite")
        if self.active_fraction <= Decimal("0"):
            raise PotencyValidationError(
                "POT-003", "active_fraction must be greater than zero"
            )
        if self.active_fraction > Decimal("1"):
            raise PotencyValidationError(
                "POT-004", "active_fraction cannot exceed one"
            )
