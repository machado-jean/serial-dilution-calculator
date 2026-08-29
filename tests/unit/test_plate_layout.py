"""Tests for mapping existing concentration values to plate positions."""

from decimal import Decimal

import pytest

from antimicrobial_calculator.plates import (
    PlateLayoutError,
    SerialDilutionLayout,
    map_concentrations_to_plate_row,
)
from antimicrobial_calculator.units import Concentration, ConcentrationUnit


CONCENTRATIONS = tuple(
    Concentration(value, ConcentrationUnit.MICROGRAM_PER_MILLILITRE)
    for value in (Decimal("8"), Decimal("4"), Decimal("2"), Decimal("1"))
)


def test_layout_maps_each_existing_value_to_configured_columns() -> None:
    mapped = map_concentrations_to_plate_row(
        CONCENTRATIONS, SerialDilutionLayout(start_column=3, number_of_columns=4), "B"
    )

    assert tuple(item.position.identifier for item in mapped) == ("B3", "B4", "B5", "B6")
    assert tuple(item.concentration.value for item in mapped) == tuple(
        item.value for item in CONCENTRATIONS
    )


def test_layout_rejects_columns_that_do_not_fit_plate96() -> None:
    with pytest.raises(PlateLayoutError, match="LAYOUT-005"):
        SerialDilutionLayout(start_column=10, number_of_columns=4)


def test_layout_rejects_series_with_wrong_number_of_positions() -> None:
    with pytest.raises(PlateLayoutError, match="LAYOUT-008"):
        map_concentrations_to_plate_row(
            CONCENTRATIONS[:3], SerialDilutionLayout(start_column=1, number_of_columns=4), "A"
        )
