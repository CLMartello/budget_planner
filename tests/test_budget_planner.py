
from planner import BudgetPlanner
import pytest

def test_create_account(tmp_path):
	test_file = tmp_path / "test.json"

	planner = BudgetPlanner(storage_path=test_file)
	planner.create_account("Personal")

	assert "Personal" in planner.accounts

def test_save_and_load(tmp_path):
	test_file = tmp_path / "test.json"

	planner = BudgetPlanner(storage_path=test_file)
	planner.create_account("Personal")
	planner.save()

	new_planner = BudgetPlanner(storage_path=test_file)
	assert "Personal" in new_planner.accounts

def test_transfer_funds(tmp_path):
	test_file = tmp_path / "test.json"
	planner = BudgetPlanner(storage_path=test_file)
    
	planner.create_account("Checking")
	planner.create_account("Savings")
	planner.add_transaction(
		"Checking",
		100,
		"Income",
		"Initial deposit"
	)

	planner.transfer_funds("Checking", "Savings", 30)

	assert planner.accounts["Checking"].get_balance() == 70
	assert planner.accounts["Savings"].get_balance() == 30

def test_transfer_insufficient_funds(tmp_path):
	test_file = tmp_path / "test.json"
	planner = BudgetPlanner(storage_path=test_file)

	planner.create_account("Checking")
	planner.create_account("Savings")
	planner.add_transaction(
		"Checking",
		100,
		"Income",
		"Initial deposit"
	)

	with pytest.raises(ValueError, match="Insufficient funds"):
		planner.transfer_funds("Checking", "Savings", 200)

def test_cannot_merge_account_with_itself(tmp_path):
	test_file = tmp_path / "test.json"
	planner = BudgetPlanner(storage_path=test_file)
	planner.create_account("Personal")

	with pytest.raises(ValueError, match="different"):
		planner.merge_accounts("Personal", "Personal")

	