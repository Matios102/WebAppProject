<script>
    import { showNotification } from '$lib/stores/popupStore.js';

    let email = '';
    let popupMessage = '';
    let popupType = '';

    async function handleSubmit() {
        if (!validateEmail(email)) {
          showNotification("Invalid email address", "error");
            return;
        }

        try {
            let query = '';
            const urlParams = new URLSearchParams();
            if (email) urlParams.append('email', email);

            query = urlParams.toString();
            const response = await fetch(`http://localhost:8000/reset-password?${query}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                const data = await response.json();
                if(confirm(data.password)) {
                    window.location.href = "/login";
                }
            } else {
                const data = await response.json();
                showNotification(data.detail, "error");
            }
        } catch (error) {
          showNotification("Error sending reset email", "error");
        }
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }
</script>

  
<style>
      .container {
      max-width: 400px;
      margin: 100px auto;
      padding: 2rem;
      background-color: #f5f5f5;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
  
    h1 {
      text-align: center;
      color: #E74C3C;
    }
  
    label {
      font-weight: bold;
      color: #E74C3C;
      display: block;
      margin-bottom: 0.5rem;
    }
  
    input {
      width: 100%;
      box-sizing: border-box;
      padding: 0.5rem;
      margin-bottom: 1rem;
      border: 1px solid #E74C3C;
      border-radius: 5px;
    }
  
    button {
      width: 100%;
      padding: 0.75rem;
      background-color: #E74C3C;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 1rem;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #95361F;
    }
  
  
    p {
      text-align: center;
      margin-top: 1rem;
    }
  
    a {
      color: #E74C3C;
      text-decoration: none;
    }
  
    a:hover {
      text-decoration: underline;
    }
</style>

  <div class="container">
    <h1>Reset password</h1>
    <form on:submit|preventDefault={handleSubmit}>
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" bind:value={email} required />
        </div>
        <button type="submit">Reset password</button>

        <br><br>
        <a href="/login">Back to login</a>
    </form>

</div>
