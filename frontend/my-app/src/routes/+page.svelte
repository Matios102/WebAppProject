<script>
    import { goto } from "$app/navigation";
    import { ArrowDown } from 'lucide-svelte';
</script>

<style>
    body {
        margin: 0;
        background: white;
        color: #333;
        line-height: 1.6;
    }

    .welcome-body {
        margin: 0;
        background: linear-gradient(135deg, #E74C3C, #FF6F61);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white; 
        position: relative;
        flex-direction: column;
    }

    .welcome-container {
        text-align: center;
        animation: fadeIn 1s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        position: relative;
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

    .info-section, .about-section {
        padding: 50px 20px;
        text-align: center;
    }

    .info-section {
        background-color: #f9f9f9;
    }

    .about-section {
        background-color: #f4f4f4;
    }

    h1, h2 {
        margin-bottom: 20px;
    }

    p {
        max-width: 800px;
        margin: 0 auto 20px;
        font-size: 1.1rem;
        color: #555;
    }

    .scroll-down {
        font-size: 1rem;
        color: white;
        cursor: pointer;
        margin-top: 30px;
        animation: bounce 2s infinite;
        background: none;
        border: none;
        position: absolute;
        bottom: 20px;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }

</style>

<div class="welcome-body">
    <div class="welcome-container">
        <h1>Welcome to Track That Dough</h1>
        <button class="welcome-button" on:click={() => {goto("/login")}}>
            Login
        </button>
        <button class="scroll-down" on:click={() => window.scrollTo({top: window.innerHeight, behavior: 'smooth'})} aria-label="Scroll down to learn more">
            <ArrowDown/>
        </button>
    </div>
</div>

<div class="info-section">
    <h2>What is Track That Dough?</h2>
    <p>
        Track That Dough is an innovative financial management tool designed to help you keep track of your income and expenses effortlessly. With our intuitive interface and powerful analytics, you'll gain insights into your spending habit and achieve your financial goals.
    </p>
</div>

<div class="about-section">
    <h2>About Me</h2>
    <p>
        Hi! I'm the creator of Track That Dough. My goal is to make personal finance easier for everyone, helping you make informed financial decisions and reach your savings targets. Track That Dough was built with simplicity in mind, allowing you to stay on top of your finances without the hassle.
    </p>
</div>
