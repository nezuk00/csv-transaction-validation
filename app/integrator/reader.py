import csv
from collections.abc import Iterator
from pathlib import Path

from integrator.exceptions import InvalidTransactionError

REQUIRED_COLUMNS = {"transaction_id", "user_id", "amount", "date", "category"}


class CsvTransactionReader:
    """Reads raw transaction rows from a CSV file."""

    def read(self, path: Path) -> Iterator[dict[str, str]]:
        try:
            with path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None:
                    raise InvalidTransactionError("CSV file has no header")

                missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
                if missing_columns:
                    columns = ", ".join(sorted(missing_columns))
                    raise InvalidTransactionError(f"CSV file misses columns: {columns}")

                yield from reader
        except OSError as exc:
            raise InvalidTransactionError(f"Cannot read input file: {path}") from exc
