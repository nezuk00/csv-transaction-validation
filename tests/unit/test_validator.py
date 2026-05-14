from decimal import Decimal

import pytest

from integrator.exceptions import InvalidTransactionError, ValidationError
from integrator.validator import MAX_AMOUNT, MIN_AMOUNT, TransactionValidator


@pytest.mark.parametrize(
    ("overrides", "expected_valid"),
    [
        ({"amount": "0.01"}, True),
        ({"amount": "0"}, False),
        ({"amount": "-1"}, False),
        ({"amount": "abc"}, False),
        ({"amount": str(MAX_AMOUNT)}, True),
        ({"amount": str(MAX_AMOUNT + Decimal("0.01"))}, False),
        ({"date": "2026-02-30"}, False),
        ({"date": "14-05-2026"}, False),
        ({"transaction_id": "1001"}, False),
        ({"transaction_id": ""}, False),
        ({"user_id": "501"}, False),
        ({"category": ""}, False),
    ],
)
def test_validator_boundaries_parametrized(
    validator: TransactionValidator,
    valid_row: dict[str, str],
    overrides: dict[str, str],
    expected_valid: bool,
) -> None:
    # Arrange
    row = valid_row | overrides

    # Act + Assert
    if expected_valid:
        transaction = validator.validate_raw(row)
        assert transaction.amount >= MIN_AMOUNT
    else:
        with pytest.raises(ValidationError):
            validator.validate_raw(row)


def test_garbage_row_raises_domain_error_not_index_error(
    validator: TransactionValidator,
) -> None:
    # Arrange
    garbage_row = {"broken": "data"}

    # Act + Assert
    with pytest.raises(InvalidTransactionError):
        validator.validate_raw(garbage_row)
