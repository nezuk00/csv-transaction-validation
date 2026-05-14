class IntegratorError(Exception):
    """Base exception for the data integration system."""


class ValidationError(IntegratorError):
    """Raised when a row is structurally correct, but violates business rules."""


class InvalidTransactionError(IntegratorError):
    """Raised when a row cannot be parsed as a transaction at all."""


class SaveResultError(IntegratorError):
    """Raised when the processor cannot save the final JSON report."""
