import json
import logging
from pathlib import Path
from unittest.mock import patch

import pytest

from integrator.exceptions import SaveResultError
from integrator.processor import TransactionProcessor

CSV_HEADER = "transaction_id,user_id,amount,date,category\n"


def test_processor_saves_only_valid_rows(
    tmp_path: Path,
    processor_factory,
) -> None:
    # Arrange
    input_path = tmp_path / "transactions.csv"
    output_path = tmp_path / "result.json"
    input_path.write_text(
        CSV_HEADER
        + "TRX-1,USR-1,0.01,2026-05-14,food\n"
        + "TRX-2,USR-2,0,2026-05-14,food\n"
        + "BAD-ID,USR-3,10.00,wrong-date,transport\n",
        encoding="utf-8",
    )
    processor = processor_factory(tmp_path)

    # Act
    result = processor.process_file(input_path, output_path)

    # Assert
    saved_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(result) == 1
    assert len(saved_payload) == 1
    assert saved_payload[0]["transaction_id"] == "TRX-1"


def test_processor_logs_save_error_when_disk_is_read_only(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    processor_factory,
) -> None:
    # Arrange
    input_path = tmp_path / "transactions.csv"
    output_path = tmp_path / "result.json"
    input_path.write_text(
        CSV_HEADER + "TRX-1,USR-1,10.00,2026-05-14,food\n",
        encoding="utf-8",
    )
    processor: TransactionProcessor = processor_factory(tmp_path)
    caplog.set_level(logging.ERROR)

    # Act + Assert
    with patch("pathlib.Path.write_text", side_effect=PermissionError("read-only disk")):
        with pytest.raises(SaveResultError):
            processor.process_file(input_path, output_path)

    assert "Cannot save result.json" in caplog.text


def test_processor_returns_empty_list_when_input_file_is_broken(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    processor_factory,
) -> None:
    # Arrange
    input_path = tmp_path / "broken.csv"
    output_path = tmp_path / "result.json"
    input_path.write_text("bad_header\nvalue\n", encoding="utf-8")
    processor: TransactionProcessor = processor_factory(tmp_path)
    caplog.set_level(logging.ERROR)

    # Act
    result = processor.process_file(input_path, output_path)

    # Assert
    assert result == []
    assert json.loads(output_path.read_text(encoding="utf-8")) == []
    assert "Input file processing failed" in caplog.text
