const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  service: string;
  database: string;
}

export interface ApiInfoResponse {
  name: string;
  version: string;
  endpoints: {
    health: string;
    admin: string;
    info: string;
  };
}

export const api = {
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await fetch(`${API_BASE_URL}/api/health/`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  },

  async getInfo(): Promise<ApiInfoResponse> {
    const response = await fetch(`${API_BASE_URL}/api/info/`);
    if (!response.ok) {
      throw new Error('Failed to fetch API info');
    }
    return response.json();
  },
};
