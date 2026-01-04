
from models.account import Account
from services.storage_manager import StorageManager

class	BudgetPlanner:
	def __init__(self, storage_path="data/accounts.json"):
		self.storage = StorageManager(storage_path)
		self.accounts: dict[str, Account] = {}
		self.load()

	def create_account(self, name: str):
		if name in self.accounts:
			raise ValueError("Account already exists.")
		self.accounts[name] = Account(name)

	def get_account(self, name: str) -> Account:
		return self.accounts.get(name)

	def remove_account(self, name: str):
		if name not in self.accounts:
			raise ValueError("Account does not exist.")
		del self.accounts[name]

	def merge_accounts(self, source: str, target: str):
		if source not in self.accounts or target not in self.accounts:
			raise ValueError("One or both accounts do not exist.")

		source_acc = self.accounts[source]
		target_acc = self.accounts[target]

		for transaction in source_acc.transactions:
			target_acc.transactions.append(transaction)

		del self.accounts[source]

	def edit_last_transaction(self, account_name, amount, category, description):
		if account_name not in self.accounts:
			raise ValueError("Account does not exist.")

		self.accounts[account_name].edit_last_transaction(
			amount, category, description
		)

	def transfer_funds(self, source, target, amount):
		if source not in self.accounts or target not in self.accounts:
			raise ValueError("One or both accounts do not exist.")

		if amount <= 0:
			raise ValueError("Amount must be positive.")

		source_acc = self.accounts[source]
		target_acc = self.accounts[target]

		if source_acc.balance < amount:
			raise ValueError("Insuficiente funds.")

		source_acc.add_transaction(-amount, "transfer", f"Transfer to {target}")
		target_acc.add_transaction(-amount, "transfer", f"Transfer to {source}")

	def load(self):
		raw_data = self.storage.load()
		from models.account import Account

		self.accounts = {
			name: Account.from_dict(data)
			for name, data in raw_data.items()
		}

	def save(self):
		data = {
			name: account.to_dict()
			for name, account in self.accounts.items()
		}
		self.storage.save(data)

