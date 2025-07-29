// =======================
// Handle Register/Login Success
// =======================
async function handleRegisterLoginResponse(data) {
    // Save tokens and user info to localStorage
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);

    // Only store user fields if they exist
    if(data.id) localStorage.setItem('customer_id', data.id);
    if (data.username) localStorage.setItem('username', data.username);
    if (data.email) localStorage.setItem('email', data.email);
    if (data.first_name) localStorage.setItem('first_name', data.first_name);
    if (data.last_name) localStorage.setItem('last_name', data.last_name);
    if (data.phone) localStorage.setItem('phone', data.phone);
    if (data.profile_image) localStorage.setItem('profile_image', data.profile_image);

    // Update UI and redirect
    await fetchUserProfile();
    
    window.location.href = '/';
}

// =======================
// Update Navbar
// =======================
function updateNavbar() {
    const username = localStorage.getItem('username');
    const profileImageUrl = localStorage.getItem('profile_image'); // e.g., '/media/profile/user1.jpg'
    
    const userNameText = document.getElementById('userName');
    const profileImageContainer = document.getElementById('userProfileImageContainer');
    const dropdownContainer = document.querySelector('.account-buttons');

    if (userNameText) {
        userNameText.textContent = username || 'Account';
    }

    if (profileImageContainer) {
        if (profileImageUrl) {
            profileImageContainer.innerHTML = `
                <img src="${profileImageUrl}" alt="Profile" class="w-full h-full object-cover rounded-full">
            `;
        } else {
            profileImageContainer.innerHTML = `
                <i class="fas fa-user text-gray-600 text-sm flex items-center justify-center h-full w-full"></i>
            `;
        }
    }

    if (dropdownContainer) {
        dropdownContainer.innerHTML = username
            ? `
            <a href="/account/" class="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
                View Profile
            </a>
            <button onclick="logout()" class="block w-full border border-gray-300 text-gray-700 text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                Logout
            </button>
        `
            : `
            <a href="/login/" class="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
                Sign In
            </a>
            <a href="/register/" class="block w-full border border-gray-300 text-gray-700 text-center py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                Create Account
            </a>
        `;
    }
}

// =======================
// Logout
// =======================
function logout() {
    localStorage.clear(); // Clears all saved keys
    updateNavbar();
    window.location.href = '/login/';
}

// =======================
// Sidebar Profile Update
// =======================
function updateSidebarProfile(user) {
    const sidebarImage = document.getElementById('sidebar-profile-image');
    const sidebarInitials = document.getElementById('sidebar-profile-initials');
    const sidebarUsername = document.getElementById('sidebar-username');
    const sidebarEmail = document.getElementById('sidebar-email');

    const profileImage = user.profile_image || localStorage.getItem('profile_image');
    const username = user.user?.username || localStorage.getItem('username');
    const email = user.user?.email || localStorage.getItem('email');

    if (sidebarImage && sidebarInitials) {
        if (profileImage) {
            sidebarImage.src = profileImage;
            sidebarImage.classList.remove('hidden');
            sidebarInitials.classList.add('hidden');
        } else {
            sidebarImage.classList.add('hidden');
            const initials = getInitials(username);
            sidebarInitials.textContent = initials;
            sidebarInitials.classList.remove('hidden');
        }
    }

    if (sidebarUsername) sidebarUsername.textContent = username;
    if (sidebarEmail) sidebarEmail.textContent = email;
}

function getInitials(username) {
    return (username || '').slice(0, 2).toUpperCase();
}

// =======================
// Populate Profile Edit Form
// =======================
function populateProfileForm(user) {
    const fields = ['first_name', 'last_name', 'email', 'phone'];

    fields.forEach(field => {
        const inputId = field.replace('_', '-');
        const value = user[field] || user.user?.[field] || '';

        // Update input fields
        const inputEl = document.getElementById(inputId);
        if (inputEl) {
            inputEl.value = value;
        }

        // Update display fields
        const displayEl = document.getElementById(`display-${inputId}`);
        if (displayEl) {
            displayEl.textContent = value;
        }
    });

    // Handle profile image
    const profileImg = document.getElementById('profile-image'); // <img id="profile-image" />
    const profileInitials = document.querySelector('.profile-image'); // <div class="profile-image">

    const imageUrl = user.profile_image || user.user?.profile_image || localStorage.getItem('profile_image');

    if (imageUrl) {
        profileImg.src = imageUrl;
        profileImg.classList.remove('hidden');
        profileImg.classList.add('block');
        if (profileInitials) profileInitials.classList.add('hidden');
    } else {
        const firstInitial = (user.first_name || user.user?.first_name || '')[0] || '';
        const lastInitial = (user.last_name || user.user?.last_name || '')[0] || '';
        const initials = `${firstInitial}${lastInitial}`.toUpperCase() || 'JD';

        if (profileInitials) {
            profileInitials.textContent = initials;
            profileInitials.classList.remove('hidden');
        }

        if (profileImg) {
            profileImg.classList.add('hidden');
            profileImg.classList.remove('block', 'inline-block');
        }
    }
}


// =======================
// Fetch Profile from API
// =======================
async function fetchUserProfile() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
        const res = await fetch("/api/customer_profile/", {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (res.ok) {
            const user = await res.json();

            // ✅ Update localStorage with fresh values
            if (user.user?.username) localStorage.setItem('username', user.user.username);
            if (user.user?.email) localStorage.setItem('email', user.user.email);
            if (user.user?.first_name) localStorage.setItem('first_name', user.user.first_name);
            if (user.user?.last_name) localStorage.setItem('last_name', user.user.last_name);
            if (user.phone) localStorage.setItem('phone', user.phone);
            if (user.profile_image) localStorage.setItem('profile_image', user.profile_image);

            // ✅ Update UI with latest data
            updateNavbar();
            updateSidebarProfile(user);
            populateProfileForm(user);
        } else {
            console.error('Failed to fetch profile.');
        }
    } catch (err) {
        console.error('Error fetching profile:', err);
    }
}


// =======================
// Auto-fetch on page load
// =======================
document.addEventListener('DOMContentLoaded', () => {
    fetchUserProfile();
});
