const accountsList = document.querySelector("#accounts-list");
const totalBalance = document.querySelector("#total-balance");
const totalIncome = document.querySelector("#total-income");
const totalExpenses = document.querySelector("#total-expenses");
const accountCount = document.querySelector("#account-count");

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

			const accountName = document.createElement("strong");
			accountName.textContent = name;

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

async function loadSummary() {
    try {
        const response = await fetch("/reports/summary");

        if (!response.ok) {
            throw new Error("Could not load finantial summary.");
        }

        const data = await response.json();

        totalBalance.textContent = formatCurrency(data.balance);
        totalIncome = formatCurrency(data.income);
        totalExpenses = formatCurrency(data.expenses);
    } catch (error) {
        totalBalance.textContent = "Unavailable";
        totalIncome.textContent = "Unavailable";
        totalExpenses.textContent = "Unavailable";
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

        await loadAccounts();
        await loadSummary();
    } catch (error) {
        accountMessage.textContent = error.message;
    }
}

const accountForm = document.querySelector("#account-form");
const accountNameInput = document.querySelector("#account-name");
const accountMessage = document.querySelector("#account-message");

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

loadAccounts();
loadSummary();