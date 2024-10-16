<script>
    export let user;
    export let onClose;
    export let changeUserRole;

    let newRole = user.role === 'manager' ? 'user' : 'manager';

    const handleRoleChange = () => {
        if (changeUserRole) {
            changeUserRole(user, newRole);
            onClose(null, "");
        }
    };

    const handleCancel = () => {
        if (onClose) {
            onClose(null, "");
        }
    };

</script>

<div class="overlay">
    <div class="popup">
        <h2>Edit User Information</h2>
        <div class="details">
            <p><strong>Name:</strong> {user.name} {user.surname}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Current Role:</strong> {user.role}</p>
        </div>
        <div class="actions">
            <button class="button yellow-btn" on:click={handleRoleChange}>
                Change Role to {newRole}
            </button>
            <button class="button cancel-btn" on:click={handleCancel}>
                Cancel
            </button>
        </div>
    </div>
</div>
