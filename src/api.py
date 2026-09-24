from fastapi import FastAPI, HTTPException
from planner import BudgetPlanner
from pydantic import BaseModel
from datetime import datetime

class AccountCreate(BaseModel):
    name: str

class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: str = ""
    date: datetime | None = None

class TransactionUpdate(BaseModel):
    amount: float
    category: str
    description: str = ""

class TransferCreate(BaseModel):
    source: str
    target: str
    amount: float

app = FastAPI(title="Budget Planner API")
planner = BudgetPlanner()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/accounts")
def list_accounts():
    return {"accounts": list(planner.accounts)}

@app.post("/accounts", status_code=201)
def create_account(account: AccountCreate):
    try:
        planner.create_account(account.name)
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        ) from error
    
    planner.save()

    return{"name": account.name}

@app.delete("/accounts/{name}", status_code=204)
def remove_account(name: str):
    try:
        planner.remove_account(name)
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error
    
    planner.save()

@app.post(
    "/accounts/{name}/transactions",
    status_code=201
)
def create_transaction(
    name: str,
    transaction: TransactionCreate
):
    try:
        planner.add_transaction(
            name,
            transaction.amount,
            transaction.category,
            transaction.description,
            transaction.date
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    planner.save()

    created_transaction = (
        planner.get_account(name).transactions[-1]
    )
    return created_transaction.to_dict()

@app.get("/accounts/{name}/transactions")
def list_transactions(name: str):
    account = planner.get_account(name)
    
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account does not exist."
        )

    return {
        "transactions": [
            transaction.to_dict()
            for transaction in account.transactions
        ]
    }

@app.patch("/accounts/{name}/transactions/latest")
def edit_latest_transaction(
    name: str,
    transaction: TransactionUpdate
):
    try:
        planner.edit_last_transaction(
            name,
            transaction.amount,
            transaction.category,
            transaction.description
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    planner.save()

    edited_transaction = (
        planner.get_account(name).transactions[-1]
    )

    return edited_transaction.to_dict()

@app.post("/transfers", status_code=201)
def transfer_funds(transfer: TransferCreate):
    try:
        planner.transfer_funds(
            transfer.source,
            transfer.target,
            transfer.amount
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    planner.save()

    return {
        "source": transfer.source,
        "target": transfer.target,
        "amount": transfer.amount
    }

@app.get("/reports/summary")
def get_financial_summary():
    income, expenses = planner.get_income_and_expenses()

    return {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses
    }

@app.get("/reports/expenses/by-category")
def get_expense_breakdown():
    expenses = planner.get_expense_breakdown()

    return {"expenses": expenses}

@app.get("/accounts/{name}/reports/semester-balance")
def get_semester_balance(
    name: str,
    year: int,
    semester: int
):
    if planner.get_account(name) is None:
        raise HTTPException(
            status_code=404,
            detail="Account does not exist."
        )

    try:
        balance = planner.get_semester_balance(
            name,
            year,
            semester
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    return {
        "account": name,
        "year": year,
        "semester": semester,
        "balance": balance
    }