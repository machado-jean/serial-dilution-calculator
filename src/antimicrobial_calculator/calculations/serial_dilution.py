"""Derived mathematics for concentration dilution series."""

from decimal import Decimal

from antimicrobial_calculator.domain import DilutionFactor
from antimicrobial_calculator.units import Concentration

from .errors import CalculationInputError

EQUATION_ID = "EQ-SER-001"


def generate_serial_dilution_series(
    initial_concentration: Concentration,
    dilution_factor: DilutionFactor,
    number_of_concentrations: int,
) -> tuple[Concentration, ...]:
    """Generate concentrations using ``Cₙ = C₀ / factorⁿ`` from index zero."""
    _validate_inputs(initial_concentration, dilution_factor, number_of_concentrations)
    return tuple(
        Concentration(
            initial_concentration.value / (dilution_factor.value**index),
            initial_concentration.unit,
        )
        for index in range(number_of_concentrations)
    )


def _validate_inputs(
    initial_concentration: object,
    dilution_factor: object,
    number_of_concentrations: object,
) -> None:
    if not isinstance(initial_concentration, Concentration):
        raise CalculationInputError(
            "SER-004", "initial_concentration must be a Concentration with an explicit unit"
        )
    if not isinstance(dilution_factor, DilutionFactor):
        raise CalculationInputError(
            "SER-005", "dilution_factor must be a DilutionFactor"
        )
    if isinstance(number_of_concentrations, bool) or not isinstance(
        number_of_concentrations, int
    ):
        raise CalculationInputError(
            "SER-006", "number_of_concentrations must be an integer"
        )
    if initial_concentration.value <= Decimal("0"):
        raise CalculationInputError(
            "SER-007", "initial_concentration must be greater than zero"
        )
    if number_of_concentrations <= 0:
        raise CalculationInputError(
            "SER-008", "number_of_concentrations must be greater than zero"
        )
