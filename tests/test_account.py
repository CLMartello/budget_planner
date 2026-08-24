
from models.account import Account
from models.transaction import Transaction

def test_account_creation():
	acc = Account("Personal")
	assert acc.name == "Personal"
	assert acc.transactions == []

def test_add_transaction():
	acc = Account("Personal")
	acc.add_transaction(Transaction(100, "Salary"))
	acc.add_transaction(Transaction(-30, "Food"))

	assert len(acc.transactions) == 2

def test_account_balance():
	acc = Account("Personal")
	acc.add_transaction(Transaction(100, "Salary"))
	acc.add_transaction(Transaction(-40, "Food"))

	assert acc.get_balance() == 60

def test_account_serialization():
	acc = Account("Savings")
	acc.add_transaction(Transaction(500, "Deposit"))

	data = acc.to_dict()
	restored = Account.from_dict(data)

	assert restored.name == "Savings"
	assert restored.get_balance() == 500

def test_account_logs_serialization():
	account = Account("Personal")
	account.add_transaction(Transaction(100, "Salary"))
	account.edit_last_transaction(150, "Bonus", "Updated income")

	data = account.to_dict()
	restored = Account.from_dict(data)

	assert restored.logs == account.logs

