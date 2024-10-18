<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { checkToken, checkRole } from "$lib/utils/auth.js";
    import { showNotification } from "$lib/stores/popupStore.js";
    import ExpenseCard from "$lib/components/cards/ExpenseCard.svelte";
    import AddWindowPopup from "$lib/components/Popups/WindowPopups/Expense/AddWindowPopup.svelte";
    import EditWindowPopup from "$lib/components/Popups/WindowPopups/Expense/EditWindowPopup.svelte";
    import GeneralDeleteWindowPopup from "$lib/components/Popups/WindowPopups/GeneralDeleteWidnowPopup.svelte";
    import ExpenseFilterPanel from "$lib/components/FilterPanels/ExpenseFilterPanel.svelte";
    import { ListFilter, Trash, X, Plus } from "lucide-svelte";

    let isValid = false;
    let errorMessage = "";
    let hasAccess = false;
    let expenses = [];
    let selectedExpense = null;
    let isDeletionMode = false;
    let popupType = "";
    let isProccessing = true;
    let showPopupWindow = false;
    let filters = {};
    const expectedRoles = ["user", "manager"];

    onMount(async () => {
        isProccessing = true;
        const { isValid: valid, error } = await checkToken();
        if (!valid) {
            errorMessage = error;
            if (error === "Your account is pending approval") {
                showNotification("Your account is pending approval", "info");
                goto("/pending-approval");
                return;
            } else {
                showNotification(
                    "You do not have access to this page",
                    "error",
                );
                goto("/login");
                return;
            }
        }

        if (valid) {
            hasAccess = await checkRole(expectedRoles);
        }
        if (!hasAccess) {
            showNotification("You do not have access to this page", "error");
            goto("/login");
        } else {
            isValid = true;
            await fetchExpenses();
        }
        isProccessing = false;
    });

    async function fetchExpenses() {
        isProccessing = true;
        let query = "";
        const params = new URLSearchParams();
        if (filters.expenseName)
            params.append("expense_name", filters.expenseName);
        if (filters.expenseAmount)
            params.append("expense_amount", filters.expenseAmount);
        if (filters.expenseDate)
            params.append("expense_date", filters.expenseDate);
        if (filters.expenseCategory)
            params.append("expense_category", filters.expenseCategory);

        query = params.toString();
        try {
            const response = await fetch(
                `http://localhost:8000/api/expenses?${query}`,
                {
                    method: "GET",
                    headers: {
                        Accept: "application/json",
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                        "Content-Type": "application/json",
                    },
                },
            );
            if (!response.ok) {
                const errorData = await response.json();
                if (errorData.status === 403) {
                    if (errorData.detail === "Admins cannot have expenses") {
                        errorMessage =
                            "Admins cannot have expenses. Please contact support for more information.";
                        goto("/login");
                    } else if (
                        errorData.detail === "User is not approved yet"
                    ) {
                        errorMessage =
                            "Your account has not been approved yet. Please wait for approval.";
                        goto("/pending-approval");
                    } else {
                        errorMessage = "You do not have access to this page.";
                        goto("/login");
                    }
                    showNotification(errorMessage, "error");
                } else {
                    errorMessage =
                        errorData.detail || "Failed to fetch expenses";
                    showNotification(errorMessage, "error");
                }
            } else {
                expenses = await response.json();
            }
        } catch (error) {
            console.error("Error occurred while fetching expenses:", error);
            showNotification("Failed to fetch expenses", "error");
        }
        isProccessing = false;
    }

    async function addExpense(expenseName, amount, date, category) {
        isProccessing = true;
        try {
            const response = await fetch("http://localhost:8000/api/expenses", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
                body: JSON.stringify({
                    name: expenseName,
                    amount: amount,
                    date: date,
                    category_id: category,
                }),
            });
            if (!response.ok) {
                const errorData = await response.json();
                showNotification(errorData.detail, "error");
            } else {
                showNotification("Expense added successfully", "success");
                await fetchExpenses();
            }
        } catch (error) {
            console.error("Error occurred while adding expense:", error);
            showNotification("Failed to add expense", "error");
        }
        isProccessing = false;
    }

    async function deleteExpense() {
        isProccessing = true;
        try {
            const response = await fetch(
                `http://localhost:8000/api/expenses/${selectedExpense.id}`,
                {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                },
            );
            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 403) {
                    if (errorData.detail === "Admins cannot have expenses") {
                        errorMessage =
                            "Admins cannot have expenses. Please contact support for more information.";
                        goto("/login");
                    } else if (
                        errorData.detail === "User is not approved yet"
                    ) {
                        errorMessage =
                            "Your account has not been approved yet. Please wait for approval.";
                        goto("/pending-approval");
                    } else {
                        errorMessage = "You do not have access to this page.";
                        goto("/login");
                    }
                    showNotification(errorMessage, "error");
                } else if (response.status === 404) {
                    showNotification("Expense not found", "error");
                } else {
                    errorMessage =
                        errorData.detail || "Failed to delete expense";
                    showNotification(errorMessage, "error");
                }
            } else {
                showNotification("Expense deleted successfully", "success");
                await fetchExpenses();
            }
        } catch (error) {
            console.error("Error occurred while deleting expense:", error);
            showNotification("Failed to delete expense", "error");
        }
        isProccessing = false;
    }

    async function editExpense(name, amount, date, category) {
        isProccessing = true;
        try {
            const response = await fetch(
                `http://localhost:8000/api/expenses/${selectedExpense.id}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                        Accept: "application/json",
                    },
                    body: JSON.stringify({
                        name: name,
                        amount: amount,
                        date: date,
                        category_id: category,
                    }),
                },
            );
            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 403) {
                    if (errorData.detail === "Admins cannot have expenses") {
                        errorMessage =
                            "Admins cannot have expenses. Please contact support for more information.";
                        goto("/login");
                    } else if (
                        errorData.detail === "User is not approved yet"
                    ) {
                        errorMessage =
                            "Your account has not been approved yet. Please wait for approval.";
                        goto("/pending-approval");
                    } else {
                        errorMessage = "You do not have access to this page.";
                        goto("/login");
                    }
                    showNotification(errorMessage, "error");
                } else if (response.status === 404) {
                    showNotification("Expense not found", "error");
                } else {
                    errorMessage = errorData.detail || "Failed to edit expense";
                    showNotification(errorMessage, "error");
                }
            } else {
                showNotification("Expense edited successfully", "success");
                await fetchExpenses();
            }
        } catch (error) {
            console.error("Error occurred while editing expense:", error);
            showNotification("Failed to edit expense", "error");
        }
        isProccessing = false;
    }

    function toggleWindowPopup(expense, popup) {
        selectedExpense = expense;
        popupType = popup;
        if (popup === " ") showPopupWindow = false;
        else showPopupWindow = true;
    }

    function toggleDeletionMode() {
        isDeletionMode = !isDeletionMode;
    }
</script>

<div class="action-button-container">
    <button
        class="action-button"
        on:click={() => toggleWindowPopup(null, "filter")}
    >
        <ListFilter />
    </button>
    <button
        class="action-button"
        on:click={() => toggleWindowPopup(null, "addExpense")}
    >
        <Plus />
    </button>
    <button class="action-button" on:click={toggleDeletionMode}>
        {#if isDeletionMode}
            <X />
        {:else}
            <Trash />
        {/if}
    </button>
</div>

{#if showPopupWindow}
    {#if popupType === "addExpense"}
        <AddWindowPopup
            onAdd={addExpense}
            onClose={() => toggleWindowPopup(null, " ")}
        />
    {:else if popupType === "deleteExpense"}
        <GeneralDeleteWindowPopup
            header="Delete expense?"
            label="Expense"
            data={selectedExpense.name}
            onDelete={deleteExpense}
            onClose={() => toggleWindowPopup(selectedExpense, " ")}
        />
    {:else if popupType === "editExpense"}
        <EditWindowPopup
            expense={selectedExpense}
            onEdit={editExpense}
            onClose={() => toggleWindowPopup(selectedExpense, " ")}
        />
    {:else if popupType === "filter"}
        <ExpenseFilterPanel
            applyFilter={fetchExpenses}
            toggleWindowPopup={() => toggleWindowPopup(selectedExpense, " ")}
            {filters}
        />
    {/if}
{/if}

{#if isProccessing}
    <div class="loading-circle"></div>
{:else if expenses.length === 0}
    <p>No expenses found.</p>
{:else}
    <div class="center-container">
        <div class="card-container">
            {#each expenses as expense}
                <ExpenseCard {expense} {isDeletionMode} {toggleWindowPopup} />
            {/each}
        </div>
    </div>
{/if}
