<script>
    import { Bitcoin, ShoppingBag } from 'lucide-svelte';
    import { onMount, onDestroy } from 'svelte';

    let basketX = 200; // Position of the basket
    let objectY = 0; // Vertical position of the falling object
    let objectX = Math.floor(Math.random() * 400); // Horizontal position of the object
    let score = 0;
    let isGameOver = false;
    let gameInterval;
    
    // Account approval status
    let isApproved = false; // Change this based on real approval status
    let approvalMessage = "Your account is pending approval. Feel free to play this mini-game in the meantime!";

    // Move basket left or right based on arrow keys
    function handleKeydown(event) {
        if (event.key === 'ArrowLeft' && basketX > 0) {
            basketX -= 20;
        } else if (event.key === 'ArrowRight' && basketX < window.innerWidth - 80) { // Adjust to window width
            basketX += 20; // Adjust so the basket doesn't go out of bounds
        }
    }

    // Function to drop the object
    function dropObject() {
        gameInterval = setInterval(() => {
            objectY += 5; // Move object down

            // Check if object reached the bottom
            if (objectY >= window.innerHeight - 100) { // Adjust to window height
                // Check if object is caught by the basket
                if (Math.abs(objectX - basketX) < 50) {
                    score += 1; // Increase score if object is caught
                    resetObject();
                } else {
                    isGameOver = true;
                    clearInterval(gameInterval); // Stop game if object hits the ground
                }
            }
        }, 50);
    }

    // Reset object position
    function resetObject() {
        objectY = 0;
        objectX = Math.floor(Math.random() * (window.innerWidth - 60)); // New random position for next object
    }

    // Restart the game
    function restartGame() {
        score = 0;
        isGameOver = false;
        resetObject();
        dropObject();
    }

    onMount(() => {
        window.addEventListener('keydown', handleKeydown);
        dropObject();
    });

    // Cleanup on unmount
    onDestroy(() => {
        clearInterval(gameInterval);
    });
</script>

<div class="center-container">
    <div class="game-container">
        {#if !isGameOver}
            <div class="falling-object" style="top: {objectY}px; left: {objectX}px;">
                <Bitcoin color="#fdd835" size="30"/>
            </div>
            <div class="basket" style="left: {basketX}px;">
                <ShoppingBag color="#d32f2f" size="60"/>
            </div>
            <p class="score">Score: {score}</p>
            {#if !isApproved}
                <p class="approval-message">{approvalMessage}</p>
            {/if}
        {/if}
        {#if isGameOver}
            <div class="game-over">
                <h1>Game Over!</h1>
                <p>Your score: {score}</p>
                <button on:click={restartGame}>Play Again</button>
            </div>
        {/if}
    </div>
</div>

<style>
    body {
        margin: 0;
        font-family: 'Arial', sans-serif;
        background-color: #1c1c1c;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
    }

    .game-container {
        position: relative;
        width: 90vw; /* Make width responsive */
        max-width: 400px; /* Max width for larger screens */
        height: 80vh; /* Responsive height */
        max-height: 500px; /* Max height */
        border: 2px solid #444;
        background-color: #121212;
        overflow: hidden;
        outline: none;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.8);
        border-radius: 10px;
    }

    .falling-object {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .basket {
        position: absolute;
        bottom: 10px;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .score, .approval-message {
        color: #fff;
        text-align: center;
        font-size: 24px;
        margin-top: 10px;
    }

    .game-over {
        text-align: center;
        color: #fff;
    }

    .game-over h1 {
        color: #e53935;
        font-size: 36px;
    }

    .game-over p {
        font-size: 20px;
    }

    .game-over button {
        padding: 10px 20px;
        background-color: #43a047;
        border: none;
        border-radius: 5px;
        color: white;
        font-size: 18px;
        cursor: pointer;
        margin-top: 20px;
    }

    .game-over button:hover {
        background-color: #388e3c;
    }

    /* Responsive styles */
    @media (max-width: 600px) {
        .score, .approval-message {
            font-size: 18px; /* Reduce font size on smaller screens */
        }

        .game-over h1 {
            font-size: 28px; /* Reduce font size for game over */
        }

        .game-over p {
            font-size: 18px; /* Reduce font size for game over message */
        }
    }
</style>
