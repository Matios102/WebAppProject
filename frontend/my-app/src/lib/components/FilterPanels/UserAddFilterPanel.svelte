<script>
    import { onMount } from "svelte";
    import SimpleUserCard from "$lib/components/cards/SimpleUserCard.svelte";
    
    export let team;
    export let toggleWidnowPopup;
    export let onAdd;

    let fullName = '';
    let users = [];
    let selectedUser = null;
    let isProcessing = false;

    async function fetchUsersWithoutTeam(filters = {}) {
        isProcessing = true;
        let query = '';
        const params = new URLSearchParams();
        if (filters.fullName) params.append("fullName", filters.fullName);

        query = params.toString();
        try {
            const response = await fetch(`http://localhost:8000/api/team/users?${query}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                if(response.status === 403) {
                    showNotification('You do not have permission to fetch users', 'error');
                    goto('/login');
                } else {
                    showNotification(errorData.detail || 'An error occurred. Please try again.', 'error');
                }
            } else {
                users = await response.json();
            }
        } catch (error) {
            console.error('Error occurred while fetching users:', error);
            showNotification('Failed to fetch users.', 'error');
        }
        isProcessing = false;
    }

    onMount(async () => {
        await fetchUsersWithoutTeam({ fullName });
    });

    function clearFilters() {
        fullName = '';
        fetchUsersWithoutTeam();
    }

    const handleAddUser = () => {
        if (selectedUser) {
            onAdd(selectedUser, team);
        }
        toggleWidnowPopup(null, team, '');
    };

    const handleKeyPress = async (event) => {
        if (event.key === "Enter") {
            users = await fetchUsersWithoutTeam({ fullName });
        }
    };

    const handleUserClicker = (user) => {
        selectedUser = user;
    };
</script>

<!-- Filter Panel -->
<div class="filter-panel">
    <button class="close-btn" on:click={toggleWidnowPopup(null, team ,'')}>&times;</button>

    <h2>Filter Users</h2>

    <div>
        <input type="text" bind:value={fullName} on:keydown={handleKeyPress} placeholder="Enter full name" />
    </div>

    <!-- User List -->
    <div class="user-list scrollable">
        {#if isProcessing}
            <div class="loading-circle"></div>
        
        {:else}
            {#if users.length === 0 && !isProcessing}
                <p>No users found</p>
            {:else}
            {#each users as user}
                <SimpleUserCard
                    user={user}
                    selectUser={() => handleUserClicker(user)}
                    isSelected={user === selectedUser}
                />
            {/each}
            {/if}
        {/if}
    </div>

    <div class="actions">
        <button class="button green-btn" on:click={handleAddUser}>Add User</button>
        <button class="button clear-btn" on:click={clearFilters}>Clear Filters</button>
    </div>
</div>

<style>
    .user-list {
        max-height: 200px;
        overflow-y: auto;
    }

    .user-list.scrollable::-webkit-scrollbar {
        width: 6px;
    }

    .user-list.scrollable::-webkit-scrollbar-thumb {
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 3px;
    }
</style>
