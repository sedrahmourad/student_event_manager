// Base API URL. Update this if your API prefix changes.
const API_BASE_URL = '/api/users/';

/**
 * Handles basic response checking and error display.
 * @param {Response} response - The fetch API Response object.
 * @returns {Promise<any>} The JSON data if successful.
 * @throws {Error} If the HTTP status is not OK (200-299).
 */
async function checkResponse(response) {
    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            // Handle case where response body is not valid JSON (e.g., 500 error page)
            throw new Error(`HTTP error! Status: ${response.status}. Could not parse JSON error body.`);
        }
        // Extract a meaningful error message from DRF's common formats
        const errorMessage = errorData.detail || 
                             (errorData.non_field_errors && errorData.non_field_errors[0]) ||
                             (errorData.email && errorData.email[0]) ||
                             (errorData.password && errorData.password[0]) ||
                             'An unknown error occurred.';
        throw new Error(errorMessage);
    }
    return response.json();
}

/**
 * Stores the authentication token and user data in local storage.
 * @param {string} token - The authentication token.
 * @param {object} user - The user details object.
 */
function storeAuth(token, user) {
    localStorage.setItem('authToken', token);
    localStorage.setItem('userData', JSON.stringify(user));
}

/**
 * Retrieves the authentication token.
 * @returns {string | null} The token or null if not found.
 */
function getAuthToken() {
    return localStorage.getItem('authToken');
}

/**
 * Retrieves the stored user data.
 * @returns {object | null} The user data object or null.
 */
function getUserData() {
    const data = localStorage.getItem('userData');
    return data ? JSON.parse(data) : null;
}

/**
 * Displays error messages to the user in a designated element.
 * @param {string} message - The error message text.
 */
function displayError(message) {
    const errorBox = document.getElementById('auth-error-message');
    if (errorBox) {
        errorBox.textContent = message;
        errorBox.classList.remove('hidden');
    } else {
        console.error('Error Box not found:', message);
    }
}

/**
 * Handles the registration form submission.
 * @param {Event} e - The form submission event.
 */
async function handleRegistration(e) {
    e.preventDefault();
    displayError(''); // Clear previous errors

    const form = e.target;
    const formData = new FormData(form);
    
    // Convert FormData to JSON object
    const data = Object.fromEntries(formData.entries());
    
    // Automatically set role based on form or assumed standard student role if not in form
    // The form must contain a 'role' field, but we check common fields for student/organizer data
    if (!data.role) {
        data.role = data.major ? 'student' : 
                    data.organization_name ? 'organizer' : 'student'; // Default to student
    }

    try {
        const response = await fetch(`${API_BASE_URL}register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await checkResponse(response);
        
        storeAuth(result.token, result.user);
        
        // Redirect upon successful registration
        window.location.href = '/users/dashboard/';

    } catch (error) {
        displayError(error.message);
    }
}

/**
 * Handles the login form submission.
 * @param {Event} e - The form submission event.
 */
async function handleLogin(e) {
    e.preventDefault();
    displayError(''); // Clear previous errors

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${API_BASE_URL}login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await checkResponse(response);
        
        storeAuth(result.token, result.user);

        // Redirect upon successful login
        window.location.href = '/users/dashboard/';

    } catch (error) {
        displayError(error.message);
    }
}

/**
 * Logs the user out by clearing local storage and redirecting.
 */
function logoutUser() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    window.location.href = '/users/login/'; 
}

// Attach logout function to the global scope for use in the base template's button
window.logoutUser = logoutUser;