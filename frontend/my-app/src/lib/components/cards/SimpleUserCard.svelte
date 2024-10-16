<script>
    export let user;
    export let isSelected = false; 
    export let selectUser;
</script>

<button type="button" class="card {isSelected ? 'selected' : ''}" aria-label="Card Button" on:click={selectUser}>
    <div class="user-card">
        <div class="user-info">
            <h3>{user.name} {user.surname}</h3>
            <p>{user.email}</p>
        </div>
    </div>
</button>

<style>
    .selected {
        border-color: #007BFF;
        background-color: #e0f7ff;
    }


</style>
