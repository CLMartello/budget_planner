# Budget Planner
A personal finance management system designed to organize accounts, track transactions, visualize spending, and analyze financial habits — built using Python and Object-Oriented Programming (OOP).

## Features
1. Create, remove, and merge financial accounts
2. Add, edit, and classify transactions (income/expense)
3. Transfer funds between accounts
4. View account history and balances
5. Breakdown of expenses by category
6. Semester balance reports
7. Global overview of all accounts
8. Persistent storage using files
9. Clean OOP architecture for easy expansion

## OOP Architecture
UML Class Diagram (Mermaid)

```mermaid
classDiagram
    direction TB

    class BudgetPlanner {
        +Dict~str, Account~ accounts
        +create_account(name: str)
        +remove_account(name: str)
        +merge_accounts(source: str, target: str)
        +transfer_funds(from_acc: str, to_acc: str, amount: float, description: str)
        +list_accounts() List~str~
        +get_overview() Dict
        +load()
        +save()
    }

    class Account {
        +str name
        +List~Transaction~ transactions
        +add_transaction(transaction: Transaction)
        +edit_last_transaction(new_data: Dict)
        +get_balance() float
        +get_incomes() List~Transaction~
        +get_expenses() List~Transaction~
        +get_history() List~str~
        +get_semester_balance(year: int, semester: int) float
        +get_expense_breakdown() Dict~str, float~
    }

    class Transaction {
        +float amount
        +str type
        +str category
        +datetime date
        +str description
    }

    class StorageManager {
        +str file_path
        +load() Dict
        +save(data: Dict)
    }

    BudgetPlanner "1" o-- "*" Account : manages
    Account "1" o-- "*" Transaction : contains
    BudgetPlanner "1" --> "1" StorageManager : uses
```

## Folder Structure

```pgsql
budget_planner/
│
├── src/
│   ├── budget_planner.py
│   ├── account.py
│   ├── transaction.py
│   ├── storage_manager.py
│   └── main.py
│
├── data/
│   └── storage.json
│
├── docs/
│   ├── uml_class_diagram.md
|   └── roadmap.md
│
├── tests/
│   ├── test_account.py
│   ├── test_transactions.py
│   ├── test_planner.py
│   └── test_storage.py
│
└── README.md
```

## Installation

```bash
git clone https://github.com/yourusername/budget-planner
cd budget-planner
python3 main.py
```

## Usage
The system works through a simple menu-based interface:
1. Create accounts
2. Add transactions
3. View reports
4. Transfer funds
5. Remove/merge accounts
6. Save and load automatically

More interfaces (GUI, Web, REST API) can be added later thanks to the OOP structure.

## Roadmap
```markdown
## Roadmap
[x] Phase 1 – Core Classes & OOP Design
[ ] Phase 2 – CLI Interface
[ ] Phase 3 – Reporting & Analytics
[ ] Phase 4 – Persistence & Testing
[ ] Phase 5 – Optional Features
```

## License
MIT License.

You are free to use, modify, and distribute this project.
