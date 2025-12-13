
class Transaction:
	def __init__(self, amount: float, category: str, description: str = "", date=None):
		from datetime import datetime
		self.amount = float(amount)
		self.category = category
		self.description = description
		self.date = date if date else datetime.now()

	def __repr__(self):
		return f"<Transaction {self.amount} {self.category} on {self.fate}>"

	def to_dict(self) -> dict:
		return {
			"amount": self.amount,
			"category": self.category,
			"description": self.description,
			"date": self.date.isoformat()
		}

	@classmethod
	def from_dict(cls, data: dict):
		from datetime import datetime
		return cls(
			amount=data["amount"],
			category=data["category"],
			description=data.get("description", ""),
			date=datetime.fromisoformat(data["date"])
		)

