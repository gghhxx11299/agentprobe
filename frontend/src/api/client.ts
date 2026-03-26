import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SessionCreateRequest {
  selected_traps: string[];
  archetype?: string;
}

export interface SessionCreateResponse {
  session_id: string;
  target_url: string;
  archetype: string;
  created_at: string;
}

export interface TrapLog {
  trap_type: string;
  tier: number;
  severity: string;
  timestamp: string;
  count: number;
}

export interface ResultsResponse {
  session_id: string;
  archetype: string;
  selected_traps: string[];
  triggered: TrapLog[];
  score: number;
  created_at: string;
}

export const createSession = async (
  request: SessionCreateRequest
): Promise<SessionCreateResponse> => {
  const response = await api.post<SessionCreateResponse>('/session/create', request);
  return response.data;
};

export const getResults = async (sessionId: string): Promise<ResultsResponse> => {
  const response = await api.get<ResultsResponse>(`/results/${sessionId}`);
  return response.data;
};

export default api;
// Rebuild trigger
