
from .transaction import Transaction

class Account:
	def __init__(self, name: str):
		self.name = name
		self.transactions: list[Transaction] = []

	def add_transaction(self, transaction: Transaction):
		self.transactions.append(transaction)

	def balance(self):
		return sum(t.amount for t in self.transactions)

	def history(self):
		return self.transactions

	def edit_last_transaction(self, amount, category, description):
		if not self.transactions:
			raise ValueError("No transactions to edit.")

		last = self.transactions[-1]
		last.amount = amount
		last.category = category
		last.description = description

	def to_dict(self) -> dict:
		return {
			"name": self.name,
			"transactions": [t.to_dict() for t in self.transactions]
		}

	@classmethod
	def from_dict(cls, data: dict):
		from .transaction import Transaction
		account = cls(data["name"])
		account.transactions = [
			Transaction.from_dict(t)
			for t in data.get("transactions", [])
		]
		return account

