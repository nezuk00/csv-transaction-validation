from pathlib import Path

import pytest

from integrator.exceptions import InvalidTransactionError
from integrator.reader import CsvTransactionReader


def test_reader_rejects_file_without_required_columns(tmp_path: Path) -> None:
    # Arrange
    csv_path = tmp_path / "broken.csv"
    csv_path.write_text("id,amount\n1,100\n", encoding="utf-8")
    reader = CsvTransactionReader()

    # Act + Assert
    with pytest.raises(InvalidTransactionError):
        list(reader.read(csv_path))


def test_reader_rejects_missing_file(tmp_path: Path) -> None:
    # Arrange
    missing_path = tmp_path / "missing.csv"
    reader = CsvTransactionReader()

    # Act + Assert
    with pytest.raises(InvalidTransactionError):
        list(reader.read(missing_path))
