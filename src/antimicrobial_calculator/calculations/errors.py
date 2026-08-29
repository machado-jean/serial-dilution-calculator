"""Explicit errors raised by scientific calculation operations."""


class CalculationInputError(ValueError):
    """Raised when calculation inputs are dimensionally or physically invalid."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")
