<script>
    export let toggleFilterMenu;
    export let applyFilter;

    let name = "";
    let ascending = true;

    function clearFilters() {
        name = "";
        ascending = true;
        applyFilter({ name, ascending });
        toggleFilterMenu();
    }

    const handleApplyFilters = () => {
        applyFilter({ name, ascending });
        toggleFilterMenu();
    };

    function toggleOrder(event) {
        ascending = event.target.value === "ascending";
    }

    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            handleApplyFilters();
        }
    };
</script>

<div class="filter-panel">
    <button class="close-btn" on:click={toggleFilterMenu}>&times;</button>

    <h2>Filter Categories</h2>

    <div>
        <input
            type="text"
            bind:value={name}
            placeholder="Enter category name"
            on:keydown={handleKeyPress}
        />
    </div>

    <div class="order-selector">
        <label>
            <input
                type="radio"
                name="order"
                value="ascending"
                checked={ascending}
                on:change={toggleOrder}
            />
            Ascending
        </label>
        <label>
            <input
                type="radio"
                name="order"
                value="descending"
                checked={!ascending}
                on:change={toggleOrder}
            />
            Descending
        </label>
    </div>

    <div class="buttons">
        <button class="filter-btn" on:click={handleApplyFilters}>Apply Filters</button>
        <button class="clear-btn" on:click={clearFilters}>Clear Filters</button>
    </div>
</div>

<style>
.order-selector {
    display: flex;
    align-items: left; 
    margin-bottom: 10px;
}

.order-selector label {
    display: flex;
    align-items: center; 
    margin-right: 20px; 
}

.order-selector input[type="radio"] {
    margin-right: 5px; 
}

.buttons {
    display: flex; 
    gap: 10px; 
    margin-top: 10px; 
}
</style>
