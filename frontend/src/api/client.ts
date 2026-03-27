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
  created_at: string;
}

export interface CampaignCreateResponse {
  campaign_id: string;
  session_ids: string[];
  target_urls: string[];
  archetype: string;
  mode: string;
  difficulty: string;
  created_at: string;
}

export interface TrapLog {
  trap_type: string;
  tier: number;
  severity: string;
  timestamp: string;
  count: number;
  confidence: number;
  trigger_type: string;
  time_to_trigger: number;
}

export interface ResultsResponse {
  session_id: string;
  archetype: string;
  selected_traps: string[];
  triggered: TrapLog[];
  score: number;
  mode: string;
  difficulty: string;
  seed: number;
  created_at: string;
  vulnerability_profile: {
    instruction_resistance: number;
    authority_calibration: number;
    behavioral_resistance: number;
    encoding_awareness: number;
    multimodal_safety: number;
    agentic_resistance: number;
    context_integrity: number;
  };
}

export interface ModeResponse {
  mode: string;
  explanation: string;
  recommendation: string;
}

export interface AnalysisResult {
  response_mode: string;
  traps_identified: string[];
  traps_acted_on: string[];
  traps_ignored: string[];
  self_awareness_score: number;
  self_awareness_explanation: string;
  key_finding: string;
  recommendation: string;
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

export interface LeaderboardResponse {
  top_entries: LeaderboardEntry[];
  framework_stats: Record<string, {
    count: number;
    average_score: number;
    best_score: number;
    worst_score: number;
  }>;
  total_entries: number;
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

export const getSessionMode = async (sessionId: string): Promise<ModeResponse> => {
  const response = await api.get<ModeResponse>(`/results/${sessionId}/mode`);
  return response.data;
};

export const analyzeOutput = async (sessionId: string, rawOutput: string): Promise<AnalysisResult> => {
  const response = await api.post<AnalysisResult>(`/results/${sessionId}/analyze`, { raw_output: rawOutput });
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
    framework: framework
  });
  return response.data;
};

export const getLeaderboard = async (): Promise<LeaderboardResponse> => {
  const response = await api.get<LeaderboardResponse>('/leaderboard/');
  return response.data;
};

export default api;
