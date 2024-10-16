<script>
    import { showNotification } from '$lib/stores/popupStore';
    import Notification from '../lib/components/Popups/Notification/Notification.svelte';

    function handleClick1() {
        showNotification('This is a success message!', 'success');
    }

    function handleClick2() {
        showNotification('This is an error message!', 'error');
    }
</script>

<button on:click={handleClick1}>Show Popup</button>
<button on:click={handleClick2}>Show Error Popup</button>
<Notification />