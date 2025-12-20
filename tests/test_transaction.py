
from models.transaction import Transaction

def test_transaction_creation():
	t = Transaction(100, "Salary", "January salary")
	assert t.amount == 100
	assert t.category == "Salary"

def test_transaction_repr():
	t = Transaction(-50, "Food")
	text = repr(t)
	assert "Food" in text
	assert "-50" in text

def test_transaction_serialization():
	t = Transaction(200, "Bonus", "Year end")
	data = t.to_dict()

	restored = Transaction.from_dict(data)

	assert restored.amount == 200
	assert restored.category == "Bonus"
	assert restored.description == "Year end"

