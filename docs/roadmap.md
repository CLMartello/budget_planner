# Budget Planner Roadmap

```markdown
Phase 1 – Project Setup (Core Foundation)

[x] Create GitHub repository
[x] Define project structure (src/, data/, tests/, docs/)
[x] Add README and LICENSE
[x] Configure Python environment and requirements
[x] Plan OOP architecture (UML class diagram)

Phase 2 – Core OOP Implementation
[x] Create Transaction class
[x] Create Account class
[x] Create StorageManager class for file persistence
[x] Create BudgetPlanner class to manage accounts
[x] Implement serialization (to_dict / from_dict)
[ ] Write initial unit tests for core classes

Phase 3 – CLI Interface
[ ] Create main CLI menu
[ ] Implement account management in CLI:
	[ ] Create account
	[ ] Remove account
	[ ] Merge accounts
	[ ] List all accounts
[ ] Implement transaction management in CLI:
	[ ] Add transaction
	[ ] Edit last transaction
	[ ] List incomes and expenses
	[ ] Discriminate expenses by category or date
[ ] Implement fund transfer between accounts
[ ] Display account history and balance

Phase 4 – Analytics & Reporting
[ ] Implement semester balance calculation
[ ] Implement overall financial summary
[ ] Generate expense breakdown by category
[ ] Optional: Visual charts with matplotlib or similar

Phase 5 – Persistence & Data Handling
[ ] Load and save all accounts and transactions to JSON
[ ] Implement error handling for file I/O
[ ] Optional: CSV import/export for accounts and transactions

Phase 6 – Testing
[ ] Write unit tests for:
	[ ] Account methods
	[ ] Transaction methods
	[ ] BudgetPlanner methods
	[ ] StorageManager methods
[ ] Implement CLI I/O mocking for automated testing
[ ] Ensure 100% coverage of core logic

Phase 7 – Documentation
[ ] Complete README (description, setup, usage, roadmap)
[ ] Add UML class diagram and OOP explanation
[ ] Add usage examples
[ ] Optional: CONTRIBUTING.md and Code of Conduct

Phase 8 – Optional / Advanced Features
[ ] Predictive expense suggestions using ML
[ ] Web or GUI interface (Flask, Tkinter, or PyQt)
[ ] Multi-user support
[ ] Additional reporting (monthly, yearly, category trends)
```
