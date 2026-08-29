"""Foundation-level checks for the package layout."""


def test_package_can_be_imported() -> None:
    import antimicrobial_calculator

    assert antimicrobial_calculator.__doc__ is not None
