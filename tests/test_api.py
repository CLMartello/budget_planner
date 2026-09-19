from fastapi.testclient import TestClient
import api
from planner import BudgetPlanner

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