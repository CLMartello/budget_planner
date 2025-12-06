
from models.account import Account
from services.storage_manager import StorageManager

class	BudgetPlanner:
	def __init__(self):
		self.storage = StorageManager()
		self.accounts: dict[str, Account] = {}

	def create_account(self, name: str):
		if name in self.accounts:
			raise ValueError("Account already exists.")
		self.accounts[name] = Account(name)

	def get_account(self, name: str) -> Account:
		return self.accounts.get(name)

