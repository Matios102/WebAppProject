<script>
    export let onEdit;
    export let onClose;
    export let categoryName;
    
    let newCategoryName = categoryName;

    function addCategory() {
        if (categoryName === newCategoryName) {
            onClose();
            return;
        }
        onEdit(newCategoryName); 
        onClose();
    }
    
</script>

<div class="overlay">
    <div class="popup">
        <h2>Edit Category</h2>
        <form on:submit|preventDefault={addCategory}>
            <input type="text" bind:value={newCategoryName} placeholder={categoryName} />
            <div class="actions">
                <button class="button green-btn">Edit</button>
                <button class="button cancel-btn" on:click={onClose}>Cancel</button>
            </div>
        </form>
    </div>
</div>