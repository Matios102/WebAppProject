<script>
    import { goto } from "$app/navigation";
</script>

<style>
    .welcome-body {
        margin: 0;
        font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        color: white; 
    }

    .welcome-container {
        text-align: center;
    }


    .welcome-button {
        margin-top: 20px;
        padding: 15px 30px;
        font-size: 1.5rem;
        color: #ff4b2b; 
        background-color: white; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    .welcome-button:hover {
        background-color: #f0f0f0;
        transform: scale(1.05);
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes slideIn {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes popIn {
        from {
            transform: scale(0.8);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
</style>

<div class="welcome-body">
    <div class="welcome-container">
        <h1>
            Welcome to Track That Dough
        </h1>
        <button class="welcome-button" on:click={() => {goto("/login")}}>
            Login
        </button>
    </div>
</div>
