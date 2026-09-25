const accountsList = document.querySelector("#accounts-list");
const totalBalance = document.querySelector("#total-balance");
const totalIncome = document.querySelector("#total-income");
const totalExpenses = document.querySelector("#total-expenses");
const accountCount = document.querySelector("#account-count");
const transactionsList = document.querySelector("#transactions-list");
const selectedAccountName = document.querySelector("#selected-account-name");
const addTransactionButton = document.querySelector("#add-transaction-button");
const transactionForm = document.querySelector("#transaction-form");
const transactionAmount = document.querySelector("#transaction-amount");
const transactionCategory = document.querySelector("#transaction-category");
const transactionDescription = document.querySelector("#transaction-description");
const transactionDate = document.querySelector("#transaction-date");
const transactionMessage = document.querySelector("#transaction-message");
const expenseBreakdown = document.querySelector("#expense-breakdown");
const semesterForm = document.querySelector("#semester-form");
const semesterYear = document.querySelector("#semester-year");
const semesterNumber = document.querySelector("#semester-number");
const semesterBalance = document.querySelector("#semester-balance");
const semesterPeriod = document.querySelector("#semester-period");

semesterYear.value = new Date().getFullYear();

let selectedAccount = null;

function formatCurrency(amount) {
    return new Intl.NumberFormat("en-IE", {
        style: "currency",
        currency: "EUR"
    }).format(amount);
}

async function loadAccounts() {
	try {
		const response = await fetch("/accounts");

		if (!response.ok) {
			throw new Error("Could not load accounts.");
		}

		const data = await response.json();

        const count = data.accounts.length;
        accountCount.textContent = 
            `${count} account${count === 1 ? "" : "s"}`;

		accountsList.replaceChildren();

		if (data.accounts.length === 0) {
			const message = document.createElement("p");
			message.textContent = "No accounts created yet.";
			accountsList.append(message);
			return;
		}

		for (const name of data.accounts) {
			const account = document.createElement("div");
			account.className = "account";

			const accountName = document.createElement("button");
			accountName.type = "button";
            accountName.className = "account-select";
            accountName.textContent = name;

            accountName.addEventListener("click", () => {
                loadTransactions(name);
            })

			const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.textContent = "Remove";
            removeButton.className = "remove-account";

            removeButton.addEventListener("click", () => {
                removeAccount(name);
            });
            
            account.append(accountName, removeButton);
			accountsList.append(account);
		}
	} catch (error) {
		accountsList.textContent = error.message;
	}
}

async function loadTransactions(name) {
    semesterBalance.textContent = "";
    semesterPeriod.textContent = 
        "Select a year and semester.";

    selectedAccount = name;
    addTransactionButton.disabled = false;

	selectedAccountName.textContent = name;
	transactionsList.textContent = "Loading transactions...";

	try {
		const response = await fetch(
			`/accounts/${encodeURIComponent(name)}/transactions`
		);

		if (!response.ok) {
			const data = await response.json();
			throw new Error(data.detail);
		}

		const data = await response.json();
		transactionsList.replaceChildren();

		if (data.transactions.length === 0) {
			const message = document.createElement("p");
			message.textContent = "No transactions yet.";
			transactionsList.append(message);
			return;
		}

		for (const transaction of data.transactions) {
			const row = document.createElement("div");
			row.className = "transaction";

			const icon = document.createElement("div");
			icon.className = "transaction-icon";
			icon.textContent =
				transaction.amount >= 0 ? "↗" : "↘";

			const details = document.createElement("div");

			const description = document.createElement("strong");
			description.textContent =
				transaction.description || "Transaction";

			const category = document.createElement("small");
			category.textContent = transaction.category;

			details.append(description, document.createElement("br"), category);

			const amount = document.createElement("span");
			amount.className = "amount";

			if (transaction.amount < 0) {
				amount.classList.add("negative");
			}

			amount.textContent =
				transaction.amount >= 0
					? `+${formatCurrency(transaction.amount)}`
					: formatCurrency(transaction.amount);

			row.append(icon, details, amount);
			transactionsList.append(row);
		}
	} catch (error) {
		transactionsList.textContent = error.message;
	}
}

async function loadSummary() {
    try {
        const response = await fetch("/reports/summary");

        if (!response.ok) {
            throw new Error("Could not load financial summary.");
        }

        const data = await response.json();

        totalBalance.textContent = formatCurrency(data.balance);
        totalIncome.textContent = formatCurrency(data.income);
        totalExpenses.textContent = formatCurrency(data.expenses);
    } catch (error) {
        totalBalance.textContent = "Unavailable";
        totalIncome.textContent = "Unavailable";
        totalExpenses.textContent = "Unavailable";
    }
}

async function loadExpenseBreakdown() {
    try {
        const response = await fetch(
            "/reports/expenses/by-category"
        );

        if (!response.ok) {
            throw new Error(
                "Could not load expense breakdown."
            );
        }

        const data = await response.json();
        const entries = Object.entries(data.expenses);

        expenseBreakdown.replaceChildren();

        if (entries.length === 0) {
            const message = document.createElement("p");
            message.textContent = "No expenses recorded.";
            expenseBreakdown.append(message);
            return;
        }

        const total = entries.reduce(
            (sum, entry) => sum + entry[1],
            0
        );

        for (const [categoryName, categoryAmount] of entries) {
            const category = document.createElement("div");
            category.className = "category";

            const name = document.createElement("span");
            name.textContent = categoryName;

            const amount = document.createElement("strong");
            amount.textContent = formatCurrency(categoryAmount);

            const percentage = document.createElement("small");
            percentage.textContent = 
                `${Math.round(categoryAmount / total * 100)}% of expenses`;
            
            category.append(name, amount, percentage);
            expenseBreakdown.append(category);
        }
    } catch (error) {
        expenseBreakdown.textContent = error.message;
    }
}

async function removeAccount(name) {
    const confirmed = window.confirm(
        `Remove account "${name}"?`
    );

    if (!confirmed) {
        return;
    }

    accountMessage.textContent = "";

    try {
        const response = await fetch(
            `/accounts/${encodeURIComponent(name)}`,
            { method: "DELETE" }
        );

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail);
        }

        accountMessage.textContent =
            `Account "${name}" removed.`;

        if (selectedAccount === name) {
            selectedAccount = null;
            addTransactionButton.disabled = true;
            transactionForm.hidden = true;
            selectedAccountName.textContent = "Select an account";
            transactionsList.textContent =
                "Select an account to view its transactions.";
        }

        await loadAccounts();
        await loadSummary();
        await loadExpenseBreakdown();
    } catch (error) {
        accountMessage.textContent = error.message;
    }
}

const accountForm = document.querySelector("#account-form");
const accountNameInput = document.querySelector("#account-name");
const accountMessage = document.querySelector("#account-message");

addTransactionButton.addEventListener("click", () => {
    transactionForm.hidden = !transactionForm.hidden;
});

transactionForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    transactionMessage.textContent = "";

    if (selectedAccount === null) {
        transactionMessage.textContent =
            "Select an account first."
        return;
    }

    const transaction = {
        amount: Number(transactionAmount.value),
        category: transactionCategory.value.trim(),
        description: transactionDescription.value.trim(),
        date: transactionDate.value || null
    };

    try {
        const response = await fetch(
            `/accounts/${encodeURIComponent(selectedAccount)}/transactions`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(transaction)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail);
        }

        transactionMessage.textContent = 
            "Transaction created.";

        transactionForm.reset();
        transactionForm.hidden = true;

        await loadTransactions(selectedAccount);
        await loadSummary();
        await loadExpenseBreakdown();
    } catch (error) {
        transactionMessage.textContent = error.message;
    }
});

accountForm.addEventListener("submit", async (event) => {
	event.preventDefault();

	const name = accountNameInput.value.trim();
	accountMessage.textContent = "";

	try {
		const response = await fetch("/accounts", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ name })
		});

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.detail);
		}

		accountMessage.textContent =
			`Account "${data.name}" created.`;

		accountForm.reset();
		await loadAccounts();
	} catch (error) {
		accountMessage.textContent = error.message;
	}
});

semesterForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (selectedAccount === null) {
        semesterBalance.textContent = "";
        semesterPeriod.textContent =
            "Select an account first.";
        return;
    }

    const year = Number(semesterYear.value);
    const semester = Number(semesterNumber.value);

    const parameters = new URLSearchParams({
        year: String(year),
        semester: String(semester)
    });

    try {
        const response = await fetch(
            `/accounts/${encodeURIComponent(selectedAccount)}` +
			`/reports/semester-balance?${parameters}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail);
        }

        semesterBalance.textContent = 
            formatCurrency(data.balance);

        const months = 
            semester === 1 ? "January-June" : "July-December";

        semesterPeriod.textContent =
            `${selectedAccount} · ${months} ${year}`;
    } catch (error) {
        semesterBalance.textContent = "Unavailable";
        semesterPeriod.textContent = error.message;
    }
});

loadAccounts();
loadSummary();
loadExpenseBreakdown();