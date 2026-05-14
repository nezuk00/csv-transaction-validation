from datetime import datetime
from decimal import Decimal, InvalidOperation

from integrator.exceptions import InvalidTransactionError, ValidationError
from integrator.models import Transaction

MAX_AMOUNT = Decimal("1000000000000.00")
MIN_AMOUNT = Decimal("0.01")


class TransactionValidator:
    """Validates raw CSV rows and converts them to domain Transaction objects."""

    def validate_raw(self, row: dict[str, str]) -> Transaction:
        try:
            transaction_id = row["transaction_id"].strip()
            user_id = row["user_id"].strip()
            amount_raw = row["amount"].strip()
            date_raw = row["date"].strip()
            category = row["category"].strip()
        except (KeyError, AttributeError) as exc:
            raise InvalidTransactionError("Malformed transaction row") from exc

        if not transaction_id.startswith("TRX-"):
            raise ValidationError("Transaction ID must start with TRX-")

        if not user_id.startswith("USR-"):
            raise ValidationError("User ID must start with USR-")

        try:
            amount = Decimal(amount_raw)
        except (InvalidOperation, TypeError) as exc:
            raise ValidationError("Amount must be a decimal number") from exc

        if amount < MIN_AMOUNT:
            raise ValidationError("Amount must be at least 0.01")

        if amount > MAX_AMOUNT:
            raise ValidationError("Amount is too large")

        try:
            parsed_date = datetime.strptime(date_raw, "%Y-%m-%d")
        except ValueError as exc:
            raise ValidationError("Date must have YYYY-MM-DD format") from exc

        if not category:
            raise ValidationError("Category cannot be empty")

        return Transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            amount=amount,
            date=parsed_date,
            category=category,
        )
