<script>
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation';
    import {checkToken, checkRole} from '$lib/utils/auth.js';
    import {showNotification} from '$lib/stores/popupStore.js';
    import UserExpenseCard from '$lib/components/cards/UserExpenseCard.svelte';
    import { Download } from 'lucide-svelte';
    import saveAs from 'file-saver';
    import * as XLSX from 'xlsx';

    let hasAccess = false;
    let isProccessing = false;
    let userExpenses = [];

    const expectedRoles = ['manager'];

    onMount(async () => {
    isProccessing = true;
    const { isValid: valid, error } = await checkToken();

    if (!valid) {
      if (error === "Your account is pending approval") {
        showNotification("Your account is pending approval", "info");
        goto("/pending-approval");
        return;
      } else {
        showNotification("You do not have access to this page", "error");
          goto("/login");
          return;
        }
    }

    if (valid) {
      hasAccess = await checkRole(expectedRoles);
    }

    if (!hasAccess) {
      showNotification("You do not have access to this page", "error");
      goto("/login");
  
    } else {
      await fetchUserExpenses();
    }
    isProccessing = false;
  });

    async function fetchUserExpenses() {
        isProccessing = true;

        try {
            const response = await fetch("http://localhost:8000/api/team/expenses", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();

                if(response.status === 404){
                    showNotification("No team asigned", 'info');
                } else {
                    showNotification(errorData.message, 'error');
                }
            } else {
                const data = await response.json();
                userExpenses = Object.values(data);
            }

        } catch (error) {
            showNotification("Failed to fetch team", 'error');
        }
    }

    function handleDownload() {
        const data = userExpenses.map(user => {
            const row = {
                name: user.name,
                surname: user.surname,
                total: user.total_spendings,
                ...user.spendings_by_category
            };
            return row;
        });

        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Expenses");

        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
        saveAs(blob, 'user_expenses.xlsx');
    }

</script>

<div class="action-button-container">
    <button class="action-button" on:click={handleDownload}>
      <Download />
    </button>
</div>

{#if isProccessing}
    <div class="loading-circle"></div>
{:else}
    {#if userExpenses.length > 0}
    <div class="center-container">
        <div class="card-container">
          {#each userExpenses as user}
            <UserExpenseCard user={user}/>
          {/each}
        </div>
      </div>
    {:else}
        <p>No users found</p>
    {/if}
{/if}