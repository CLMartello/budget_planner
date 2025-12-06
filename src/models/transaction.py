
class Transaction:
	def __init__(self, amount: float, category: str, description: str = "", date=None):
		from datetime import datetime
		self.amount = float(amount)
		self.category = category
		self.description = description
		self.date = date if date else datetime.now()

	def __repr__(self):
		return f"<Transaction {self.amount} {self.category} on {self.fate}>"

