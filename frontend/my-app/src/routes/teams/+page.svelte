<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { checkToken, checkRole } from "$lib/utils/auth.js";
    import { showNotification } from "$lib/stores/popupStore.js";
    import TeamCard from "$lib/components/cards/TeamCard.svelte";
    import UserAddFilterPanel from "$lib/components/FilterPanels/UserAddFilterPanel.svelte";
    import GeneralDeletePopup from "$lib/components/Popups/WindowPopups/GeneralDeleteWidnowPopup.svelte";
    import AddWindowPopup from "$lib/components/Popups/WindowPopups/Team/AddWindowPopup.svelte";
    import { Plus, Trash, X } from 'lucide-svelte';

    //Data displayed
    let teams = [];

    //Popup
    let errorMessage = "";
    let showPopupWindow = false;
    let currentPopup = null;

    //User validation
    let isValid = false;
    let hasAccess = false;
    const expectedRoles = ["admin"];
    
    //User interaction
    let selectedTeam = null;
    let isDeletionMode = false;
    let selectedUser = null;

    //Awaiting data
    let isProcessing = true;

    onMount(async () => {
        isProcessing = true;
        const { isValid: valid, error } = await checkToken(); 
        if (!valid) {
            errorMessage = error;
            if (error === 'Your account is pending approval') {
                goto('/pending-approval');
            } else {
                goto('/login');
            }
        } 
        if(valid) {
            hasAccess = await checkRole(expectedRoles);
        }
        if (!hasAccess) {
            errorMessage = 'You do not have access to this page.';
            goto('/login')

        } else {
            isValid = true;
        }

        if(!isValid) {
            showNotification(errorMessage, 'error');
        }
        await fetchTeams();
        isProcessing = false;
    });


    //API calls
    async function fetchTeams() {
        isProcessing = true;
        try {
            const response = await fetch("http://localhost:8000/api/team/all", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
            });

            if (!response.ok) {
                errorData = await response.json();
                if(errorData.status === 403) {
                    errorMessage = "You do not have access to this page.";
                    showNotification(errorMessage, 'error');
                    goto('/login');
                } else {
                    errorMessage = errorData.detail || "Failed to fetch teams";
                    showNotification(errorMessage, 'error');
                }
            } else {
                teams = await response.json();
            }
        } catch (error) {
            console.error("Error fetching teams", error);
            showNotification("Failed to fetch teams", 'error');
        }
        isProcessing = false;
    }

    async function deleteUser() {
        isProcessing = true;
        try {
            const response = await fetch(
                `http://localhost:8000/api/team?user_id=${selectedUser.id}&team_id=${selectedTeam.team.id}`,
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
                    showNotification("You do not have permission to delete this user", "error");
                    goto("/login");
                } else if (response.status === 404) {
                    showNotification("User not found", "error");
                } else {
                    showNotification(errorData.detail || "Failed to delete user", "error");
                }
            } else {
                showNotification("User deleted successfully", "success");
                await fetchTeams();
            }
        } catch (error) {
            console.error("Error deleting user", error);
            showNotification("Failed to delete user", "error");
        }
        isProcessing = false;
    }

    async function addTeamMember() {
        isProcessing = true;
        try {
            const response = await fetch(
                `http://localhost:8000/api/team?user_id=${selectedUser.id}&team_id=${selectedTeam.team.id}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                },
            );

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 403) {
                    showNotification("You do not have permission to add this user", "error");
                    goto("/login");
                } else if (response.status === 404) {
                    showNotification("User not found", "error");
                } else if (response.status === 409) {
                    showNotification(errorData.detail, "error");
                } else {
                    showNotification(errorData.detail || "Failed to add user", "error");
                }
            } else {
                showNotification("User added successfully", "success");
                await fetchTeams();
            }
        } catch (error) {
            console.error("Error adding user", error);
            showNotification("Failed to add user", "error");
        }
        isProcessing = false;
    }

    async function deleteTeam() {
        isProcessing = true;
        let query = '';
        const params = new URLSearchParams();
        if(selectedTeam.team) params.append('team_id', selectedTeam.team.id);
        query = params.toString();

        try {
            const response = await fetch(`http://localhost:8000/api/team/delete?${query}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 403) {
                    showNotification("You do not have permission to delete this team", "error");
                    goto("/login");
                } else if (response.status === 404) {
                    showNotification("Team not found", "error");
                } else {
                    showNotification(errorData.detail || "Failed to delete team", "error");
                }
            } else {
                showNotification("Team deleted successfully", "success");
                await fetchTeams();
            }
        } catch (error) {
            console.error("Error deleting team", error);
            showNotification("Failed to delete team", "error");
        }
    }

    async function addTeam(teamName) {
        isProcessing = true;
        let query = '';

        const params = new URLSearchParams();
        if(teamName) params.append('team_name', teamName);
        query = params.toString();
        try {
            
            const response = await fetch(`http://localhost:8000/api/team/create?${query}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("authToken")}`,
                },
                body: JSON.stringify({ name: teamName }),
            });

            if (!response.ok) {
                errorData = await response.json();
                if(response.status === 403) {
                    errorMessage = "You do not have access to this page.";
                    showNotification(errorMessage, 'error');
                    goto('/login');
                } else {
                    errorMessage = errorData.detail || "Failed to add team";
                    showNotification(errorMessage, 'error');
                }
            } else {
                showNotification("Team added successfully", 'success');
                await fetchTeams();
            }
        } catch (error) {
            console.error("Error adding team", error);
            showNotification("Failed to add team", 'error');
        }
        isProcessing = false;
    }

    //Toggle deletion mode
    const toggleDeletionMode = () => {
        isDeletionMode = !isDeletionMode;
    };

    const toggleWidowPopup = (user, team, popup) => {
        selectedUser = user;
        selectedTeam = team;
        if(popup == '')
            showPopupWindow = false;
        else
            showPopupWindow = true;
        currentPopup = popup;
    };

    const handleAddUser = (user, team) => {
        selectedUser = user;
        selectedTeam = team;
        addTeamMember();
    }

</script>
<div class="action-button-container">
    <button class="action-button" on:click={() => toggleWidowPopup(null, null, 'addTeam')}>
        <Plus/>
    </button>
    
    <button class="action-button" on:click={toggleDeletionMode}>
        {#if isDeletionMode}
            <X />
        {:else}
            <Trash />
        {/if}
    </button>

</div>


{#if isProcessing}
    <div class="loading-circle"></div>
{:else}
<div class="center-container">
    <div class="team-container">
        {#each teams as team}
            <TeamCard
                team={team}
                users={team.users}
                manager={team.manager}
                isDeletionMode={isDeletionMode}
                toggleWidowPopup={toggleWidowPopup}
            />
        {/each}
    </div>
</div>
    
{/if}


{#if showPopupWindow}
    {#if currentPopup === 'deleteTeam'}
        <GeneralDeletePopup
            header="Delete this team?"
            label="Team"
            data={selectedTeam.team.name}
            onClose={() => toggleWidowPopup(null, null, '')}
            onDelete={deleteTeam}
        />
    {:else if currentPopup === 'deleteUser'}
        <GeneralDeletePopup
            header="Delete this user?"
            label="User"
            data="{selectedUser.name} {selectedUser.surname}"
            onClose={() => toggleWidowPopup(null, selectedTeam, '')}
            onDelete={deleteUser}
        />
    {:else if currentPopup === 'addUser'}
        <UserAddFilterPanel
            team={selectedTeam}
            toggleWidnowPopup={toggleWidowPopup}
            onAdd={handleAddUser}
        />
    {:else if currentPopup === 'addTeam'}
        <AddWindowPopup
            onAdd={addTeam}
            onClose={() => toggleWidowPopup(null, null, '')}
        />
    {/if}
{/if}
