<script>
    export let onAdd;
    export let onClose;

    let categoryName = '';

    function addCategory() {
        onAdd(categoryName);
        onClose();
    }
    
</script>

<div class="overlay">
    <div class="popup">
        <h2>Add Category</h2>
        <form on:submit|preventDefault={addCategory}>
            <input type="text" bind:value={categoryName} placeholder="Category Name" required/>
            <div class="actions">
                <button class="button green-btn">Add</button>
                <button class="button cancel-btn" on:click={onClose}>Cancel</button>
            </div>
        </form>
    </div>
</div>