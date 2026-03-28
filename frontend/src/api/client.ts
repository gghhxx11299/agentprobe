import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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

export default api;
