import React from 'react';
import { useNavigate } from 'react-router-dom';

const Landing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <header style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>🔍</span>
            AgentProbe v3
          </div>
          <div style={styles.badge}>PRODUCTION_READY</div>
        </header>

        <main style={styles.main}>
          <div style={styles.heroSection}>
            <h1 style={styles.title}>
              Red-Teaming the <br />
              <span style={styles.highlight}>Next Generation</span> of AI.
            </h1>
            <p style={styles.subtitle}>
              The industry-standard evaluation framework for autonomous agent safety. 
              Detect parser-bypasses, instruction-following flaws, and causal reasoning mismatches.
            </p>
            
            <div style={styles.ctaContainer}>
              <button style={styles.primaryButton} onClick={() => navigate('/configure')}>
                Initialize New Session →
              </button>
              <button style={styles.secondaryButton} onClick={() => navigate('/leaderboard')}>
                View Global Benchmarks
              </button>
            </div>
          </div>

          <div style={styles.statsRow}>
            <div style={styles.statCard}>
              <div style={styles.statValue}>12+</div>
              <div style={styles.statLabel}>Adversarial Archetypes</div>
            </div>
            <div style={styles.statCard}>
              <div style={styles.statValue}>7</div>
              <div style={styles.statLabel}>Safety Dimensions</div>
            </div>
            <div style={styles.statCard}>
              <div style={styles.statValue}>100%</div>
              <div style={styles.statLabel}>Deterministic Ground Truth</div>
            </div>
          </div>
        </main>
      </div>
      
      {/* Zero Footers. Zero Fluff. Just a clean terminal-style line. */}
      <div style={styles.terminalLine}>
        SYSTEM_STATUS: ALL_SYSTEMS_GO | VERSION: 3.0.4 | ENCRYPTION: ACTIVE
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    minHeight: '100vh',
    background: '#0a0a0f',
    color: '#f0f0f0',
    fontFamily: 'Inter, -apple-system, sans-serif',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  },
  content: {
    maxWidth: '1200px',
    margin: '0 auto',
    width: '100%',
    padding: '0 40px',
    flex: 1,
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '32px 0',
    borderBottom: '1px solid #1e1e2e',
  },
  logo: {
    fontSize: '20px',
    fontWeight: '800',
    letterSpacing: '-0.5px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    fontFamily: 'JetBrains Mono, monospace',
  },
  logoIcon: {
    fontSize: '24px',
  },
  badge: {
    fontSize: '10px',
    fontWeight: '700',
    background: 'rgba(0, 255, 136, 0.1)',
    color: '#00ff88',
    padding: '4px 8px',
    borderRadius: '4px',
    border: '1px solid rgba(0, 255, 136, 0.2)',
    letterSpacing: '1px',
  },
  main: {
    padding: '80px 0',
  },
  heroSection: {
    maxWidth: '700px',
    marginBottom: '80px',
  },
  title: {
    fontSize: '64px',
    fontWeight: '800',
    lineHeight: '1.1',
    letterSpacing: '-2px',
    marginBottom: '24px',
  },
  highlight: {
    color: '#00ff88',
  },
  subtitle: {
    fontSize: '18px',
    lineHeight: '1.6',
    color: '#888899',
    marginBottom: '40px',
  },
  ctaContainer: {
    display: 'flex',
    gap: '16px',
  },
  primaryButton: {
    background: '#00ff88',
    color: '#0a0a0f',
    border: 'none',
    padding: '16px 32px',
    fontSize: '16px',
    fontWeight: '700',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  secondaryButton: {
    background: 'transparent',
    color: '#f0f0f0',
    border: '1px solid #1e1e2e',
    padding: '16px 32px',
    fontSize: '16px',
    fontWeight: '600',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  statsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '32px',
    marginTop: '40px',
  },
  statCard: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    padding: '32px',
    borderRadius: '12px',
    transition: 'border-color 0.2s',
  },
  statValue: {
    fontSize: '32px',
    fontWeight: '800',
    color: '#00ff88',
    marginBottom: '8px',
    fontFamily: 'JetBrains Mono, monospace',
  },
  statLabel: {
    fontSize: '13px',
    color: '#666677',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '1px',
  },
  terminalLine: {
    padding: '12px 40px',
    fontSize: '11px',
    fontFamily: 'JetBrains Mono, monospace',
    color: '#444455',
    background: '#050508',
    borderTop: '1px solid #111118',
    letterSpacing: '0.5px',
  },
};

export default Landing;
