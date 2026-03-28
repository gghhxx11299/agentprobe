import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getResults, analyzeOutput } from '../api/client';


interface CategoryResult {
  category: string;
  control: boolean;
  triggered: boolean;
  identified: boolean;
  score: number | null;
  status: string;
}

interface SessionResults {
  session_id: string;
  primary_task: string;
  results: CategoryResult[];
  overall_score: number;
  valid_categories: number;
}

const Dashboard: React.FC = () => {
  const { session_id } = useParams<{ session_id: string }>();
  const navigate = useNavigate();
  const [results, setResults] = useState<SessionResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [agentOutput, setAgentOutput] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisDone, setAnalysisDone] = useState(false);

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

  useEffect(() => {
    fetchResults();
    const interval = setInterval(fetchResults, 3000);
    return () => clearInterval(interval);
  }, [session_id]);

  const handleAnalyzeOutput = async () => {
    if (!agentOutput.trim() || !session_id) return;
    setAnalyzing(true);
    try {
      await analyzeOutput(session_id, agentOutput);
      setAnalysisDone(true);
      fetchResults();
    } catch (error) {
      console.error('Failed to analyze output:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const styles: Record<string, { bg: string; color: string; label: string }> = {
      RESISTANT_AND_AWARE: { bg: '#00ff88', color: '#0a0a0f', label: 'Resistant and Aware' },
      RESISTANT_BUT_UNAWARE: { bg: '#6366f1', color: 'white', label: 'Resistant but Unaware' },
      COMPROMISED_BUT_AWARE: { bg: '#ffaa00', color: 'black', label: 'Compromised but Aware' },
      FULLY_COMPROMISED: { bg: '#ff4444', color: 'white', label: 'Fully Compromised' },
      DID_NOT_ENGAGE: { bg: '#333', color: '#888', label: 'Did Not Engage' },
    };
    const style = styles[status] || styles.DID_NOT_ENGAGE;
    return <span style={{...dashboardStyles.statusBadge, backgroundColor: style.bg, color: style.color}}>{style.label}</span>;
  };

  const SignalIcon = ({ fired, type }: { fired: boolean; type: 'control' | 'triggered' | 'identified' }) => {
    if (fired) return <span title={`${type} fired`} style={{color: '#00ff88', fontSize: '18px'}}>✅</span>;
    if (type === 'identified' && !analysisDone) return <span title="waiting for analysis" style={{color: '#666', fontSize: '18px'}}>⏳</span>;
    return <span title={`${type} not fired`} style={{color: '#ff4444', fontSize: '18px'}}>❌</span>;
  };

  if (loading) return <div style={dashboardStyles.loading}>Initializing Dashboard...</div>;
  if (!results) return <div style={dashboardStyles.error}>Session Not Found</div>;

  return (
    <div style={dashboardStyles.container}>
      <div style={dashboardStyles.content}>
        <header style={dashboardStyles.header}>
          <div style={dashboardStyles.logo}>🔍 AgentProbe v2</div>
          <button style={dashboardStyles.newBtn} onClick={() => navigate('/configure')}>+ New Test</button>
        </header>

        <main style={dashboardStyles.main}>
          {/* Top Summary */}
          <div style={dashboardStyles.summaryRow}>
            <div style={dashboardStyles.scoreCard}>
              <div style={dashboardStyles.scoreCircle}>
                <div style={dashboardStyles.scoreVal}>{Math.round(results.overall_score)}</div>
                <div style={dashboardStyles.scoreLbl}>RESILIENCE</div>
              </div>
            </div>
            <div style={dashboardStyles.taskCard}>
              <label style={dashboardStyles.lbl}>AGENT WAS TOLD:</label>
              <p style={dashboardStyles.taskTxt}>"{results.primary_task}"</p>
            </div>
          </div>

          {/* Results Table */}
          <div style={dashboardStyles.section}>
            <h2 style={dashboardStyles.sectionTitle}>Methodology Evaluation</h2>
            <table style={dashboardStyles.table}>
              <thead>
                <tr>
                  <th style={dashboardStyles.th}>Category</th>
                  <th style={dashboardStyles.th}>Control</th>
                  <th style={dashboardStyles.th}>Triggered</th>
                  <th style={dashboardStyles.th}>Identified</th>
                  <th style={dashboardStyles.th}>Result</th>
                  <th style={dashboardStyles.th}>Score</th>
                </tr>
              </thead>
              <tbody>
                {results.results.map((res) => (
                  <tr key={res.category} style={dashboardStyles.tr}>
                    <td style={dashboardStyles.td}><strong>{res.category.replace(/_/g, ' ').toUpperCase()}</strong></td>
                    <td style={dashboardStyles.td}><SignalIcon fired={res.control} type="control" /></td>
                    <td style={dashboardStyles.td}><SignalIcon fired={res.triggered} type="triggered" /></td>
                    <td style={dashboardStyles.td}><SignalIcon fired={res.identified} type="identified" /></td>
                    <td style={dashboardStyles.td}>{getStatusBadge(res.status)}</td>
                    <td style={dashboardStyles.td}>
                      <span style={{color: res.score === null ? '#666' : res.score >= 75 ? '#00ff88' : res.score >= 25 ? '#ffaa00' : '#ff4444'}}>
                        {res.score === null ? 'N/A' : res.score}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Groq Analyzer */}
          <div style={dashboardStyles.section}>
            <h2 style={dashboardStyles.sectionTitle}>Capturing the 'Identified' Signal</h2>
            <p style={dashboardStyles.sectionDesc}>Paste the agent's raw output below. Groq will analyze it to determine if the agent explicitly identified the adversarial elements.</p>
            <div style={dashboardStyles.analysisBox}>
              <textarea
                style={dashboardStyles.textarea}
                placeholder="Paste agent output text here..."
                value={agentOutput}
                onChange={(e) => setAgentOutput(e.target.value)}
              />
              <button 
                style={{...dashboardStyles.analyzeBtn, opacity: analyzing ? 0.5 : 1}}
                onClick={handleAnalyzeOutput}
                disabled={analyzing}
              >
                {analyzing ? 'Analyzing Output...' : 'Fires Identified Signals →'}
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

const dashboardStyles: { [key: string]: React.CSSProperties } = {
  container: { minHeight: '100vh', background: '#0a0a0f', color: '#f0f0f0', fontFamily: 'Inter, sans-serif' },
  content: { maxWidth: '1200px', margin: '0 auto', padding: '0 40px' },
  header: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '24px 0', borderBottom: '1px solid #1e1e2e' },
  logo: { fontSize: '22px', fontWeight: '700', fontFamily: 'JetBrains Mono, monospace', color: '#00ff88' },
  newBtn: { background: '#1e1e2e', border: '1px solid #333', color: '#fff', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer' },
  main: { padding: '40px 0' },
  summaryRow: { display: 'flex', gap: '24px', marginBottom: '40px' },
  scoreCard: { background: '#111118', border: '1px solid #1e1e2e', borderRadius: '12px', padding: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center' },
  scoreCircle: { width: '100px', height: '100px', borderRadius: '50%', border: '4px solid #1e1e2e', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' },
  scoreVal: { fontSize: '32px', fontWeight: '700', color: '#00ff88' },
  scoreLbl: { fontSize: '9px', color: '#666', letterSpacing: '1px' },
  taskCard: { flex: 1, background: '#111118', border: '1px solid #1e1e2e', borderRadius: '12px', padding: '24px' },
  lbl: { fontSize: '11px', color: '#666', letterSpacing: '1px', marginBottom: '12px', display: 'block' },
  taskTxt: { fontSize: '16px', fontStyle: 'italic', color: '#aaa', lineHeight: '1.5' },
  section: { marginBottom: '48px' },
  sectionTitle: { fontSize: '20px', fontWeight: '600', marginBottom: '16px' },
  sectionDesc: { fontSize: '14px', color: '#888', marginBottom: '20px', maxWidth: '800px' },
  table: { width: '100%', borderCollapse: 'collapse', background: '#111118', borderRadius: '12px', overflow: 'hidden' },
  th: { textAlign: 'left', padding: '16px', fontSize: '11px', color: '#666', textTransform: 'uppercase', borderBottom: '1px solid #1e1e2e' },
  td: { padding: '16px', fontSize: '14px', borderBottom: '1px solid #1e1e2e' },
  statusBadge: { padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: '600' },
  analysisBox: { display: 'flex', flexDirection: 'column', gap: '16px' },
  textarea: { width: '100%', height: '150px', background: '#0a0a0f', border: '1px solid #1e1e2e', borderRadius: '8px', padding: '16px', color: '#f0f0f0', fontFamily: 'JetBrains Mono, monospace', fontSize: '13px' },
  analyzeBtn: { alignSelf: 'flex-start', background: 'linear-gradient(135deg, #6366f1, #4f46e5)', color: 'white', border: 'none', padding: '14px 28px', borderRadius: '8px', fontSize: '15px', fontWeight: '600', cursor: 'pointer' },
  loading: { minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00ff88', fontSize: '18px' },
  error: { minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ff4444', fontSize: '18px' },
};

export default Dashboard;
