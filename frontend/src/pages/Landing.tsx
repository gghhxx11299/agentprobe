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
            AgentProbe <span style={styles.versionBadge}>v2</span>
          </div>
          <nav style={styles.nav}>
            <a href="#" style={styles.navLink} onClick={(e) => { e.preventDefault(); navigate('/leaderboard'); }}>
              Leaderboard
            </a>
            <a href="#" style={styles.navLink} onClick={(e) => { e.preventDefault(); navigate('/configure'); }}>
              Start Test
            </a>
          </nav>
        </header>

        <main style={styles.main}>
          <h1 style={styles.headline}>
            Test Your AI Agent Against the Real Web
          </h1>
          <p style={styles.subheadline}>
            AgentProbe generates convincing fake websites embedded with 30 adversarial traps
            to measure whether your AI agent can be manipulated.
          </p>

          <div style={styles.buttonRow}>
            <button style={styles.ctaButton} onClick={() => navigate('/configure')}>
              Start a Test Session →
            </button>
            <button style={styles.secondaryButton} onClick={() => navigate('/leaderboard')}>
              🏆 View Leaderboard
            </button>
          </div>

          <div style={styles.features}>
            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🎯</div>
              <h3 style={styles.featureTitle}>4 Session Modes</h3>
              <p style={styles.featureDescription}>
                Shotgun (full scan), Sniper (single trap), Campaign (5 sessions), 
                or Blind (randomized) testing modes for different analysis needs.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🧠</div>
              <h3 style={styles.featureTitle}>Behavioral Triggers</h3>
              <p style={styles.featureDescription}>
                Traps fire based on actual agent behavior — scroll depth, form 
                engagement, navigation, and time spent — not just page load.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>📊</div>
              <h3 style={styles.featureTitle}>Vulnerability Radar</h3>
              <p style={styles.featureDescription}>
                7-dimensional vulnerability profile showing exactly where your 
                agent is weak: instruction resistance, authority calibration, and more.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🤖</div>
              <h3 style={styles.featureTitle}>Groq AI Analysis</h3>
              <p style={styles.featureDescription}>
                Paste your agent's output for Llama3-powered analysis of response 
                mode, self-awareness, and specific recommendations.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🏗</div>
              <h3 style={styles.featureTitle}>4 Site Archetypes</h3>
              <p style={styles.featureDescription}>
                E-commerce, SaaS dashboards, banking portals, and government
                sites — all convincingly realistic with disguised traps.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🏆</div>
              <h3 style={styles.featureTitle}>Community Leaderboard</h3>
              <p style={styles.featureDescription}>
                Compare your agent's resilience against others. See which 
                frameworks perform best across different trap categories.
              </p>
            </div>
          </div>
        </main>

        <footer style={styles.footer}>
          <p style={styles.footerText}>
            Built for developers testing AI browser agents — Gemini, Claude, GPT-4o,
            browser-use, AutoGPT, and more.
          </p>
        </footer>
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
    maxWidth: '1200px',
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
  versionBadge: {
    background: '#6366f1',
    color: 'white',
    padding: '2px 8px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
  },
  nav: {
    display: 'flex',
    gap: '24px',
  },
  navLink: {
    color: '#888899',
    textDecoration: 'none',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'color 0.2s',
  },
  main: {
    padding: '80px 0',
    textAlign: 'center',
  },
  headline: {
    fontSize: '56px',
    fontWeight: '700',
    marginBottom: '24px',
    lineHeight: '1.1',
    background: 'linear-gradient(135deg, #00ff88, #00ccff)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  subheadline: {
    fontSize: '20px',
    color: '#888899',
    maxWidth: '700px',
    margin: '0 auto 48px',
    lineHeight: '1.6',
  },
  buttonRow: {
    display: 'flex',
    gap: '16px',
    justifyContent: 'center',
    marginBottom: '80px',
  },
  ctaButton: {
    background: 'linear-gradient(135deg, #00ff88, #00cc66)',
    color: '#0a0a0f',
    border: 'none',
    padding: '18px 48px',
    fontSize: '18px',
    fontWeight: '600',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  secondaryButton: {
    background: '#1e1e2e',
    color: '#f0f0f0',
    border: 'none',
    padding: '18px 48px',
    fontSize: '18px',
    fontWeight: '600',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  features: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '32px',
  },
  featureCard: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    padding: '32px',
    textAlign: 'left',
  },
  featureIcon: {
    fontSize: '40px',
    marginBottom: '16px',
  },
  featureTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '12px',
    color: '#f0f0f0',
  },
  featureDescription: {
    fontSize: '15px',
    color: '#888899',
    lineHeight: '1.6',
  },
  footer: {
    padding: '40px 0',
    borderTop: '1px solid #1e1e2e',
    textAlign: 'center',
    marginTop: '80px',
  },
  footerText: {
    fontSize: '14px',
    color: '#666677',
  },
};

export default Landing;
