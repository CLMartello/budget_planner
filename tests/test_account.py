
from models.account import Account
from models.transaction import Transaction
from datetime import datetime
import pytest

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

def test_first_semester_balance():
	account = Account("Personal")

	account.add_transaction(
		Transaction(
			1000,
			"Salary",
			date=datetime(2026, 1, 15)
		)
	)
	account.add_transaction(
		Transaction(
			-200,
			"Food",
			date=datetime(2026, 3, 10)
		)
	)
	account.add_transaction(
		Transaction(
			500,
			"Bonus",
			date=datetime(2026, 7, 1)
		)
	)

	balance = account.get_semester_balance(2026, 1)

	assert balance == 800

def test_second_semester_balance():
	account = Account("Personal")

	account.add_transaction(
		Transaction(
			100,
			"June income",
			date=datetime(2026, 6, 30)
		)
	)
	account.add_transaction(
		Transaction(
			500,
			"July income",
			date=datetime(2026, 7, 1)
		)
	)
	account.add_transaction(
		Transaction(
			-100,
			"December expense",
			date=datetime(2026, 12, 31)
		)
	)
	account.add_transaction(
		Transaction(
			2000,
			"Previous year",
			date=datetime(2025, 7, 1)
		)
	)

	balance = account.get_semester_balance(2026, 2)

	assert balance == 400

def test_invalid_semester():
	account = Account("Personal")

	with pytest.raises(
		ValueError,
		match="Semester must be 1 or 2"
	):
		account.get_semester_balance(2026, 3)