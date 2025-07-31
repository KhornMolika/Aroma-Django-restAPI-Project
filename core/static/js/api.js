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
    // Try to refresh the token
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
      const retryResponse = await fetch(url, options);

      if (!retryResponse.ok) {
        const errText = await retryResponse.text();
        throw new Error('Retry failed: ' + errText);
      }

      return retryResponse.json();
    } else {
      logout();
      throw new Error('Session expired. Please log in again.');
    }
  }

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }

  return response.json();
}

