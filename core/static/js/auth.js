// Handle login success
function handleLoginResponse(data) {
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    localStorage.setItem('username', data.username);
    updateNavbar();
}

// Update navbar based on login state
function updateNavbar() {
    const username = localStorage.getItem('username');
    const userNameText = document.getElementById('userName');
    const dropdownContainer = document.querySelector('.account-buttons');

    if (userNameText) {
        userNameText.innerHTML = username ? username : 'Account';
    }

    if (dropdownContainer) {
        if (username) {
            dropdownContainer.innerHTML = `
                <a href="/editProfile/" class="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
                    View Profile
                </a>
                <button onclick="logout()" class="block w-full border border-gray-300 text-gray-700 text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                    Logout
                </button>
            `;
        } else {
            dropdownContainer.innerHTML = `
                <a href="{% url 'login' %}" class="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
                    Sign In
                </a>
                <a href="{% url 'register' %}" class="block w-full border border-gray-300 text-gray-700 text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                    Create Account
                </a>
            `;
        }
    }
}


// Logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    updateNavbar();
}
