"""Tests for the physical, layout-independent 96-well plate model."""

import pytest

from antimicrobial_calculator.plates import Plate96, PlatePositionError, WellPosition


def test_plate96_exposes_standard_physical_geometry() -> None:
    plate = Plate96()

    assert plate.rows == tuple("ABCDEFGH")
    assert plate.columns == tuple(range(1, 13))
    assert plate.well_count == 96
    assert len(plate.wells) == 96


def test_plate96_returns_valid_positions_at_physical_boundaries() -> None:
    plate = Plate96()

    assert plate.well("A", 1).identifier == "A1"
    assert plate.well("H", 12).identifier == "H12"


def test_plate96_enumerates_positions_in_row_major_order() -> None:
    wells = Plate96().wells

    assert wells[0].identifier == "A1"
    assert wells[11].identifier == "A12"
    assert wells[12].identifier == "B1"
    assert wells[-1].identifier == "H12"


@pytest.mark.parametrize(
    ("row", "column", "error_code"),
    [
        ("I", 1, "PLATE-001"),
        ("a", 1, "PLATE-001"),
        ("A", 0, "PLATE-003"),
        ("A", 13, "PLATE-003"),
        ("A", 1.0, "PLATE-002"),
    ],
)
def test_well_position_rejects_coordinates_outside_the_plate(
    row: str, column: object, error_code: str
) -> None:
    with pytest.raises(PlatePositionError, match=error_code):
        WellPosition(row, column)  # type: ignore[arg-type]
