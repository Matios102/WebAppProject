<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import {checkToken} from '$lib/utils/auth.js';
    import { showNotification } from '$lib/stores/popupStore';

    let email = '';
    let password = '';
    let popupMessage = '';
    let popupType = '';

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (!validateEmail(email)) {
            popupMessage = 'Please enter a valid email address';
            popupType = 'error';
            showNotification(popupMessage, popupType);
            return;
        }
      
        try {
            const formData = new URLSearchParams();
            formData.append('grant_type', 'password');
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch('http://localhost:8000/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('authToken', data.access_token);
                localStorage.setItem('userRole', data.role);
                popupMessage = 'Login successful';
                popupType = 'success';
                if(data.role === 'admin') {
                    goto('/users');
                } else {
                  goto('/dashboard');
                }
            } else {
                const errorData = await response.json();
                popupMessage = errorData.detail || 'Invalid credentials';
                popupType = 'error';
            }
        } catch (error) {
            console.error('Error occurred during login:', error);
            popupMessage = 'An error occurred. Please try again.';
            popupType = 'error';
        }
        
        showNotification(popupMessage, popupType);
    }

    onMount(async () => {
      const { isValid: valid, error } = await checkToken();
        
        if (valid) {
            const userRole = localStorage.getItem('userRole');
            if (userRole === 'admin') {
                goto('/users'); 
            } else {
                goto('/dashboard');
            }
        }
      
    });
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
      box-sizing: border-box;
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
    <h1>Login</h1>
    <form on:submit|preventDefault={handleSubmit}>
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" bind:value={email} required />
        </div>
        <div>
            <label for="password">Password</label>
            <input type="password" id="password" bind:value={password} required />
        </div>
        <a href="/password-reset">Forgot password?</a>
        <br><br>
        <button type="submit">Login</button>
    </form>

    <p>Don't have an account? <a href="/register">Register here</a>.</p>
</div>
