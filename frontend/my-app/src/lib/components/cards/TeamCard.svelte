<script>
    import { ChevronRight, ChevronDown, Plus } from 'lucide-svelte';

    export let users = [];
    export let manager;
    export let team;
    export let toggleWidowPopup;
    export let isDeletionMode;

    let isExpanded = false;

    const toggleCollapse = () => {
        if (isDeletionMode) {
            toggleWidowPopup(null, team, 'deleteTeam');
        } else {
            toggleWidowPopup(null, team, '');
            isExpanded = !isExpanded;
        }
    };

    const handleUserClick = (event, team, user) => {
        event.stopPropagation();
        toggleWidowPopup(user, team, 'deleteUser');
    };

    const handleAddClick = (event, team) => {
        event.stopPropagation();
        toggleWidowPopup(null, team, 'addUser');
    };

    function randomDelay() {
        return `${Math.random() * 0.1}s`;
    }

    function randomDuration() {
        return `${0.4 + Math.random() * 0.1}s`;
    }

</script>

<!-- Team Card -->
<button
    class="team-card {isDeletionMode ? 'shaking' : ''}"
    on:click={toggleCollapse}
    style="--shake-delay: {randomDelay()}; --shake-duration: {randomDuration()};"
>
    <div class="team-header">
        <div class="team-info">
            <h3>{team.team.name}</h3>
        </div>
        {#if isExpanded} <ChevronDown/> {:else} <ChevronRight/> {/if}
    </div>

    <div class="collapsible-content {isExpanded && !isDeletionMode ? 'expanded' : ''}">
        <div class="center-container">
            <div class="card-container">
                <!-- Manager Card -->
                {#if manager !== null}
                    <button 
                        type="button" 
                        class="card-fixed" 
                        on:click={(event) => handleUserClick(event, team, manager)} 
                        aria-label="Card Button"
                    >
                        <div class="user-card">
                            <div class="user-info">
                                <h3>{manager.name} {manager.surname}</h3>
                                <p>{manager.email}</p>
                                <p>Role: {manager.role}</p>
                            </div>
                        </div>
                    </button>
                {/if}
                

                <!-- User Cards -->
                 {#if users.length > 0}
                    {#each users as user}
                        <button 
                            type="button" 
                            class="card-fixed" 
                            on:click={(event) => handleUserClick(event, team, user)} 
                            aria-label="Card Button"
                            >
                            <div class="user-card">
                                <div class="user-info">
                                    <h3>{user.name} {user.surname}</h3>
                                    <p>{user.email}</p>
                                    <p>Role: {user.role}</p>
                                </div>
                            </div>
                        </button>
                    {/each}
                {/if}
                
                <!-- Add Team Member Button -->
                <button 
                    type="button" 
                    class="add-card" 
                    on:click={(event) => handleAddClick(event, team)} 
                    aria-label="Card Button"
                >
                    <div class="user-card">
                        <div class="user-info">
                            <Plus size="24" />
                        </div>
                    </div>
                </button>
            </div>
        </div>
    </div>
</button>

<style>
@keyframes rotate-shake {
    0%, 100% {
        transform: rotate(0deg);
    }
    25% {
        transform: rotate(-0.3deg);
    }
    75% {
        transform: rotate(0.3deg);
    }
}

.shaking {
    animation: rotate-shake var(--shake-duration, 0.5s) infinite;
    animation-delay: var(--shake-delay, 0s);
    transform-origin: center;
    border-color: rgb(255, 73, 73);
    background-color: #ffcdd1;
}
</style>


