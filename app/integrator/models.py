from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    user_id: str
    amount: Decimal
    date: datetime
    category: str

    def to_dict(self) -> dict[str, str]:
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": str(self.amount),
            "date": self.date.date().isoformat(),
            "category": self.category,
        }
