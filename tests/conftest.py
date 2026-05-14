import logging
from collections.abc import Callable
from pathlib import Path

import pytest

from integrator.processor import TransactionProcessor
from integrator.reader import CsvTransactionReader
from integrator.validator import TransactionValidator


@pytest.fixture
def valid_row() -> dict[str, str]:
    return {
        "transaction_id": "TRX-1001",
        "user_id": "USR-501",
        "amount": "100.50",
        "date": "2026-05-14",
        "category": "education",
    }


@pytest.fixture
def validator() -> TransactionValidator:
    return TransactionValidator()


@pytest.fixture
def processor_factory() -> Callable[[Path], TransactionProcessor]:
    def factory(log_path: Path) -> TransactionProcessor:
        logger = logging.getLogger(f"test-integrator-{log_path.name}")
        logger.setLevel(logging.INFO)
        return TransactionProcessor(
            reader=CsvTransactionReader(),
            validator=TransactionValidator(),
            logger=logger,
        )

    return factory
