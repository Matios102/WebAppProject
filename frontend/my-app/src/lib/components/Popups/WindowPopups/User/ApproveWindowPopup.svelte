<script>
    export let user;
    export let onApprove;
    export let onClose;

    const handleApprove = () => {
        if (onApprove) {
            onApprove(user);
            onClose(null, "");
        }
    };

    const handleClose = () => {
        if (onClose) {
            onClose(null, "");
        }
    };
</script>

<div class="overlay">
    <div class="popup">
        <h2>Approve this user?</h2>
        <div class="details">
            <p><strong>Name:</strong> {user.name} {user.surname}</p>
            <p><strong>Email:</strong> {user.email}</p>
        </div>
    
        <div class="actions">
            <button class="button green-btn" on:click={handleApprove}>Approve</button>
            <button class="button cancel-btn" on:click={handleClose}>Cancel</button>
        </div>
    </div>
</div>


