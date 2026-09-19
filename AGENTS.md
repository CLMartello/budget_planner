# AGENTS.md

## Project overview

Budget Planner is a small Python application for managing accounts and transactions. The core domain code lives under `src/`, JSON persistence is handled by `StorageManager`, and the interactive entry point is `src/cli.py`.

This file applies to the entire repository.

## Project goals

This is both a learning project and a public portfolio project. Every change should support these goals:

1. Help the repository owner learn Python and object-oriented programming.
2. Develop the application in small, understandable, verifiable steps.
3. Keep the repository polished enough to present in a CV or portfolio.

Prefer clear Python and explicit OOP concepts over clever or overly abstract solutions. When handing off a change, briefly explain the relevant Python/OOP concept, why the design was chosen, and what the owner could study or implement next. Do not complete several roadmap phases in one change unless explicitly requested.

## Repository map

- `src/planner.py`: `BudgetPlanner` orchestration and cross-account operations.
- `src/models/account.py`: account state, transaction history, balance, and serialization.
- `src/models/transaction.py`: transaction model and serialization.
- `src/services/storage_manager.py`: JSON file persistence.
- `src/cli.py`: menu-driven command-line interface.
- `tests/`: pytest unit tests.
- `docs/roadmap.md`: planned and completed features.
- `pytest.ini`: adds `src` to the pytest import path.
- `src/api.py`: FastAPI endpoints that expose planner operations over HTTP.

## Development setup

Use Python 3.10 or newer because the code uses built-in generic type annotations such as `list[Transaction]` and `dict[str, Account]`.

Create and activate a virtual environment, then install pytest:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Verification

Run these checks from the repository root:

```bash
python -m compileall -q src
python -m pytest -q
```

For a focused change, run the relevant test module first, then the full suite before handoff. Examples:

```bash
python -m pytest -q tests/test_account.py
python -m pytest -q tests/test_budget_planner.py
```

When changing persistence, also exercise a save/load round trip with a temporary path. Never use or commit a developer's real `data/accounts.json` as a test fixture.

## Code conventions

- Keep domain behavior in the model and planner modules; keep terminal input/output in `src/cli.py`.
- Pass `Transaction` objects to `Account.add_transaction()` unless deliberately changing that API and all callers/tests together.
- Preserve the sign convention: positive amounts are income and negative amounts are expenses.
- Keep persisted data JSON-compatible. Update both `to_dict()` and `from_dict()` together when the schema changes, and remain tolerant of missing optional fields where practical.
- Accept caller-provided storage paths so tests can use `tmp_path`; avoid hard-coding paths outside the existing default.
- Raise `ValueError` for invalid domain operations in the same style as the existing planner methods.
- Follow the surrounding style for narrow edits. Avoid repository-wide whitespace or indentation cleanup as part of an unrelated change.
- Add type hints to new or changed public methods when practical.

## Testing expectations

- Add tests for new behavior and regressions.
- Cover successful operations and important error cases, especially duplicate/missing accounts, empty transaction histories, invalid transfer amounts, insufficient funds, and serialization round trips.
- Use pytest's `tmp_path` for filesystem tests.
- Keep tests deterministic: provide explicit dates when date values affect assertions.
- Do not test the interactive CLI when the same behavior can be tested through `BudgetPlanner` or the models; mock input/output only for CLI-specific behavior.

## Change discipline

- Read the relevant implementation and tests before editing.
- Make one small, coherent change at a time. Avoid mixing features, refactors, formatting, and unrelated fixes.
- Keep each step easy to review and explain. Introduce abstractions only when they solve a current, visible problem.
- Preserve opportunities for learning: explain important decisions and avoid replacing straightforward project code with advanced frameworks or generated boilerplate.
- Keep changes focused and do not overwrite unrelated work in a dirty worktree.
- Do not commit generated files such as `__pycache__/`, `.pyc`, local virtual environments, or runtime account data.
- Update documentation with every code change. At minimum, check `README.md` and `docs/roadmap.md`; update whichever describes the changed behavior, architecture, usage, or feature status. If no text change is needed, state why in the handoff.
- Treat documentation quality, spelling, examples, and accurate project status as part of the deliverable because the repository is intended for a CV/portfolio.
- Recommend a concise Conventional Commit message for every completed change, such as `feat(planner): add account removal`, `fix(account): restore JSON serialization`, or `test(storage): cover save and load`. Use the imperative mood and describe one coherent change.
- Do not create a Git commit, push, or rewrite history unless the repository owner explicitly requests it.

## Handoff

Summarize the files changed and behavior affected. Explain the main Python/OOP lesson in plain language, state the exact verification commands run and their results, identify documentation updated, and recommend the next small step plus a commit message. If a check could not run or still fails, include the reason and enough output to distinguish a new regression from a known baseline issue.
