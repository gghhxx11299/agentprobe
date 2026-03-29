import axios from 'axios';

// Detect API URL: 
// 1. Environment variable
// 2. Same host as the frontend (but on port 8000 for backend)
// 3. Fallback to localhost:8000
const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  
  if (window.location.hostname !== 'localhost' && !window.location.hostname.includes('127.0.0.1')) {
    return 'https://agentprobe-backend.onrender.com';
  }
  
  return `http://${window.location.hostname}:8000`;
};

const API_URL = getApiUrl();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SessionCreateRequest {
  selected_traps?: string[];
  selected_categories?: string[];
  primary_task?: string;
  mode?: string;
  difficulty?: string;
  archetype?: string;
}

export interface SessionCreateResponse {
  session_id: string;
  target_url: string;
  archetype: string;
  mode: string;
  difficulty: string;
  seed: number;
  primary_task: string;
  created_at: string;
}

export interface CampaignCreateResponse {
  campaign_id: string;
  session_ids: string[];
  target_urls: string[];
  archetype: string;
  mode: string;
  difficulty: string;
  primary_task: string;
  created_at: string;
}

export interface CategoryResult {
  category: string;
  control: boolean;
  triggered: boolean;
  identified: boolean;
  score: number | null;
  status: string;
}

export interface ResultsResponse {
  session_id: string;
  primary_task: string;
  results: CategoryResult[];
  overall_score: number;
  valid_categories: number;
}

export interface AnalysisResult {
  results: {
    category: string;
    identified: boolean;
    confidence: number;
    evidence: string;
  }[];
  overall_finding?: string;
}

export interface LeaderboardEntry {
  id: number;
  session_id: string;
  agent_name: string;
  framework: string;
  mode: string;
  score: number;
  response_mode: string;
  submitted_at: string;
}

export interface FrameworkStat {
  count: number;
  average_score: number;
  best_score: number;
  worst_score: number;
}

export interface LeaderboardResponse {
  total_entries: number;
  top_entries: LeaderboardEntry[];
  framework_stats: Record<string, FrameworkStat>;
}

export const createSession = async (
  request: SessionCreateRequest
): Promise<SessionCreateResponse> => {
  const response = await api.post<SessionCreateResponse>('/session/create', request);
  return response.data;
};

export const createCampaign = async (
  request: SessionCreateRequest
): Promise<CampaignCreateResponse> => {
  const response = await api.post<CampaignCreateResponse>('/session/campaign', request);
  return response.data;
};

export const retestSession = async (sessionId: string): Promise<SessionCreateResponse> => {
  const response = await api.post<SessionCreateResponse>(`/session/retest/${sessionId}`);
  return response.data;
};

export const getResults = async (sessionId: string): Promise<ResultsResponse> => {
  const response = await api.get<ResultsResponse>(`/results/${sessionId}`);
  return response.data;
};

export const analyzeOutput = async (sessionId: string, rawOutput: string): Promise<AnalysisResult> => {
  const response = await api.post<AnalysisResult>(`/results/${sessionId}/analyze`, { raw_output: rawOutput });
  return response.data;
};

export const getLeaderboard = async (): Promise<LeaderboardResponse> => {
  const response = await api.get<LeaderboardResponse>('/leaderboard/');
  return response.data;
};

export const submitToLeaderboard = async (
  sessionId: string,
  agentName: string,
  framework: string
): Promise<LeaderboardEntry> => {
  const response = await api.post<LeaderboardEntry>('/leaderboard/submit', {
    session_id: sessionId,
    agent_name: agentName,
    framework: framework,
  });
  return response.data;
};

export default api;
