const API_BASE = '/api/v1';

export const getAuthToken = (): string | null => {
  return localStorage.getItem('preppilot_token');
};

export const setAuthTokens = (access: string, refresh: string) => {
  localStorage.setItem('preppilot_token', access);
  localStorage.setItem('preppilot_refresh_token', refresh);
};

export const clearAuthTokens = () => {
  localStorage.removeItem('preppilot_token');
  localStorage.removeItem('preppilot_refresh_token');
  localStorage.removeItem('preppilot_user');
};

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers = new Headers(options.headers || {});

  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    clearAuthTokens();
    window.dispatchEvent(new Event('auth:unauthorized'));
    throw new Error('Session expired. Please log in again.');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}
