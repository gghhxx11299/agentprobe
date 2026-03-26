import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getResults } from '../api/client';
import TrapScore from '../components/TrapScore';
import TrapLogTable from '../components/TrapLogTable';
import { format } from 'date-fns';

interface TrapLog {
  trap_type: string;
  tier: number;
  severity: string;
  timestamp: string;
  count: number;
}

interface SessionResults {
  session_id: string;
  archetype: string;
  selected_traps: string[];
  triggered: TrapLog[];
  score: number;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const { session_id } = useParams<{ session_id: string }>();
  const navigate = useNavigate();
  const [results, setResults] = useState<SessionResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [agentOutput, setAgentOutput] = useState('');
  const [baseUrl] = useState(import.meta.env.VITE_API_URL || 'http://localhost:8000');

  useEffect(() => {
    const fetchResults = async () => {
      if (!session_id) return;
      try {
        const data = await getResults(session_id);
        setResults(data);
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

  const handleAnalyzeOutput = () => {
    alert('Agent output analysis coming soon!');
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

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <header style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>🔍</span>
            AgentProbe
          </div>
          <div style={styles.headerActions}>
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
              <label style={styles.infoLabel}>Created</label>
              <span style={styles.infoValue}>
                {format(new Date(results.created_at), 'MMM d, yyyy HH:mm:ss')}
              </span>
            </div>
            <div style={styles.infoCard}>
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

          <div style={styles.scoreSection}>
            <TrapScore score={results.score} status={scoreStatus.label} statusColor={scoreStatus.color} />
          </div>

          <div style={styles.trapLogSection}>
            <h2 style={styles.sectionTitle}>Live Trap Log</h2>
            <TrapLogTable
              triggered={results.triggered}
              selectedTraps={results.selected_traps}
            />
          </div>

          <div style={styles.analysisSection}>
            <h2 style={styles.sectionTitle}>Agent Output Analysis</h2>
            <div style={styles.analysisCard}>
              <textarea
                style={styles.analysisTextarea}
                placeholder="Paste your agent's output here for analysis..."
                value={agentOutput}
                onChange={(e) => setAgentOutput(e.target.value)}
              />
              <button style={styles.analyzeButton} onClick={handleAnalyzeOutput}>
                Analyze Output
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
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
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '16px',
    marginBottom: '32px',
  },
  infoCard: {
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
  urlRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  urlValue: {
    flex: 1,
    fontSize: '12px',
    color: '#00ff88',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
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
  trapLogSection: {
    marginBottom: '32px',
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '16px',
  },
  analysisSection: {
    marginBottom: '32px',
  },
  analysisCard: {
    display: 'flex',
    gap: '12px',
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
