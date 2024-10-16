<script>
    export let toggleFilterMenu;
    export let applyFilter;
    export let filters;

    function clearFilters() {
        filters.fullName = '';
        filters.email = '';
        filters.role = '';
        filters.approved = false;
        filters.unapproved = false;
        applyFilter();
        toggleFilterMenu();
    }

    const handleApplyFilters = () => {
        applyFilter();
        toggleFilterMenu();
    };

    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            handleApplyFilters();
        }
    };
</script>


<div class="filter-panel">
    <button class="close-btn" on:click={toggleFilterMenu}>&times;</button>
    
    <h2>Filter Users</h2>
    
    <input type="text" bind:value={filters.fullName} on:keydown={handleKeyPress} placeholder="Enter full name" />
    <input type="email" bind:value={filters.email} on:keydown={handleKeyPress} placeholder="Enter email" />
    <select bind:value={filters.role} on:keydown={handleKeyPress}>
        <option value="" disabled selected>Select role</option>
        <option value="manager">Manager</option>
        <option value="user">User</option>
    </select>

    <label class="checkbox-label">
        <input type="checkbox" bind:checked={filters.approved} on:keydown={handleKeyPress}/>
        Approved
    </label>
    <label class="checkbox-label">
        <input type="checkbox" bind:checked={filters.unapproved} on:keydown={handleKeyPress} />
        Unapproved
    </label>

    <div class="actions">
        <button class="button filter-btn" on:click={handleApplyFilters}>Apply Filters</button>
        <button class="button clear-btn" on:click={clearFilters}>Clear Filters</button>
    </div>
</div>
