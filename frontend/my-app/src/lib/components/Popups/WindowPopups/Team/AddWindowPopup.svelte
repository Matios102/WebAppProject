<script>
    export let onAdd;
    export let onClose;

    let teamName = '';

    function addTeam() {
        onAdd(teamName);
        onClose();
    }
</script>

<div class="overlay">
    <div class="popup">
        <h2>Add Team</h2>
        <form on:submit|preventDefault={addTeam}>
            <input type="text" bind:value={teamName} placeholder="Team Name" />
            <div class="actions">
                <button class="button green-btn">Add</button>
                <button class="button cancel-btn" on:click={onClose}>Cancel</button>
            </div>
        </form>
    </div>
</div>