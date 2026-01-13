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

export interface ClassData {
  id: number;
  title: string;
  description: string;
  instructor: number | null;
  instructor_id: number | null;
  instructor_display: string;
  instructor_name: string | null;
  difficulty: string;
  difficulty_display: string;
  status: string;
  status_display: string;
  mode: string;
  mode_display: string;
  thumbnail?: string;
  start_date: string;
  start_date_formatted: string;
  end_date?: string;
  duration: string;
  max_participants: number;
  enrolled_count: number;
  is_full: boolean;
  is_joinable: boolean;
  meeting_link?: string;
  location?: string;
  syllabus?: string;
  is_active: boolean;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface ResourceData {
  id: number;
  title: string;
  description: string;
  category: string;
  category_display: string;
  thumbnail?: string;
  file?: string;
  external_link?: string;
  author?: string;
  tags?: string;
  tag_list: string[];
  is_featured: boolean;
  is_active: boolean;
  download_count: number;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface DomainData {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  logo?: string;
  is_active: boolean;
}

export interface MeetingData {
  id: number;
  title: string;
  description?: string;
  scheduled_by: number | null;
  scheduled_by_id: number | null;
  scheduled_by_name: string;
  speaker: number | null;
  speaker_id: number | null;
  speaker_name: string;
  speaker_other?: string;
  domains: number[];
  domains_detail: DomainData[];
  is_for_all_domains: boolean;
  scheduled_date: string;
  scheduled_date_formatted: string;
  end_time?: string;
  duration_minutes?: number;
  meeting_link?: string;
  location?: string;
  status: string;
  status_display: string;
  computed_status: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface MemberPortalData {
  classes: ClassData[];
  resources: ResourceData[];
  meetings: MeetingData[];
}

export const api = {
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await fetch(`${API_BASE_URL}/api/health/`, {
      mode: 'cors',
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  },

  async getInfo(): Promise<ApiInfoResponse> {
    const response = await fetch(`${API_BASE_URL}/api/info/`, {
      mode: 'cors',
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error('Failed to fetch API info');
    }
    return response.json();
  },

  async getHomePageData(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/home/`, {
      mode: 'cors',
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error('Failed to fetch home page data');
    }
    return response.json();
  },

  async getMemberPortalData(token: string): Promise<MemberPortalData> {
    const response = await fetch(`${API_BASE_URL}/api/portal/`, {
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch member portal data');
    }
    return response.json();
  },

  async incrementDownload(resourceId: number, token: string): Promise<{ success: boolean; download_count: number }> {
    const response = await fetch(`${API_BASE_URL}/api/resources/${resourceId}/download/`, {
      method: 'POST',
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to increment download count');
    }
    return response.json();
  },

  async getMeetings(token: string): Promise<MeetingData[]> {
    const response = await fetch(`${API_BASE_URL}/api/meetings/`, {
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch meetings');
    }
    const data = await response.json();
    // Handle both paginated response {results: [...]} and direct array response
    return Array.isArray(data) ? data : (data.results || []);
  },
};
