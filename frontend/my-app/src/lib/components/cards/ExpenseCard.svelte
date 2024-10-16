<script>
    export let expense;
    export let isDeletionMode;
    export let toggleWindowPopup;

    const handleClick = () => {
        if(isDeletionMode) {
            toggleWindowPopup(expense, 'deleteExpense');
        }
        else {
            toggleWindowPopup(expense, 'editExpense');
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
    <div>
        <div>
            <h3>{expense.name}</h3>
            <p>Amount: {expense.amount} PLN</p>
            <p>Category: {expense.category_name}</p>
            <p>Date: {expense.date}</p>
        </div>
    </div>
</button>

<style>
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


