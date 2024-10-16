<script>
    export let header;
    export let label;
    export let data;
    export let onDelete;
    export let onClose;


    const handleDelete = () => {
        if (onDelete) {
            onDelete();
            onClose();
        }
    };

    const handleClose = () => {
        if (onClose) {
            onClose();
        }
    };

</script>
<div class="overlay">
    <div class="popup ">
        <h2>{header}</h2>
        <div class="details">
            <p><strong>{label}: </strong>{data}</p>
        </div>
        <div class="actions">
            <button class="button red-btn" on:click={handleDelete}>Delete</button>
            <button class="button cancel-btn" on:click={handleClose}>Cancel</button>
        </div>
    </div>
</div>
