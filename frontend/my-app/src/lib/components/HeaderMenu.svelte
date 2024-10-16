<script>
    import { goto } from '$app/navigation';
    import { showNotification } from '$lib/stores/popupStore';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { AlignJustify, X } from 'lucide-svelte';
    
    let activeTab = '';
    let userRole = '';
    let isMenuCollapsed = true; // State for menu collapsing

    $: {
        const path = $page.url.pathname;
        activeTab = path.substring(1);
    }

    onMount(() => {
        userRole = localStorage.getItem('userRole');
    });

    function navigateTo(path) {
        goto(path);
        isMenuCollapsed = true; // Close the menu after navigating
    }

    function toggleMenu() {
        isMenuCollapsed = !isMenuCollapsed;
    }

    function logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userRole');
        showNotification('You have been logged out successfully', 'success');
        goto('/login');
    }
</script>

<style>
    .header {
        display: flex;
        justify-content: center;
        background-color: #d32f2f;
        padding: 1rem;
        width: 100%;
        box-sizing: border-box;
        position: relative;
        transition: height 0.3s ease;
        z-index: 1000;
    }

    .tab-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .tab {
        margin: 0 20px;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #fff;
        background-color: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
        outline: none;
    }

    .active {
        border-bottom: 3px solid #fff;
    }

    .tab:hover {
        color: #9d2f2f;
    }

    .tab:active {
        transform: scale(0.95);
    }

    /* Button for toggling the menu on small screens */
    .menu-toggle {
        background-color: #d32f2f;
        color: white;
        font-size: 1.5rem;
        border: none;
        cursor: pointer;
        position: absolute;
        top: 1rem;
        left: 1rem;
        display: none;
    }

    /* Display the menu-toggle button on small screens */
    @media (max-width: 768px) {
        .menu-toggle {
            display: block;
        }

        /* When the menu is collapsed, the header should be 57px high */
        .header {
            height: 57px;
            transition: height 0.3s ease;
        }

        /* When the menu is expanded, increase the header height */
        .header.expanded {
            height: auto;
        }

        .tab-container {
            display: none; /* Hide tabs initially */
            flex-direction: column;
            align-items: center;
            width: 100%;
        }

        .tab {
            margin: 10px 0;
            width: 100%;
            text-align: center;
        }

        /* When the menu is expanded, show the tabs */
        .tab-container.show {
            display: flex;
        }
    }
</style>


{#if userRole === 'admin' || userRole === 'manager' || userRole === 'user'}
    <div class="header {isMenuCollapsed ? '' : 'expanded'}">
        <!-- Button for toggling the menu on small screens -->
        <button class="menu-toggle" on:click={toggleMenu}>
            {#if isMenuCollapsed}
                <AlignJustify />
            {:else}
                <X />
            {/if}
        </button>

        <div class="tab-container {isMenuCollapsed ? '' : 'show'}">
            {#if userRole === 'admin'}
                <button 
                    class="tab {activeTab === 'users' ? 'active' : ''}" 
                    on:click={() => navigateTo('users')}
                    role="tab">
                    Users
                </button>
                <button 
                    class="tab {activeTab === 'teams' ? 'active' : ''}" 
                    on:click={() => navigateTo('teams')}
                    role="tab">
                    Teams
                </button>
                <button 
                    class="tab {activeTab === 'categories' ? 'active' : ''}" 
                    on:click={() => navigateTo('categories')}
                    role="tab">
                    Categories
                </button>
            {/if}

            {#if userRole === 'manager'}
                <button 
                    class="tab {activeTab === 'dashboard' ? 'active' : ''}" 
                    on:click={() => navigateTo('dashboard')}
                    role="tab">
                    Dashboard
                </button>
                <button 
                    class="tab {activeTab === 'expenses' ? 'active' : ''}" 
                    on:click={() => navigateTo('expenses')}
                    role="tab">
                    Expenses
                </button>
                <button 
                    class="tab {activeTab === 'my_team' ? 'active' : ''}" 
                    on:click={() => navigateTo('my_team')}
                    role="tab">
                    My Team
                </button>
            {/if}

            {#if userRole === 'user'}
                <button 
                    class="tab {activeTab === 'dashboard' ? 'active' : ''}" 
                    on:click={() => navigateTo('dashboard')}
                    role="tab">
                    Dashboard
                </button>
                <button 
                    class="tab {activeTab === 'expenses' ? 'active' : ''}" 
                    on:click={() => navigateTo('expenses')}
                    role="tab">
                    Expenses
                </button>
            {/if}

            <button 
                class="tab {activeTab === 'logout' ? 'active' : ''}" 
                on:click={() => logout()}
                role="tab">
                Logout
            </button>
        </div>
    </div>
{/if}
