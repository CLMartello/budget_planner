
from planner import BudgetPlanner
from models.transaction import Transaction

planner = BudgetPlanner()

def main():
	while True:
		print("\n1. Create account")
		print("2. Add transaction")
		print("3. Show balance")
		print("0. Exit")

		option = input("Choose: ")

		if option == "1":
			name = input("Account name: ")
			planner.create_account(name)
			print("Account created!")

		elif option == "2":
			acc = input("Account: ")
			amount = float(input("Amount (+income - -expense): "))
			cat = input("Category: ")
			tx = Transaction(amount, cat)
			planner.accounts[acc].add_transaction(tx)
			print("Transaction added!")

		elif option == "3":
			acc = input("Account: ")
			lab = planner.accounts[acc].get_balance()
			print("Balance:", bal)

		elif option == "0":
			break

if __name__ == "__main__":
	main()
