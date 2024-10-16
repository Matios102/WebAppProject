<script>
    export let user;
    export let isDeletionMode;
    export let toggleWindowPopup;

    const handleClick = () => {
        if(isDeletionMode) {
            toggleWindowPopup(user, "delete");
        }
        else if (!user.is_approved) {
            toggleWindowPopup(user, "approve");
        } else {
            toggleWindowPopup(user, "edit");
        }
    };

    function randomDelay() {
        return `${Math.random() * 0.1}s`;
    }

    function randomDuration() {
        return `${0.3 + Math.random() * 0.1}s`;
    }
</script>

<button type="button" class="card {isDeletionMode ? 'shaking' : ''}" on:click={handleClick} aria-label="Card Button" style="--shake-delay: {randomDelay()}; --shake-duration: {randomDuration()};">
    <div class="user-card">
        <div class="user-info">
            <h3>{user.name} {user.surname}</h3>
            <p>{user.email}</p>
            <p>Role: {user.role}</p>
            <p>Status: {#if user.is_approved}<span class="approved">✔ Approved</span>{:else}<span class="unapproved">❗ Unapproved</span>{/if}</p>
        </div>
    </div>
</button>

<style>
    .approved {
        color: green;
    }

    .unapproved {
        color: red;
    }

    @keyframes rotate-shake {
        0%, 100% {
            transform: rotate(0deg);
        }
        25% {
            transform: rotate(-0.5deg);
        }
        75% {
            transform: rotate(0.5deg);
        }
    }

    .shaking {
        animation: rotate-shake var(--shake-duration, 0.5s) infinite;
        animation-delay: var(--shake-delay, 0s);
        transform-origin: center;
        border-color: rgb(255, 73, 73);
        background-color: #ffcdd1;
    }
</style>
