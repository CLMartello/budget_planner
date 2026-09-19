from fastapi import FastAPI, HTTPException
from planner import BudgetPlanner
from pydantic import BaseModel

class AccountCreate(BaseModel):
    name: str

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
