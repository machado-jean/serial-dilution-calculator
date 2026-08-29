"""Dimensionless factors for concentration dilution series."""

from dataclasses import dataclass
from decimal import Decimal


class DilutionFactorValidationError(ValueError):
    """Raised when a dilution factor cannot define a decreasing series."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class DilutionFactor:
    """A dimensionless divisor strictly greater than one."""

    value: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            raise DilutionFactorValidationError(
                "SER-001", "dilution factor must be decimal.Decimal"
            )
        if not self.value.is_finite():
            raise DilutionFactorValidationError(
                "SER-002", "dilution factor must be finite"
            )
        if self.value <= Decimal("1"):
            raise DilutionFactorValidationError(
                "SER-003", "dilution factor must be greater than one"
            )
