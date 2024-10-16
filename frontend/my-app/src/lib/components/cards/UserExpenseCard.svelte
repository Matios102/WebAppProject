<script>
    export let user;
</script>

<button type="button" class="card "  aria-label="Card Button">
    <div class="user-card">
        <div class="user-info">
            <h3>{user.name} {user.surname}</h3>
            <p>Total spendings: {user.total_spendings}</p>
        </div>
    </div>
</button>

