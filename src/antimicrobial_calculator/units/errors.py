"""Explicit validation errors for dimensional quantities."""


class QuantityValidationError(ValueError):
    """Raised when a dimensional quantity cannot be represented safely."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")
