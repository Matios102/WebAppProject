<script>
    export let user;
    export let team;
    export let onDelete;
    export let onClose;

    const handleDelete = (event) => {
        event.stopPropagation();
        if (onDelete) {
            onDelete(team, user);
        }
    };

    const handleClose = (event) => {
        event.stopPropagation();
        if (onClose) {
            onClose();
        }
    };
</script>

<div class="overlay">
    <div class="popup">
        <h2>Do you want delete this user from the team?</h2>
        <div class="user-details">
            <p><strong>Name:</strong> {user.name} {user.surname}</p>
            <p><strong>Email:</strong> {user.email}</p>
        </div>
    
        <div class="actions">
            <button class="delete-btn" on:click={handleDelete}>Delete</button>
            <button class="close-btn" on:click={handleClose}>Cancel</button>
        </div>
    </div>
</div>
