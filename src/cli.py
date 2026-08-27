
from planner import BudgetPlanner
from models.transaction import Transaction
from datetime import datetime

def print_menu():
	print("\n=== Budget Planner ===")
	print("1. Create account")
	print("2. Remove account")
	print("3. Merge accounts")
	print("4. List accounts")
	print("5. Add transaction")
	print("6. Edit last transaction")
	print("7. Transfer funds")
	print("8. Show account history and balance")
	print("9. List incomes and expenses")
	print("10. Discriminate expenses")
	print("11. Show semester balance")
	print("12. Show expense breakdown")
	print("0. Exit")

def get_date():
	date_str = input("Date (YYYY-MM-DD) or leave empty for today: ")
	if not date_str:
		return datetime.today().date()
	return datetime.strptime(date_str, "%Y-%m-%d").date()

def get_amount(prompt):
	try:
		return float(input(prompt))
	except ValueError:
		raise ValueError("Amount must be a number.")

def get_integer(prompt, error_message):
	try:
		return int(input(prompt))
	except ValueError:
		raise ValueError(error_message)

def main():
	planner = BudgetPlanner()

	while True:
		print_menu()
		option = input("Choose an option: ")

		try:

			# CREATE ACCOUNT
			if option == "1":
				name = input("Account name: ")
				planner.create_account(name)
				print("Account created.")

			# REMOVE ACCOUNT
			elif option == "2":
				name = input("Account name to remove: ")
				planner.remove_account(name)
				print("Account removed.")

			# MERGE ACCOUNTS
			elif option == "3":
				source = input("Source account: ")
				target = input("Target account: ")
				planner.merge_accounts(source, target)
				print("Accounts merged.")

			# LIST ACCOUNTS
			elif option == "4":
				for name in planner.accounts:
					print("-", name)

			# ADD TRANSACTION
			elif option == "5":
				account = input("Account name: ")
				amount = get_amount("Amount: ")
				category = input("Category: ")
				description = input("Description: ")
				date = get_date()

				planner.add_transaction(
					account, amount, category, description, date
				)
				print("Transaction added.")

			# EDIT LAST TRANSACTION
			elif option == "6":
				account = input("Account name: ")
				amount = get_amount("New amount: ")
				category = input("New category: ")
				description = input("New description: ")

				planner.edit_last_transaction(
					account, amount, category, description
				)
				print("Last transaction updated.")

			# TRANSFER FUNDS
			elif option == "7":
				source = input("From account: ")
				target = input("To account: ")
				amount = get_amount("Amount: ")

				planner.transfer_funds(source, target, amount)
				print("Transfer completed.")

			# ACCOUNT HISTORY AND BALANCE
			elif option == "8":
				account = input("Account name: ")
				acc = planner.get_account(account)

				if acc is None:
					raise ValueError("Account does not exist.")

				print("\nTransactions:")
				for t in acc.transactions:
					print(t)

				print(f"\nBalance: {acc.get_balance():.2f}")

			# LIST INCOMES AND EXPENSES
			elif option == "9":
				income, expenses = planner.get_income_and_expenses()
				print(f"Total income: {income:.2f}")
				print(f"Total expenses: {expenses:.2f}")
			
			# DISCRIMINATE EXPENSES
			elif option == "10":
				category = input("Category to filter: ")
				expenses = planner.get_expenses_by_category(category)

				for t in expenses:
					print(t)

			# SHOW SEMESTER BALANCE
			elif option == "11":
				account = input("Account name: ")
				year = get_integer("Year: ", "Year must be a number.")
				semester = get_integer(
					"Semester (1 or 2): ",
					"Semester must be a number.")

				balance = planner.get_semester_balance(
					account,
					year,
					semester
				)

				print(f"Semester balance: {balance:.2f}")

			# SHOW EXPENSE BREAKDOWN
			elif option == "12":
				breakdown = planner.get_expense_breakdown()

				if not breakdown:
					print("No expenses recorded.")
				else:
					print("\nExpense breakdown:")

				for category, total in sorted(breakdown.items()):
					print(f"{category}: {total:.2f}")				

			# EXIT
			elif option == "0":
				planner.save()
				print("Goodbye.")
				break

			else:
				print("Invalid option.")

		except ValueError as e:
			print(f"Error: {e}")

if __name__ == "__main__":
	main()
