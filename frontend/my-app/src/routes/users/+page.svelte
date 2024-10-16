<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { showNotification } from "$lib/stores/popupStore.js";
  import { checkToken, checkRole } from "$lib/utils/auth.js";
  import { SlidersHorizontal, Trash, X } from "lucide-svelte";
  import GeneralDeleteWidnowPopup from "$lib/components/Popups/WindowPopups/GeneralDeleteWidnowPopup.svelte";
  import ApproveWindowPopup from "$lib/components/Popups/WindowPopups/User/ApproveWindowPopup.svelte";
  import EditWindowPopup from "$lib/components/Popups/WindowPopups/User/EditWindowPopup.svelte";
  import UserCard from "$lib/components/cards/UserCard.svelte";
  import UserFilterPanel from "$lib/components/FilterPanels/UserFilterPanel.svelte";

  //Data displayed
  let users = [];

  //User validation
  let isValid = false;
  let hasAccess = false;
  const expectedRoles = ["admin"];

  //Popup
  let errorMessage = "";

  //Popup windows
  let showWindowPopup = false;
  let currentPopup = null;

  //User interaction
  let isFiltersOpen = false;
  let isProccessing = true;
  let isDeletionMode = false;
  let selectedUser = null;
  let filters = {};


  onMount(async () => {
    isProccessing = true;
    const { isValid: valid, error } = await checkToken();

    if (!valid) {
      errorMessage = error;
      if (error === "Your account is pending approval") {
        goto("/pending-approval");
      } else {
          goto("/login");
        }
    }

    if (valid) {
      hasAccess = await checkRole(expectedRoles);
    }

    if (!hasAccess) {
      errorMessage = "You do not have access to this page.";
      goto("/login");
  
    } else {
      isValid = true;
      await fetchUsers();
    }

    if (!isValid) {
      showNotification(errorMessage, "error");
    }
    isProccessing = false;
  });

  //API calls
  async function fetchUsers() {
    isProccessing = true;
    let queryParams = "";
    const params = new URLSearchParams();

    if (filters.approved && filters.unapproved) {
      // No need to append status if both are true
    } else if (filters.approved) {
      params.append("status", "approved");
    } else if (filters.unapproved) {
      params.append("status", "unapproved");
    }

    if (filters.email) params.append("email", filters.email);
    if (filters.fullName) params.append("name_or_surname", filters.fullName);
    if (filters.role) params.append("role", filters.role);

    queryParams = params.toString();

    try {
      const response = await fetch(
        `http://localhost:8000/api/users/?${queryParams}`,
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
          showNotification("You do not have permission to approve this user", "error");
          goto("/login");
        } else {
          errorMessage = errorData.detail || "Failed to fetch users";
          showNotification(errorMessage, "error");
        }
      } else {
        users = await response.json();
      }
    } catch (error) {
      console.error("Error fetching users: ", error);
      showNotification("Failed to fetch users", "error");
    }
    isProccessing = false;
  }

  async function approveUser() {
    isProccessing = true;
    try {
      const response = await fetch(
        `http://localhost:8000/api/users/approve/${selectedUser.id}`,
        {
          method: "PUT",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
        },
      );
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 403) {
          showNotification("You do not have permission to approve this user", "error");
        } else if (response.status === 404) {
          showNotification("User not found", "error");
        } else {
          showNotification(errorData.detail || "Failed to approve user", "error");
        }
      } else {
        showNotification("User approved successfully", "success");
        await fetchUsers();
      }

    } catch (error) {
      console.error("Error approving user: ", error);
      showNotification("Failed to approve user", "error");
    }
    isProccessing = false;
  }

  async function deleteUser() {
    isProccessing = true;
    try {
      const response = await fetch(
        `http://localhost:8000/api/users/${selectedUser.id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
        },
      );
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 403) {
          showNotification("You do not have permission to approve this user", "error");
        } else if (response.status === 404) {
          showNotification("User not found", "error");
        } else {
          showNotification(errorData.detail || "Failed to approve user", "error");
        }
      } else {
        showNotification("User deleted successfully", "success");
        await fetchUsers();
      }

    } catch (error) {
      console.error("Error deleting user: ", error);
      showNotification("Failed to delete user", "error");
    }
    isProccessing = false;
  }


  async function changeUserRole() {
    isProccessing = true;
    try {
      const response = await fetch(
        `http://localhost:8000/api/users/change-role/${selectedUser.id}`,
        {
          method: "PUT",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
        },
      );
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 403) {
          showNotification("You do not have permission to change this user's role", "error");
        } else if (response.status === 404) {
          showNotification("User not found", "error");
        } else if (response.status === 409) {
          showNotification("User's team already has a manager", "error");
        } else {
          showNotification(errorData.detail || "Failed to change user's role", "error");
        }
      } else {
        showNotification("User role changed successfully", "success");
        await fetchUsers();
      }
    } catch (error) {
      console.error("Error changing user's role: ", error);
      showNotification("Failed to change user's user", "error");
    }
    isProccessing = false;
  }

  //User interaction
  function toggleFilters() {
    isFiltersOpen = !isFiltersOpen;
  }

  function toggleDeletionMode() {
    isDeletionMode = !isDeletionMode;
  }


  function toggleWidnowPopup(user, popup) {
    selectedUser = user;

    if(popup === "")
      showWindowPopup = false;
    else
      showWindowPopup = true;

    currentPopup = popup;
  }

  
</script>


{#if showWindowPopup}
  {#if currentPopup == UserFilterPanel}
    <UserFilterPanel
      applyFilter={fetchUsers}
      isOpen={isFiltersOpen}
      toggleFilterMenu={toggleFilters}
    />
  {:else if currentPopup == "delete"}
    <GeneralDeleteWidnowPopup
      header="Delete this user?"
      label="User" 
      data="{selectedUser.name} {selectedUser.surname}"
      onDelete={deleteUser}
      onClose={() => toggleWidnowPopup(null, "")}
    />
  {:else if currentPopup == "approve"}
    <ApproveWindowPopup user={selectedUser} onClose={toggleWidnowPopup} onApprove={approveUser} />

  {:else if currentPopup == "edit"}
    <EditWindowPopup user={selectedUser} onClose={toggleWidnowPopup} changeUserRole={changeUserRole} />
  {:else if currentPopup == "filter"}
    <UserFilterPanel
      applyFilter={fetchUsers}
      toggleFilterMenu={() => toggleWidnowPopup(null, "")}
      filters={filters}
    />
    {/if}
{/if}


 
<div class="action-button-container">
  <button class="action-button" on:click={() => toggleWidnowPopup(null, "filter")}>
    <SlidersHorizontal />
  </button>
  <button class="action-button" on:click={toggleDeletionMode}>
    {#if isDeletionMode}
      <X />
    {:else}
      <Trash />
    {/if}
  </button>
</div>

{#if isProccessing}
  <div class="loading-circle"></div>
{:else if users.length === 0}
  <p>No users found.</p>
{:else}
  <div class="center-container">
    <div class="card-container">
      {#each users as user}
        <UserCard user={user} isDeletionMode={isDeletionMode} toggleWindowPopup={toggleWidnowPopup} />
      {/each}
    </div>
  </div>
{/if}
