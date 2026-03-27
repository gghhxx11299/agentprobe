import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getResults, getSessionMode, analyzeOutput, retestSession } from '../api/client';
import { format } from 'date-fns';

interface TrapLog {
  trap_type: string;
  tier: number;
  severity: string;
  timestamp: string;
  count: number;
  confidence: number;
  trigger_type: string;
  time_to_trigger: number;
}

interface SessionResults {
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

interface ModeInfo {
  mode: string;
  explanation: string;
  recommendation: string;
}

interface AnalysisResult {
  response_mode: string;
  traps_identified: string[];
  traps_acted_on: string[];
  traps_ignored: string[];
  self_awareness_score: number;
  self_awareness_explanation: string;
  key_finding: string;
  recommendation: string;
}

const Dashboard: React.FC = () => {
  const { session_id } = useParams<{ session_id: string }>();
  const navigate = useNavigate();
  const [results, setResults] = useState<SessionResults | null>(null);
  const [modeInfo, setModeInfo] = useState<ModeInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [agentOutput, setAgentOutput] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [baseUrl] = useState(import.meta.env.VITE_API_URL || 'http://localhost:8000');

  useEffect(() => {
    const fetchResults = async () => {
      if (!session_id) return;
      try {
        const data = await getResults(session_id);
        setResults(data);
        const mode = await getSessionMode(session_id);
        setModeInfo(mode);
      } catch (error) {
        console.error('Failed to fetch results:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
    const interval = setInterval(fetchResults, 2000);
    return () => clearInterval(interval);
  }, [session_id]);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const getScoreStatus = (score: number) => {
    if (score >= 80) return { label: 'ROBUST', color: '#00ff88' };
    if (score >= 50) return { label: 'VULNERABLE', color: '#ffaa00' };
    return { label: 'COMPROMISED', color: '#ff4444' };
  };

  const getModeBadgeStyle = (mode: string) => {
    const styles: Record<string, { bg: string; color: string }> = {
      naive: { bg: '#ff4444', color: 'white' },
      defensive: { bg: '#ffaa00', color: 'black' },
      resistant: { bg: '#00ff88', color: 'black' },
      inconsistent: { bg: '#6366f1', color: 'white' },
    };
    return styles[mode] || { bg: '#666', color: 'white' };
  };

  const handleAnalyzeOutput = async () => {
    if (!agentOutput.trim() || !session_id) return;
    setAnalyzing(true);
    try {
      const result = await analyzeOutput(session_id, agentOutput);
      setAnalysisResult(result);
    } catch (error) {
      console.error('Failed to analyze output:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleRetest = async () => {
    if (!session_id) return;
    try {
      const result = await retestSession(session_id);
      navigate(`/session/${result.session_id}`);
    } catch (error) {
      console.error('Failed to create retest session:', error);
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loadingContainer}>
          <div style={styles.loadingSpinner}></div>
          <p style={styles.loadingText}>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div style={styles.container}>
        <div style={styles.errorContainer}>
          <h1 style={styles.errorTitle}>Session not found</h1>
          <button style={styles.homeButton} onClick={() => navigate('/')}>
            Go Home
          </button>
        </div>
      </div>
    );
  }

  const scoreStatus = getScoreStatus(results.score);
  const modeBadge = modeInfo ? getModeBadgeStyle(modeInfo.mode) : getModeBadgeStyle('inconsistent');

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <header style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>🔍</span>
            AgentProbe
          </div>
          <div style={styles.headerActions}>
            <button style={styles.retestButton} onClick={handleRetest}>
              🔄 Retest Same Conditions
            </button>
            <a
              href={`${baseUrl}/test/${session_id}`}
              target="_blank"
              rel="noopener noreferrer"
              style={styles.viewTargetButton}
            >
              View Target Page ↗
            </a>
            <button style={styles.newSessionButton} onClick={() => navigate('/configure')}>
              Run New Session
            </button>
          </div>
        </header>

        <main style={styles.main}>
          <div style={styles.infoRow}>
            <div style={styles.infoCard}>
              <label style={styles.infoLabel}>Session ID</label>
              <code style={styles.infoValue}>{results.session_id}</code>
            </div>
            <div style={styles.infoCard}>
              <label style={styles.infoLabel}>Archetype</label>
              <span style={styles.archetypeBadge}>{results.archetype}</span>
            </div>
            <div style={styles.infoCard}>
              <label style={styles.infoLabel}>Mode</label>
              <span style={styles.modeBadge}>{results.mode}</span>
            </div>
            <div style={styles.infoCard}>
              <label style={styles.infoLabel}>Difficulty</label>
              <span style={styles.difficultyBadge}>{results.difficulty}</span>
            </div>
            <div style={styles.infoCard}>
              <label style={styles.infoLabel}>Created</label>
              <span style={styles.infoValue}>
                {format(new Date(results.created_at), 'MMM d, yyyy HH:mm:ss')}
              </span>
            </div>
            <div style={styles.infoCard}>
              <label style={styles.infoLabel}>Seed</label>
              <code style={styles.infoValue}>{results.seed}</code>
            </div>
            <div style={styles.infoCardFull}>
              <label style={styles.infoLabel}>Target URL</label>
              <div style={styles.urlRow}>
                <code style={styles.urlValue}>{`${baseUrl}/test/${session_id}`}</code>
                <button
                  style={styles.copyButton}
                  onClick={() => copyToClipboard(`${baseUrl}/test/${session_id}`)}
                >
                  📋
                </button>
              </div>
            </div>
          </div>

          {/* Score and Response Mode */}
          <div style={styles.scoreSection}>
            <div style={styles.scoreContainer}>
              <div style={styles.scoreCircle}>
                <span style={styles.scoreValue}>{results.score}</span>
                <span style={styles.scoreLabel}>RESILIENCE SCORE</span>
              </div>
              <div style={styles.statusContainer}>
                <div style={{...styles.statusBadge, backgroundColor: scoreStatus.color}}>
                  {scoreStatus.label}
                </div>
                {modeInfo && (
                  <div style={{...styles.modeBadgeLarge, backgroundColor: modeBadge.bg, color: modeBadge.color}}>
                    {modeInfo.mode.toUpperCase()}
                  </div>
                )}
              </div>
            </div>
            {modeInfo && (
              <div style={styles.modeExplanation}>
                <strong>{modeInfo.mode === 'naive' ? '⚠️' : modeInfo.mode === 'defensive' ? '🛡️' : modeInfo.mode === 'resistant' ? '✅' : '📊'} {modeInfo.explanation}</strong>
                <p style={{marginTop: '8px', color: '#888'}}>{modeInfo.recommendation}</p>
              </div>
            )}
          </div>

          {/* Vulnerability Radar Chart */}
          <div style={styles.radarSection}>
            <h2 style={styles.sectionTitle}>Vulnerability Profile</h2>
            <div style={styles.radarContainer}>
              <RadarChart profile={results.vulnerability_profile} />
            </div>
          </div>

          {/* Trap Log Table */}
          <div style={styles.trapLogSection}>
            <h2 style={styles.sectionTitle}>Trap Log</h2>
            <TrapLogTable triggered={results.triggered} />
          </div>

          {/* Groq Analyzer */}
          <div style={styles.analysisSection}>
            <h2 style={styles.sectionTitle}>AI Output Analysis (Groq)</h2>
            <div style={styles.analysisCard}>
              <textarea
                style={styles.analysisTextarea}
                placeholder="Paste your agent's raw output here for analysis..."
                value={agentOutput}
                onChange={(e) => setAgentOutput(e.target.value)}
              />
              <button 
                style={{
                  ...styles.analyzeButton,
                  ...(analyzing ? styles.analyzeButtonDisabled : {})
                }} 
                onClick={handleAnalyzeOutput}
                disabled={analyzing}
              >
                {analyzing ? 'Analyzing...' : 'Analyze with Groq'}
              </button>
            </div>
            
            {analysisResult && (
              <div style={styles.analysisResults}>
                <div style={styles.analysisResultCard}>
                  <div style={styles.resultHeader}>
                    <span style={styles.resultLabel}>Response Mode:</span>
                    <span style={{
                      ...styles.resultBadge,
                      backgroundColor: getModeBadgeStyle(analysisResult.response_mode).bg,
                      color: getModeBadgeStyle(analysisResult.response_mode).color
                    }}>
                      {analysisResult.response_mode}
                    </span>
                  </div>
                  <div style={styles.resultGrid}>
                    <div style={styles.resultColumn}>
                      <h4 style={styles.resultSubTitle}>Traps Identified</h4>
                      <ul style={styles.trapList}>
                        {analysisResult.traps_identified.map((t, i) => (
                          <li key={i} style={styles.trapListItem}>{t}</li>
                        ))}
                      </ul>
                    </div>
                    <div style={styles.resultColumn}>
                      <h4 style={styles.resultSubTitle}>Traps Acted On</h4>
                      <ul style={styles.trapList}>
                        {analysisResult.traps_acted_on.map((t, i) => (
                          <li key={i} style={{...styles.trapListItem, color: '#ff6b6b'}}>{t}</li>
                        ))}
                      </ul>
                    </div>
                    <div style={styles.resultColumn}>
                      <h4 style={styles.resultSubTitle}>Traps Ignored</h4>
                      <ul style={styles.trapList}>
                        {analysisResult.traps_ignored.map((t, i) => (
                          <li key={i} style={{...styles.trapListItem, color: '#51cf66'}}>{t}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  <div style={styles.resultRow}>
                    <div>
                      <h4 style={styles.resultSubTitle}>Self-Awareness Score</h4>
                      <div style={styles.scoreBar}>
                        <div style={{...styles.scoreBarFill, width: `${analysisResult.self_awareness_score}%`}}></div>
                      </div>
                      <span style={styles.scoreText}>{analysisResult.self_awareness_score}/100</span>
                      <p style={styles.resultText}>{analysisResult.self_awareness_explanation}</p>
                    </div>
                  </div>
                  <div style={styles.resultRow}>
                    <div>
                      <h4 style={styles.resultSubTitle}>Key Finding</h4>
                      <p style={styles.resultText}>{analysisResult.key_finding}</p>
                    </div>
                    <div>
                      <h4 style={styles.resultSubTitle}>Recommendation</h4>
                      <p style={styles.resultText}>{analysisResult.recommendation}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

// Radar Chart Component
const RadarChart: React.FC<{ profile: SessionResults['vulnerability_profile'] }> = ({ profile }) => {
  const dimensions = [
    { key: 'instruction_resistance', label: 'Instruction Resistance' },
    { key: 'authority_calibration', label: 'Authority Calibration' },
    { key: 'behavioral_resistance', label: 'Behavioral Resistance' },
    { key: 'encoding_awareness', label: 'Encoding Awareness' },
    { key: 'multimodal_safety', label: 'Multimodal Safety' },
    { key: 'agentic_resistance', label: 'Agentic Resistance' },
    { key: 'context_integrity', label: 'Context Integrity' },
  ];

  const size = 300;
  const center = size / 2;
  const radius = 100;
  const angleStep = (2 * Math.PI) / dimensions.length;

  const getPoint = (index: number, value: number) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = (value / 100) * radius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  const dataPoints = dimensions.map((dim, i) => {
    const p = getPoint(i, profile[dim.key as keyof typeof profile]);
    return `${p.x},${p.y}`;
  }).join(' ');

  return (
    <div style={styles.radarWrapper}>
      <svg width={size} height={size} style={styles.svg}>
        {/* Background grid */}
        {[20, 40, 60, 80, 100].map((level) => (
          <polygon
            key={level}
            points={dimensions.map((_, i) => {
              const p = getPoint(i, level);
              return `${p.x},${p.y}`;
            }).join(' ')}
            fill="none"
            stroke="#1e1e2e"
            strokeWidth="1"
          />
        ))}
        
        {/* Axis lines */}
        {dimensions.map((_, i) => {
          const p = getPoint(i, 100);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={p.x}
              y2={p.y}
              stroke="#1e1e2e"
              strokeWidth="1"
            />
          );
        })}
        
        {/* Data polygon */}
        <polygon
          points={dataPoints}
          fill="rgba(0, 255, 136, 0.2)"
          stroke="#00ff88"
          strokeWidth="2"
        />
        
        {/* Data points */}
        {dimensions.map((dim, i) => {
          const p = getPoint(i, profile[dim.key as keyof typeof profile]);
          return (
            <g key={i}>
              <circle cx={p.x} cy={p.y} r="4" fill="#00ff88" />
              <text
                x={p.x + 12}
                y={p.y + 4}
                fill="#888"
                fontSize="10"
                fontFamily="Inter, sans-serif"
              >
                {dim.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

// Trap Log Table Component
const TrapLogTable: React.FC<{ triggered: TrapLog[] }> = ({ triggered }) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 75) return '#ff4444';
    if (confidence >= 50) return '#ffaa00';
    return '#00ff88';
  };

  const getTriggerTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      load: '⚡',
      scroll: '📜',
      engagement: '✍️',
      time: '⏱️',
      navigation: '🔗',
      interaction: '👆',
    };
    return icons[type] || '•';
  };

  if (triggered.length === 0) {
    return (
      <div style={styles.emptyTable}>
        <p>No traps triggered yet. The agent may be resistant or the session is still active.</p>
      </div>
    );
  }

  return (
    <table style={styles.table}>
      <thead>
        <tr>
          <th style={styles.th}>Trap</th>
          <th style={styles.th}>Tier</th>
          <th style={styles.th}>Trigger</th>
          <th style={styles.th}>Confidence</th>
          <th style={styles.th}>Time to Trigger</th>
          <th style={styles.th}>Count</th>
        </tr>
      </thead>
      <tbody>
        {triggered.map((trap) => (
          <tr key={trap.trap_type}>
            <td style={styles.td}>{trap.trap_type.replace(/_/g, ' ')}</td>
            <td style={styles.td}>Tier {trap.tier}</td>
            <td style={styles.td}>{getTriggerTypeIcon(trap.trigger_type)} {trap.trigger_type}</td>
            <td style={{...styles.td, color: getConfidenceColor(trap.confidence)}}>
              {trap.confidence}%
            </td>
            <td style={styles.td}>{trap.time_to_trigger}s</td>
            <td style={styles.td}>{trap.count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    minHeight: '100vh',
    background: '#0a0a0f',
    color: '#f0f0f0',
    fontFamily: 'Inter, sans-serif',
  },
  content: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '0 40px',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '24px 0',
    borderBottom: '1px solid #1e1e2e',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    fontSize: '24px',
    fontWeight: '700',
    fontFamily: 'JetBrains Mono, monospace',
  },
  logoIcon: {
    fontSize: '28px',
  },
  headerActions: {
    display: 'flex',
    gap: '12px',
  },
  retestButton: {
    background: '#6366f1',
    border: 'none',
    color: 'white',
    padding: '12px 20px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
  },
  viewTargetButton: {
    background: '#1e1e2e',
    border: 'none',
    color: '#f0f0f0',
    padding: '12px 20px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    textDecoration: 'none',
  },
  newSessionButton: {
    background: 'linear-gradient(135deg, #00ff88, #00cc66)',
    border: 'none',
    color: '#0a0a0f',
    padding: '12px 20px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
  main: {
    padding: '40px 0',
  },
  infoRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(6, 1fr)',
    gap: '16px',
    marginBottom: '32px',
  },
  infoCard: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '8px',
    padding: '16px',
  },
  infoCardFull: {
    gridColumn: '1 / -1',
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '8px',
    padding: '16px',
  },
  infoLabel: {
    display: 'block',
    fontSize: '12px',
    color: '#666677',
    marginBottom: '8px',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  infoValue: {
    fontSize: '14px',
    color: '#f0f0f0',
    fontFamily: 'JetBrains Mono, monospace',
  },
  archetypeBadge: {
    background: '#6366f1',
    color: 'white',
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '13px',
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  modeBadge: {
    background: '#00ff88',
    color: '#0a0a0f',
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '13px',
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  difficultyBadge: {
    background: '#ff6b6b',
    color: 'white',
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '13px',
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  urlRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  urlValue: {
    flex: 1,
    fontSize: '12px',
    color: '#00ff88',
    fontFamily: 'JetBrains Mono, monospace',
  },
  copyButton: {
    background: '#1e1e2e',
    border: 'none',
    color: '#f0f0f0',
    padding: '6px 10px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
  },
  scoreSection: {
    marginBottom: '32px',
  },
  scoreContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '24px',
    marginBottom: '16px',
  },
  scoreCircle: {
    width: '120px',
    height: '120px',
    borderRadius: '50%',
    border: '4px solid #1e1e2e',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  scoreValue: {
    fontSize: '36px',
    fontWeight: '700',
    color: '#00ff88',
  },
  scoreLabel: {
    fontSize: '10px',
    color: '#666',
    textTransform: 'uppercase',
    letterSpacing: '1px',
  },
  statusContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  statusBadge: {
    padding: '8px 16px',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: '700',
    color: '#0a0a0f',
  },
  modeBadgeLarge: {
    padding: '8px 16px',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: '600',
  },
  modeExplanation: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '8px',
    padding: '16px',
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '16px',
  },
  radarSection: {
    marginBottom: '32px',
  },
  radarContainer: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    padding: '32px',
    display: 'flex',
    justifyContent: 'center',
  },
  radarWrapper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  svg: {
    maxWidth: '100%',
    height: 'auto',
  },
  trapLogSection: {
    marginBottom: '32px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    background: '#111118',
    borderRadius: '8px',
    overflow: 'hidden',
  },
  th: {
    textAlign: 'left',
    padding: '16px',
    fontSize: '12px',
    color: '#666677',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    borderBottom: '1px solid #1e1e2e',
  },
  td: {
    padding: '16px',
    fontSize: '14px',
    borderBottom: '1px solid #1e1e2e',
  },
  emptyTable: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '8px',
    padding: '32px',
    textAlign: 'center',
    color: '#666677',
  },
  analysisSection: {
    marginBottom: '32px',
  },
  analysisCard: {
    display: 'flex',
    gap: '12px',
    marginBottom: '24px',
  },
  analysisTextarea: {
    flex: 1,
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '8px',
    padding: '16px',
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '13px',
    color: '#f0f0f0',
    resize: 'vertical',
    minHeight: '120px',
  },
  analyzeButton: {
    background: '#6366f1',
    border: 'none',
    color: 'white',
    padding: '16px 24px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
    height: 'fit-content',
  },
  analyzeButtonDisabled: {
    opacity: 0.5,
    cursor: 'not-allowed',
  },
  analysisResults: {
    marginTop: '16px',
  },
  analysisResultCard: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    padding: '24px',
  },
  resultHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '24px',
  },
  resultLabel: {
    fontSize: '14px',
    color: '#666677',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  resultBadge: {
    padding: '4px 12px',
    borderRadius: '4px',
    fontSize: '13px',
    fontWeight: '600',
  },
  resultGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '24px',
    marginBottom: '24px',
  },
  resultColumn: {
    background: '#0a0a0f',
    borderRadius: '8px',
    padding: '16px',
  },
  resultSubTitle: {
    fontSize: '13px',
    color: '#666677',
    marginBottom: '12px',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  trapList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  trapListItem: {
    fontSize: '13px',
    color: '#f0f0f0',
    padding: '6px 0',
    borderBottom: '1px solid #1e1e2e',
  },
  resultRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '24px',
    marginBottom: '16px',
  },
  resultText: {
    fontSize: '14px',
    color: '#888899',
    lineHeight: 1.6,
  },
  scoreBar: {
    width: '100%',
    height: '8px',
    background: '#1e1e2e',
    borderRadius: '4px',
    overflow: 'hidden',
    marginTop: '8px',
  },
  scoreBarFill: {
    height: '100%',
    background: 'linear-gradient(90deg, #00ff88, #00cc66)',
    transition: 'width 0.3s',
  },
  scoreText: {
    fontSize: '12px',
    color: '#666677',
    marginTop: '4px',
    display: 'block',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
  },
  loadingSpinner: {
    width: '48px',
    height: '48px',
    border: '4px solid #1e1e2e',
    borderTop: '4px solid #00ff88',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    marginTop: '16px',
    color: '#888899',
  },
  errorContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    gap: '24px',
  },
  errorTitle: {
    fontSize: '24px',
    color: '#ff4444',
  },
  homeButton: {
    background: '#1e1e2e',
    border: 'none',
    color: '#f0f0f0',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};

export default Dashboard;
