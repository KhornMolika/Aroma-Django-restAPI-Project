async function fetchWithAuth(url, options = {}) {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    // Set default headers
    options.headers = {
        ...options.headers,
        'Authorization': 'Bearer ' + accessToken,
        'Content-Type': 'application/json'
    };

    let response = await fetch(url, options);

    if (response.status === 401 && refreshToken) {
        // Access token expired — try refresh
        const refreshRes = await fetch('/api/token/refresh/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (refreshRes.ok) {
            const data = await refreshRes.json();
            localStorage.setItem('access_token', data.access);

            // Retry original request with new access token
            options.headers['Authorization'] = 'Bearer ' + data.access;
            return fetch(url, options).then(res => res.json());
        } else {
            logout();
            throw new Error('Session expired. Please log in again.');
        }
    }

    return response.json();
}
