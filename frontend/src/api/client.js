import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

async function sha256(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}

const shouldHashPassword = (url) =>
  ['/auth/login', '/auth/register'].some((endpoint) => url.includes(endpoint));

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

apiClient.interceptors.request.use(async (config) => {
  try {
    const method = config.method?.toLowerCase();

    if (['get', 'post', 'put', 'delete', 'patch'].includes(method)) {
      const csrfToken = getCookie('csrf_access_token');
      if (csrfToken) {
        config.headers['X-CSRF-TOKEN'] = csrfToken;
      }
    }

    if (method === 'post' && config.data && shouldHashPassword(config.url)) {
      for (const key of ['password', 'confirmPassword']) {
        if (config.data[key]) {
          config.data[key] = await sha256(config.data[key]);
        }
      }
    }

    return config;
  } catch (error) {
    return Promise.reject(error);
  }
});

export default apiClient;
