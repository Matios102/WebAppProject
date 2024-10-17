export async function checkToken() {
    const token = localStorage.getItem('authToken');
    if (!token) {
        return { isValid: false, error: 'No token found' }; 
    }
    
    try {
        const response = await fetch(`http://localhost:8000/check-token`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: token }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('userRole', data.role);
            if(data.is_approved === false) {
                return { isValid: false, error: 'Your account is pending approval'};
            }
            return { isValid: true, error: '' }; 
        } else if (response.status === 401) {
            return { isValid: false, error: 'Invalid token' }; 
        } else {
            const errorMessage = 'An error occurred, please try again later'; 
            const errorDar = await response.json();
            console.log(errorDar);
            return { isValid: false, error: errorMessage }; 
        }
    } catch (error) {
        console.log(error);
        const errorMessage = 'An error occurred, please try again later';
        return { isValid: false, error: errorMessage };
    }
}


export async function checkRole(expectedRoles) {
    const userRole = localStorage.getItem('userRole');
    if (!userRole) {
        return false;
    }

    const isRoleValid = Array.isArray(expectedRoles) 
        ? expectedRoles.includes(userRole) 
        : expectedRoles.has(userRole);

    if (!isRoleValid) {
        return false;
    }

    return true;
}