"""Derived concentration requirements for antimicrobial working solutions."""

from antimicrobial_calculator.units import Concentration, VolumeUnit

from .errors import CalculationInputError

EQUATION_ID = "EQ-WORK-001"


def calculate_required_working_concentration(
    pre_inoculation_concentration: Concentration,
    antimicrobial_volume: object,
    pre_inoculation_volume: object,
) -> Concentration:
    """Calculate ``C_working = C_pre × V_pre / V_antimicrobial``."""
    from antimicrobial_calculator.units import Volume

    if not isinstance(pre_inoculation_concentration, Concentration):
        raise CalculationInputError(
            "WORK-001", "pre_inoculation_concentration must be a Concentration"
        )
    if not isinstance(antimicrobial_volume, Volume):
        raise CalculationInputError(
            "WORK-002", "antimicrobial_volume must be a Volume"
        )
    if not isinstance(pre_inoculation_volume, Volume):
        raise CalculationInputError(
            "WORK-003", "pre_inoculation_volume must be a Volume"
        )
    antimicrobial_microlitres = antimicrobial_volume.to(VolumeUnit.MICROLITRE).value
    pre_inoculation_microlitres = pre_inoculation_volume.to(VolumeUnit.MICROLITRE).value
    if pre_inoculation_concentration.value <= 0:
        raise CalculationInputError("WORK-004", "pre_inoculation_concentration must be greater than zero")
    if antimicrobial_microlitres <= 0:
        raise CalculationInputError("WORK-005", "antimicrobial_volume must be greater than zero")
    if pre_inoculation_microlitres <= 0:
        raise CalculationInputError("WORK-006", "pre_inoculation_volume must be greater than zero")
    return Concentration(
        pre_inoculation_concentration.value
        * pre_inoculation_microlitres
        / antimicrobial_microlitres,
        pre_inoculation_concentration.unit,
    )
