"""Physical, layout-independent model of a 96-well plate."""

from dataclasses import dataclass
from typing import ClassVar


class PlatePositionError(ValueError):
    """Raised when a well coordinate is outside the physical plate geometry."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class WellPosition:
    """An immutable physical coordinate on a 96-well plate."""

    row: str
    column: int

    VALID_ROWS: ClassVar[tuple[str, ...]] = tuple("ABCDEFGH")
    MINIMUM_COLUMN: ClassVar[int] = 1
    MAXIMUM_COLUMN: ClassVar[int] = 12

    def __post_init__(self) -> None:
        if not isinstance(self.row, str) or self.row not in self.VALID_ROWS:
            raise PlatePositionError(
                "PLATE-001", "row must be one uppercase letter from A through H"
            )
        if isinstance(self.column, bool) or not isinstance(self.column, int):
            raise PlatePositionError("PLATE-002", "column must be an integer from 1 through 12")
        if not self.MINIMUM_COLUMN <= self.column <= self.MAXIMUM_COLUMN:
            raise PlatePositionError("PLATE-003", "column must be in the range 1 through 12")

    @property
    def identifier(self) -> str:
        """Return the conventional human-readable well identifier, such as ``A1``."""
        return f"{self.row}{self.column}"


@dataclass(frozen=True, slots=True)
class Plate96:
    """The physical geometry of an 8-row by 12-column plate."""

    rows: ClassVar[tuple[str, ...]] = WellPosition.VALID_ROWS
    columns: ClassVar[tuple[int, ...]] = tuple(range(1, 13))

    @property
    def well_count(self) -> int:
        """Return the number of physical well positions on this plate."""
        return len(self.rows) * len(self.columns)

    @property
    def wells(self) -> tuple[WellPosition, ...]:
        """Return all physical positions in row-major order."""
        return tuple(
            WellPosition(row, column) for row in self.rows for column in self.columns
        )

    def well(self, row: str, column: int) -> WellPosition:
        """Return one validated physical well position."""
        return WellPosition(row, column)
