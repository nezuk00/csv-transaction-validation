import json
import logging
from pathlib import Path

from integrator.exceptions import InvalidTransactionError, SaveResultError, ValidationError
from integrator.models import Transaction
from integrator.reader import CsvTransactionReader
from integrator.validator import TransactionValidator


class TransactionProcessor:
    """Coordinates reading, validating and saving clean transaction data."""

    def __init__(
        self,
        reader: CsvTransactionReader,
        validator: TransactionValidator,
        logger: logging.Logger | None = None,
    ) -> None:
        self.reader = reader
        self.validator = validator
        self.logger = logger or logging.getLogger(__name__)

    def process_file(self, input_path: Path, output_path: Path) -> list[Transaction]:
        valid_transactions: list[Transaction] = []

        try:
            rows = self.reader.read(input_path)
            for line_number, row in enumerate(rows, start=2):
                try:
                    transaction = self.validator.validate_raw(row)
                    valid_transactions.append(transaction)
                except (ValidationError, InvalidTransactionError) as exc:
                    self.logger.warning("Bad row %s skipped: %s", line_number, exc)
        except InvalidTransactionError as exc:
            self.logger.error("Input file processing failed: %s", exc)
            self._save_json([], output_path)
            return []

        self._save_json(valid_transactions, output_path)
        return valid_transactions

    def _save_json(self, transactions: list[Transaction], output_path: Path) -> None:
        payload = [transaction.to_dict() for transaction in transactions]

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            self.logger.error("Cannot save result.json: %s", exc)
            raise SaveResultError("Cannot save result.json") from exc
