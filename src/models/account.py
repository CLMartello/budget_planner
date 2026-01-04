
from .transaction import Transaction

class Account:
	def __init__(self, name: str):
		self.name = name
		self.transactions: list[Transaction] = []
		self.logs = []

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
		self.log_action("edit_transaction", last)
		last.amount = amount
		last.category = category
		last.description = description

	def log_action(self, action, transaction):
		self.logs.append({
			"action": action,
			"transaction": transaction.to_dict() if transaction else None,
			"timestamp": datetime.now().isoformat()
		})

	def to_dict(self) -> dict:
		return {
			"name": self.name,
			"transactions": [t.to_dict() for t in self.transactions]
			"logs": self.logs
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

