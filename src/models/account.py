
from .transaction import Transaction

class Account:
	def __init__(self, name: str):
		self.name = name
		self.transactions: list[Transaction] = []

	def add_transaction(self, transaction: Transaction):
		self.transactions.append(transaction)

	def get_balance(self) -> float:
		return sum(t.amount for t in self.transactions)
