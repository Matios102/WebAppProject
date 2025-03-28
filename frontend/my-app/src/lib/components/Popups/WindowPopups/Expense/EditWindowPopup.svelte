<script>
    import { onMount } from "svelte";
    import { showNotification } from "$lib/stores/popupStore.js";

    export let onEdit;
    export let onClose;
    export let expense;

    let newExpenseName = expense.name;
    let newAmount = expense.amount;
    let newDate = expense.date;
    let newCategory = expense.category_name;
    let allCategories = [];

    onMount(async () => {
        await fetchCategories();
    });

    async function editExpense() {
        if (
            expense.name === newExpenseName &&
            expense.amount === newAmount &&
            expense.date === newDate &&
            expense.category_name === newCategory
        ) {
            onClose();
        }
        let categoryId = allCategories.find(
            (category) => category.name === newCategory,
        );
        onEdit(newExpenseName, newAmount, newDate, categoryId.id);
        onClose();
    }

    async function fetchCategories() {
        try {
            const response = await fetch(
                "http://localhost:8000/api/categories",
                {
                    method: "GET",
                    headers: {
                        Accept: "application/json",
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                },
            );

            if (!response.ok) {
                const errorData = await response.json();
                showNotification(
                    errorData.detail,
                    "error",
                );
            } else {
                allCategories = await response.json();
            }

        } catch (error) {
            showNotification("Failed to fetch categories.", "error");
        }
    }
</script>

<div class="overlay">
    <div class="popup">
        <h2>Edit Expense</h2>
        <form on:submit|preventDefault={editExpense}>
            <input
                type="text"
                bind:value={newExpenseName}
                placeholder={expense.name}
                required
            />
            <input
                type="number"
                bind:value={newAmount}
                placeholder={expense.amount}
                required
                min="0"
                step="0.01"
            />
            <input type="date" bind:value={newDate} required />
            <select bind:value={newCategory}>
                <option value={expense.category_name} selected
                    >{expense.category_name}</option
                >
                {#each allCategories.filter((category) => category.name !== expense.category_name) as category}
                    <option value={category.name}>{category.name}</option>
                {/each}
            </select>
            <div class="actions">
                <button type="submit" class="button green-btn">Edit</button>
                <button class="button cancel-btn" on:click={onClose}
                    >Cancel</button
                >
            </div>
        </form>
    </div>
</div>
