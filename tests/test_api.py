from fastapi.testclient import TestClient
import api
from planner import BudgetPlanner
from datetime import datetime

client = TestClient(api.app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_accounts(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get("/accounts")

    assert response.status_code == 200
    assert response.json() == {"accounts": ["Personal"]}

def test_create_account(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/accounts",
        json={"name": "Savings"}
    )

    assert response.status_code == 201
    assert response.json() == {"name": "Savings"}
    assert "Savings" in test_planner.accounts

def test_create_duplicate_account_returns_conflict(
    tmp_path,
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Savings")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/accounts",
        json={"name": "Savings"})

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Account already exists."
    }

def test_remove_account(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.delete("/accounts/Personal")

    assert response.status_code == 204
    assert "Personal" not in test_planner.accounts

def test_remove_missing_account_returns_not_found(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.delete("/accounts/Missing")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account does not exist."
    }

def test_create_transaction(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")

    monkeypatch.setattr(api, "planner", test_planner)

    response =client.post(
        "/accounts/Personal/transactions",
        json={
            "amount": 125.50,
            "category": "Salary",
            "description": "September income",
            "date": "2026-09-21T10:00:00"
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        "amount": 125.50,
        "category": "Salary",
        "description": "September income",
        "date": "2026-09-21T10:00:00"
    }
    assert test_planner.get_account("Personal").get_balance() == 125.50

def test_create_transaction_missing_account_returns_not_found(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response =client.post(
        "/accounts/Personal/transactions",
        json={
            "amount": 125.50,
            "category": "Salary",
            "description": "September income",
            "date": "2026-09-21T10:00:00"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account does not exist."
    }

def test_list_transactions(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")
    test_planner.add_transaction(
        "Personal",
        -25,
        "Food",
        "Lunch",
        datetime.fromisoformat("2026-09-21T12:30:00")
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get("/accounts/Personal/transactions")

    assert response.status_code == 200
    assert response.json() == {
        "transactions": [
            {
                "amount": -25.0,
                "category": "Food",
                "description": "Lunch",
                "date": "2026-09-21T12:30:00"
            }
        ]
    }

def test_list_transactions_missing_account_returns_not_found(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get("/accounts/Missing/transactions")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account does not exist."
    }

def test_edit_latest_transaction(
    tmp_path,
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")
    test_planner.add_transaction(
        "Personal",
        -25,
        "Food",
        "Lunch",
        datetime(2026, 9, 21, 12, 30)
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.patch(
        "/accounts/Personal/transactions/latest",
        json={
            "amount": -30,
            "category": "Restaurant",
            "description": "Lunch with friends"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "amount": -30,
        "category": "Restaurant",
        "description": "Lunch with friends",
        "date": "2026-09-21T12:30:00"
    }

def test_edit_latest_transaction_with_empty_history_returns_not_found(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.patch(
        "/accounts/Personal/transactions/latest",
        json={
            "amount": -30,
            "category": "Restaurant",
            "description": "Lunch with friends"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No transactions to edit."
    }

def test_edit_latest_transaction_missing_account_returns_not_found(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.patch(
        "/accounts/Missing/transactions/latest",
        json={
            "amount": -30,
            "category": "Restaurant",
            "description": "Lunch with friends"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account does not exist."
    }

def test_transfer_funds(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Checking")
    test_planner.create_account("Savings")
    test_planner.add_transaction(
        "Checking",
        100,
        "Income",
        "Initial deposit"
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/transfers",
        json={
            "source": "Checking",
            "target": "Savings",
            "amount": 30
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        "source": "Checking",
        "target": "Savings",
        "amount": 30
    }
    assert test_planner.get_account("Checking").get_balance() == 70
    assert test_planner.get_account("Savings").get_balance() == 30

def test_transfer_insufficient_funds_returns_bad_request(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Checking")
    test_planner.create_account("Savings")
    test_planner.add_transaction(
        "Checking",
        10,
        "Income",
        "Initial deposit"
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/transfers",
        json={
            "source": "Checking",
            "target": "Savings",
            "amount": 30
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Insufficient funds."
    }

def test_transfer_to_same_account_returns_bad_request(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Checking")
    test_planner.add_transaction(
        "Checking",
        100,
        "Income",
        "Initial deposit"
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/transfers",
        json={
            "source": "Checking",
            "target": "Checking",
            "amount": 30
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Source and target accounts must be different."
    }

def test_transfer_non_positive_amount_returns_bad_request(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Checking")
    test_planner.create_account("Savings")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/transfers",
        json={
            "source": "Checking",
            "target": "Savings",
            "amount": 0
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Amount must be positive."
    }

def test_transfer_missing_account_returns_bad_request(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Checking")
    test_planner.add_transaction(
        "Checking",
        100,
        "Income",
        "Initial deposit"
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.post(
        "/transfers",
        json={
            "source": "Checking",
            "target": "Missing",
            "amount": 30
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "One or both accounts do not exist."
    }

def test_get_financial_summary(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")
    test_planner.add_transaction(
        "Personal",
        100,
        "Salary",
        "Income"
    )
    test_planner.add_transaction(
        "Personal",
        -40,
        "Food",
        "Groceries"
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get("/reports/summary")

    assert response.status_code == 200
    assert response.json() == {
        "income": 100.0,
        "expenses": 40.0,
        "balance": 60.0
    }

def test_get_expense_breakdown(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")
    test_planner.add_transaction(
        "Personal", -25, "Food", "Groceries"
    )
    test_planner.add_transaction(
        "Personal", -15, "Transport", "Bus pass"
    )
    test_planner.add_transaction(
        "Personal", -10, "Food", "Lunch"
    )

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get("/reports/expenses/by-category")

    assert response.status_code == 200
    assert response.json() == {
        "expenses": {
            "Food": 35.0,
            "Transport": 15.0
        }
    }

def test_get_semester_balance(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")
    test_planner.add_transaction(
		"Personal",
		100,
		"Salary",
		"January income",
		datetime(2026, 1, 15)
	)
    test_planner.add_transaction(
		"Personal",
		-30,
		"Food",
		"February expense",
		datetime(2026, 2, 10)
	)
    test_planner.add_transaction(
		"Personal",
		200,
		"Salary",
		"August income",
		datetime(2026, 8, 5)
	)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get(
        "/accounts/Personal/reports/semester-balance",
        params={"year": 2026, "semester": 1}
    )

    assert response.status_code == 200
    assert response.json() == {
        "account": "Personal",
        "year": 2026,
        "semester": 1,
        "balance": 70.0
    }

def test_get_semester_balance_invalid_semester_returns_bad_request(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get(
        "/accounts/Personal/reports/semester-balance",
        params={"year": 2026, "semester": 3}
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Semester must be 1 or 2."
    }

def test_get_semester_balance_rejects_non_numeric_year(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)
    test_planner.create_account("Personal")

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get(
        "/accounts/Personal/reports/semester-balance",
        params={"year": "not-a-year", "semester": 1}
    )

    assert response.status_code == 422

def test_get_semester_balance_missing_account_returns_not_found(
    tmp_path, 
    monkeypatch
):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get(
        "/accounts/Missing/reports/semester-balance",
        params={"year": 2026, "semester": 1}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account does not exist."
    }

def test_get_empty_expense_breakdown(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    monkeypatch.setattr(api, "planner", test_planner)

    response = client.get(
        "/reports/expenses/by-category"
    )

    assert response.status_code == 200
    assert response.json() == {
        "expenses": {}
    }