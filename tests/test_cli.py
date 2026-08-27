from cli import main
from planner import BudgetPlanner
import pytest
from datetime import datetime

def test_invalid_menu_option(tmp_path, monkeypatch, capsys):
    test_file = tmp_path / "test.json"
    planner = BudgetPlanner(storage_path=test_file)
    inputs = iter(["invalid", "0"])

    monkeypatch.setattr("cli.BudgetPlanner", lambda: planner)
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(inputs)
    )

    main()

    output = capsys.readouterr().out

    assert "Invalid option" in output
    assert "Goodbye." in output

def test_invalid_transaction_amount(tmp_path, monkeypatch, capsys):
    test_file = tmp_path / "test.json"
    planner = BudgetPlanner(storage_path=test_file)
    inputs = iter(["5", "Personal", "not-a-number", "0"])

    monkeypatch.setattr("cli.BudgetPlanner", lambda: planner)
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(inputs)
    )

    main()

    output = capsys.readouterr().out

    assert "Error: Amount must be a number." in output
    assert "Goodbye." in output


def test_history_for_missing_account(tmp_path, monkeypatch, capsys):
    test_file = tmp_path / "test.json"
    planner = BudgetPlanner(storage_path=test_file)
    inputs = iter(["8", "Missing", "0"])

    monkeypatch.setattr("cli.BudgetPlanner", lambda: planner)
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(inputs)
    )

    main()

    output = capsys.readouterr().out

    assert "Error: Account does not exist." in output
    assert "Goodbye." in output

def test_unexpected_cli_error_is_not_hidden(tmp_path, monkeypatch):
    test_file = tmp_path / "test.json"
    planner = BudgetPlanner(storage_path=test_file)
    inputs = iter(["1", "Personal", "0"])

    def raise_unexpected_error(name):
        raise RuntimeError("Unexpected failure")

    monkeypatch.setattr("cli.BudgetPlanner", lambda: planner)
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(inputs)
    )
    monkeypatch.setattr(
        planner,
        "create_account",
        raise_unexpected_error
    ) 

    with pytest.raises(RuntimeError, match="Unexpected failure"):
        main()

def test_show_semester_balance(
	tmp_path,
	monkeypatch,
	capsys
):
	test_file = tmp_path / "test.json"
	planner = BudgetPlanner(storage_path=test_file)

	planner.create_account("Personal")
	planner.add_transaction(
		"Personal",
		1000,
		"Salary",
		"January salary",
		datetime(2026, 1, 15)
	)
	planner.add_transaction(
		"Personal",
		-200,
		"Food",
		"March groceries",
		datetime(2026, 3, 10)
	)

	inputs = iter([
		"11",
		"Personal",
		"2026",
		"1",
		"0"
	])

	monkeypatch.setattr("cli.BudgetPlanner", lambda: planner)
	monkeypatch.setattr(
		"builtins.input",
		lambda prompt: next(inputs)
	)

	main()

	output = capsys.readouterr().out

	assert "Semester balance: 800.00" in output
	assert "Goodbye." in output