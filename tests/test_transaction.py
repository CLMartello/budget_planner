
from models.transaction import Transaction

def test_transaction_creation():
	t = Transaction(100, "Salary", "January salary")
	assert t.amount == 100
	assert t.category == "Salary"

