<script>
    import { goto } from '$app/navigation';
    import { showNotification } from '$lib/stores/popupStore.js';
  
    let name = '';
    let surname = '';
    let email = '';
    let password = '';
    
    let popupMessage = '';
    let popupType = '';

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }
  
    async function handleSubmit(event) {
        try {
            event.preventDefault();

            if (!validateEmail(email)) {
                popupMessage = 'Please enter a valid email address';
                popupType = 'error';
                showNotification(popupMessage, popupType);
                return;
            }
      
            const response = await fetch('http://localhost:8000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    name,
                    surname,
                    email,
                    password
                })
            });
        
            if (response.ok) {
                popupMessage = 'Registration successful';
                popupType = 'success';
                goto('/login');
            } else {
                const errorData = await response.json();
                popupMessage = errorData.detail || 'Registration failed';
                popupType = 'error';
            }
        } catch (error) {
            console.error('Error occurred during registration:', error);
            popupMessage = 'An error occurred. Please try again.';
            popupType = 'error';
        }
        showNotification(popupMessage, popupType);
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
      color: #d32f2f;
    }
  
    label {
      font-weight: bold;
      color: #d32f2f;
      display: block;
      margin-bottom: 0.5rem;
    }
  
    input {
      width: 100%;
      padding: 0.5rem;
      margin-bottom: 1rem;
      border: 1px solid #d32f2f;
      border-radius: 5px;
    }
  
    button {
      width: 100%;
      padding: 0.75rem;
      background-color: #d32f2f;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 1rem;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #b71c1c;
    }
  
    p {
      text-align: center;
      margin-top: 1rem;
    }
  
    a {
      color: #d32f2f;
      text-decoration: none;
    }
  
    a:hover {
      text-decoration: underline;
    }
  </style>
  
  <div class="container">
    <h1>Register</h1>
    <form on:submit|preventDefault={handleSubmit}>
      <div>
        <label for="name">First Name</label>
        <input type="text" id="name" bind:value={name} required />
      </div>
  
      <div>
        <label for="surname">Surname</label>
        <input type="text" id="surname" bind:value={surname} required />
      </div>
  
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" bind:value={email} required />
      </div>
  
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" bind:value={password} required />
      </div>
  
      <button type="submit">Register</button>
    </form>
  
    <p>Already have an account? <a href="/login">Login here</a>.</p>
  </div>
  