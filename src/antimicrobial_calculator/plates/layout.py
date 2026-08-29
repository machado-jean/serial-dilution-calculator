"""Configurable mapping of already-calculated concentrations to plate wells."""

from dataclasses import dataclass

from antimicrobial_calculator.units import Concentration

from .plate96 import Plate96, PlatePositionError, WellPosition


class PlateLayoutError(ValueError):
    """Raised when a linear layout does not fit the plate or supplied series."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class SerialDilutionLayout:
    start_column: int
    number_of_columns: int

    def __post_init__(self) -> None:
        if isinstance(self.start_column, bool) or not isinstance(self.start_column, int):
            raise PlateLayoutError("LAYOUT-001", "start_column must be an integer")
        if isinstance(self.number_of_columns, bool) or not isinstance(self.number_of_columns, int):
            raise PlateLayoutError("LAYOUT-002", "number_of_columns must be an integer")
        if self.start_column < 1:
            raise PlateLayoutError("LAYOUT-003", "start_column must be at least one")
        if self.number_of_columns <= 0:
            raise PlateLayoutError("LAYOUT-004", "number_of_columns must be greater than zero")
        if self.end_column > Plate96.columns[-1]:
            raise PlateLayoutError("LAYOUT-005", "layout exceeds the physical plate columns")

    @property
    def end_column(self) -> int:
        return self.start_column + self.number_of_columns - 1


@dataclass(frozen=True, slots=True)
class WellConcentration:
    position: WellPosition
    concentration: Concentration


def map_concentrations_to_plate_row(
    concentrations: tuple[Concentration, ...],
    layout: SerialDilutionLayout,
    row: str,
    plate: Plate96 | None = None,
) -> tuple[WellConcentration, ...]:
    """Map values without recalculation to successive wells of one physical row."""
    active_plate = plate or Plate96()
    if not isinstance(active_plate, Plate96):
        raise PlateLayoutError("LAYOUT-006", "plate must be a Plate96")
    try:
        active_plate.well(row, layout.start_column)
    except PlatePositionError as error:
        raise PlateLayoutError("LAYOUT-007", "row must be valid for Plate96") from error
    if len(concentrations) != layout.number_of_columns:
        raise PlateLayoutError(
            "LAYOUT-008", "number of concentrations must equal layout number_of_columns"
        )
    if not all(isinstance(item, Concentration) for item in concentrations):
        raise PlateLayoutError("LAYOUT-009", "concentrations must contain only Concentration objects")
    return tuple(
        WellConcentration(active_plate.well(row, layout.start_column + index), concentration)
        for index, concentration in enumerate(concentrations)
    )
