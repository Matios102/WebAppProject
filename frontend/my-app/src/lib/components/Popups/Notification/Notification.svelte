<script>
    import { popupStore } from '$lib/stores/popupStore';
    import { onDestroy, onMount } from 'svelte';

    let popup;

    const unsubscribe = popupStore.subscribe(value => {
        popup = value;
    });

    let progressBarWidth = 100; 

    function updateProgressBar() {
        if (popup.isVisible) {
            const elapsedTime = Date.now() - popup.startTime; 
            progressBarWidth = Math.max(0, 100 - (elapsedTime / popup.duration) * 100); 

            if (elapsedTime >= popup.duration) {
                progressBarWidth = 100;
            }
        } else {
            progressBarWidth = 100; 
        }
    }

    let intervalId;

    onMount(() => {
        intervalId = setInterval(updateProgressBar, 100); 
    });

    onDestroy(() => {
        clearInterval(intervalId); 
        unsubscribe();
    });
</script>

<div class="notification {popup.type} {popup.isVisible ? 'is-visible' : ''}">
    <button class="close-btn" on:click={() => popup.isVisible = false}>&times;</button>
    <span>{popup.message}</span>
    <div class="progress-bar" style="width: {progressBarWidth}%"></div>
</div>

<style>
    .notification {
        position: fixed;
        top: 20px; 
        right: 20px;
        padding: 1rem;
        border-radius: 5px;
        z-index: 1000;
        transition: opacity 0.2s ease; 
        opacity: 0;
        visibility: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        min-width: 300px;
        max-width: 400px;
    }

    .notification.is-visible {
        opacity: 1;
        visibility: visible;
    }

    .success {
        background-color: #4caf50;
        color: white;
    }

    .error {
        background-color: #f44336;
        color: white;
    }

    .info {
        background-color: #007bff;
        color: white;
    }

    .close-btn {
        position: absolute; 
        top: 10px; 
        right: 10px; 
        background: transparent;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
    }

    .close-btn:hover {
        color: #ccc;
    }

    .progress-bar {
        height: 4px;
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 2px;
        margin-top: 0.5rem;
        transition: width 0.1s ease;
    }
</style>
