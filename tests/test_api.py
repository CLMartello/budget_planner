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

def test_list_transactions_missing_account_returns_not_found(tmp_path, monkeypatch):
    test_file = tmp_path / "accounts.json"
    test_planner = BudgetPlanner(storage_path=test_file)

    response = client.get("/accounts/Missing/transactions")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account does not exist."
    }
