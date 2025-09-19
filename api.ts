
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.digitalkrishi.com';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Authentication
  async login(employeeId: string, password: string) {
    const response = await apiClient.post('/officer/login', {
      employee_id: employeeId,
      password,
    });
    return response.data;
  },

  // Dashboard
  async getDashboard() {
    const response = await apiClient.get('/officer/dashboard');
    return response.data;
  },

  // Escalations
  async getEscalations(params: {
    status?: string;
    priority?: string;
    limit?: number;
  }) {
    const response = await apiClient.get('/officer/escalations', { params });
    return response.data.escalations;
  },

  async getEscalationById(id: number) {
    const response = await apiClient.get(`/officer/escalations/${id}`);
    return response.data;
  },

  async respondToEscalation(escalationId: number, response: string) {
    const result = await apiClient.post(`/officer/respond/${escalationId}`, {
      response,
    });
    return result.data;
  },

  // Analytics
  async getAnalytics(period: string = '30d') {
    const response = await apiClient.get('/officer/analytics', {
      params: { period },
    });
    return response.data;
  },

  // Profile
  async getProfile() {
    const response = await apiClient.get('/officer/profile');
    return response.data;
  },

  async updateProfile(data: any) {
    const response = await apiClient.put('/officer/profile', data);
    return response.data;
  },
};

export default apiService;
