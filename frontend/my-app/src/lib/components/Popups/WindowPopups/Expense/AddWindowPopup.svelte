<script>
    import { onMount } from "svelte";
    import { showNotification } from "$lib/stores/popupStore.js";

    export let onAdd;
    export let onClose;

    let expenseName;
    let amount;
    let date;
    let category;
    let allCategories = [];

    onMount(async () => {
        await fetchCategories();
    });

    async function fetchCategories () {
        try {
            const response = await fetch('http://localhost:8000/api/categories', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 403) {
                    showNotification('You do not have permission to fetch categories', 'error');
                    goto('/login');
                } else {
                    showNotification(errorData.detail || 'An error occurred. Please try again.', 'error');
                }
            } else {
                allCategories = await response.json();
            }
        } catch (error) {
            console.error('Error occurred while fetching categories:', error);
            showNotification('Failed to fetch categories.', 'error');
        }
    }

    function addExpense() {
        onAdd(expenseName, amount, date, category);
        onClose();
    }
</script>

<div class="overlay">
    <div class="popup">
        <h2>Add Expense</h2>
        <form on:submit|preventDefault={addExpense}>
            <input type="text" bind:value={expenseName} placeholder="Expense Name" required/>
            <input type="number" bind:value={amount} placeholder="Amount" required/>
            <input type="date" bind:value={date} placeholder="Date" required/>
            <select bind:value={category}>
                <option value="">Select Category</option>
                {#each allCategories as category}
                    <option value={category.id}>{category.name}</option>
                {/each}
            </select>
            <div class="actions">
                <button type="submit" class="button green-btn">Add</button>
                <button class="button cancel-btn" on:click={onClose}>Cancel</button>
            </div>
        </form>
    </div>
</div>