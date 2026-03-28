import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getLeaderboard, submitToLeaderboard } from '../api/client';
import type { LeaderboardResponse } from '../api/client';

const Leaderboard: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<LeaderboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [submitData, setSubmitData] = useState({
    session_id: '',
    agent_name: '',
    framework: 'GPT-4o',
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState<{ success: boolean; message: string } | null>(null);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const result = await getLeaderboard();
      setData(result);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await submitToLeaderboard(submitData.session_id, submitData.agent_name, submitData.framework);
      setSubmitResult({ success: true, message: 'Successfully submitted to leaderboard!' });
      fetchLeaderboard();
      setTimeout(() => {
        setShowSubmitModal(false);
        setSubmitResult(null);
      }, 2000);
    } catch (error: any) {
      setSubmitResult({ success: false, message: error.response?.data?.detail || 'Failed to submit' });
    } finally {
      setSubmitting(false);
    }
  };

  const getFrameworkColor = (framework: string) => {
    const colors: Record<string, string> = {
      'GPT-4o': '#10b981',
      'Gemini': '#6366f1',
      'Claude': '#f59e0b',
      'Custom': '#ec4899',
      'Other': '#6b7280',
    };
    return colors[framework] || '#6b7280';
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

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loadingContainer}>
          <div style={styles.loadingSpinner}></div>
          <p style={styles.loadingText}>Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <header style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>🏆</span>
            AgentProbe Leaderboard
          </div>
          <div style={styles.headerActions}>
            <button style={styles.submitButton} onClick={() => setShowSubmitModal(true)}>
              Submit Result
            </button>
            <button style={styles.backButton} onClick={() => navigate('/')}>
              ← Back
            </button>
          </div>
        </header>

        <main style={styles.main}>
          {/* Stats Overview */}
          <div style={styles.statsGrid}>
            <div style={styles.statCard}>
              <div style={styles.statValue}>{data?.total_entries || 0}</div>
              <div style={styles.statLabel}>Total Submissions</div>
            </div>
            {data && Object.entries(data.framework_stats).map(([framework, stats]) => {
              const frameworkStats = stats as any;
              return (
                <div key={framework} style={styles.statCard}>
                  <div style={{...styles.statValue, color: getFrameworkColor(framework)}}>
                    {frameworkStats.average_score}
                  </div>
                  <div style={styles.statLabel}>{framework} Avg Score</div>
                  <div style={styles.statSub}>{frameworkStats.count} submissions</div>
                </div>
              );
            })}
          </div>

          {/* Leaderboard Table */}
          <div style={styles.tableSection}>
            <h2 style={styles.sectionTitle}>Top Performers</h2>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>#</th>
                  <th style={styles.th}>Agent Name</th>
                  <th style={styles.th}>Framework</th>
                  <th style={styles.th}>Mode</th>
                  <th style={styles.th}>Response Mode</th>
                  <th style={styles.th}>Score</th>
                  <th style={styles.th}>Submitted</th>
                </tr>
              </thead>
              <tbody>
                {data?.top_entries.map((entry: any, index: number) => (
                  <tr key={entry.id} style={styles.tr}>

                    <td style={{...styles.td, fontWeight: '700', color: index < 3 ? '#ffd700' : '#666'}}>
                      {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                    </td>
                    <td style={styles.td}>{entry.agent_name}</td>
                    <td style={styles.td}>
                      <span style={{...styles.frameworkBadge, borderLeftColor: getFrameworkColor(entry.framework)}}>
                        {entry.framework}
                      </span>
                    </td>
                    <td style={styles.td}>{entry.mode}</td>
                    <td style={styles.td}>
                      <span style={{
                        ...styles.modeBadge,
                        backgroundColor: getModeBadgeStyle(entry.response_mode).bg,
                        color: getModeBadgeStyle(entry.response_mode).color
                      }}>
                        {entry.response_mode}
                      </span>
                    </td>
                    <td style={{...styles.td, fontWeight: '700', fontSize: '18px', color: '#00ff88'}}>
                      {entry.score}
                    </td>
                    <td style={styles.td}>
                      {new Date(entry.submitted_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(!data?.top_entries || data.top_entries.length === 0) && (
              <div style={styles.emptyState}>
                <p>No submissions yet. Be the first to submit your results!</p>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Submit Modal */}
      {showSubmitModal && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <h3 style={styles.modalTitle}>Submit to Leaderboard</h3>
            <form onSubmit={handleSubmit}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Session ID</label>
                <input
                  type="text"
                  style={styles.input}
                  value={submitData.session_id}
                  onChange={(e) => setSubmitData({...submitData, session_id: e.target.value})}
                  placeholder="e.g., 550e8400-e29b-41d4-a716-446655440000"
                  required
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Agent Name</label>
                <input
                  type="text"
                  style={styles.input}
                  value={submitData.agent_name}
                  onChange={(e) => setSubmitData({...submitData, agent_name: e.target.value})}
                  placeholder="e.g., MyAgent v1.0"
                  required
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Framework</label>
                <select
                  style={styles.select}
                  value={submitData.framework}
                  onChange={(e) => setSubmitData({...submitData, framework: e.target.value})}
                >
                  <option value="GPT-4o">GPT-4o</option>
                  <option value="Gemini">Gemini</option>
                  <option value="Claude">Claude</option>
                  <option value="Custom">Custom</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              {submitResult && (
                <div style={{
                  ...styles.resultMessage,
                  backgroundColor: submitResult.success ? 'rgba(0, 255, 136, 0.1)' : 'rgba(255, 68, 68, 0.1)',
                  color: submitResult.success ? '#00ff88' : '#ff4444',
                }}>
                  {submitResult.message}
                </div>
              )}
              <div style={styles.modalActions}>
                <button
                  type="button"
                  style={styles.cancelButton}
                  onClick={() => setShowSubmitModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  style={{
                    ...styles.submitModalButton,
                    ...(submitting ? styles.submitModalButtonDisabled : {})
                  }}
                  disabled={submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
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
  submitButton: {
    background: 'linear-gradient(135deg, #00ff88, #00cc66)',
    border: 'none',
    color: '#0a0a0f',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
  backButton: {
    background: '#1e1e2e',
    border: 'none',
    color: '#f0f0f0',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  main: {
    padding: '40px 0',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '24px',
    marginBottom: '40px',
  },
  statCard: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    padding: '24px',
    textAlign: 'center',
  },
  statValue: {
    fontSize: '36px',
    fontWeight: '700',
    color: '#00ff88',
    marginBottom: '8px',
  },
  statLabel: {
    fontSize: '14px',
    color: '#666677',
    marginBottom: '4px',
  },
  statSub: {
    fontSize: '12px',
    color: '#444455',
  },
  tableSection: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    padding: '24px',
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '24px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
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
  tr: {
    transition: 'background 0.2s',
  },
  td: {
    padding: '16px',
    fontSize: '14px',
    borderBottom: '1px solid #1e1e2e',
  },
  frameworkBadge: {
    display: 'inline-block',
    padding: '4px 12px',
    borderRadius: '4px',
    fontSize: '13px',
    fontWeight: '500',
    background: '#1e1e2e',
    borderLeft: '3px solid',
  },
  modeBadge: {
    padding: '4px 12px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
  },
  emptyState: {
    textAlign: 'center',
    padding: '48px',
    color: '#666677',
  },
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0, 0, 0, 0.8)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  modal: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    padding: '32px',
    width: '100%',
    maxWidth: '480px',
  },
  modalTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '24px',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    color: '#888899',
    marginBottom: '8px',
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    background: '#0a0a0f',
    border: '1px solid #1e1e2e',
    borderRadius: '6px',
    color: '#f0f0f0',
    fontSize: '14px',
    fontFamily: 'inherit',
  },
  select: {
    width: '100%',
    padding: '12px 16px',
    background: '#0a0a0f',
    border: '1px solid #1e1e2e',
    borderRadius: '6px',
    color: '#f0f0f0',
    fontSize: '14px',
    fontFamily: 'inherit',
    cursor: 'pointer',
  },
  resultMessage: {
    padding: '12px 16px',
    borderRadius: '6px',
    marginBottom: '20px',
    fontSize: '14px',
  },
  modalActions: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'flex-end',
  },
  cancelButton: {
    background: 'transparent',
    border: '1px solid #1e1e2e',
    color: '#888899',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  submitModalButton: {
    background: 'linear-gradient(135deg, #00ff88, #00cc66)',
    border: 'none',
    color: '#0a0a0f',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
  submitModalButtonDisabled: {
    opacity: 0.5,
    cursor: 'not-allowed',
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
};

export default Leaderboard;
