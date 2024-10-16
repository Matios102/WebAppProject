<script>
    import { onMount } from "svelte";
    export let toggleWindowPopup;
    export let applyFilter;
    export let filters;

    let allCategories = [];

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
                if (response.status === 403) {
                    showNotification("Your account has not been approved", "error");
                    goto("/pending-approval");
                } else {
                    showNotification(errorData.detail || "An error occurred. Please try again.", "error");
                }
            } else {
                allCategories = await response.json();
            }
        } catch (error) {
            console.error("Error occurred while fetching categories:", error);
            showNotification("Failed to fetch categories.", "error");
        }
    }

    onMount(async () => {
        await fetchCategories();
    });

    function clearFilters() {
        filters.expenseName = "";
        filters.expenseAmount = "";
        filters.expenseDate = "";
        filters.expenseCategory = "";
        applyFilter();
        toggleWindowPopup();
    }

    const handleApplyFilters = () => {
        applyFilter();
        toggleWindowPopup();
    };

    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            handleApplyFilters();
        }
    };
</script>


<div class="filter-panel">
    <button class="close-btn" on:click={toggleWindowPopup}>&times;</button>
    
    <h2>Filter Expenses</h2>
    
    <div>
        <input type="text" bind:value={filters.expenseName} on:keydown={handleKeyPress} placeholder="Enter expense name" />
        <input type="number" bind:value={filters.expenseAmount} on:keydown={handleKeyPress} placeholder="Enter expense amount" />
        <input type="date" bind:value={filters.expenseDate} on:keydown={handleKeyPress} placeholder="Enter expense date" />
        <select bind:value={filters.expenseCategory} on:keydown={handleKeyPress}>
            <option value="">Select Category</option>
            {#each allCategories as category}
                <option value={category.id}>{category.name}</option>
            {/each}
        </select>
        
    </div>

    <div class="buttons">
        <button class="filter-btn" on:click={handleApplyFilters}>Apply Filters</button>
        <button class="clear-btn" on:click={clearFilters}>Clear Filters</button>
    </div>
</div>
