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
            AgentProbe
          </div>
        </header>

        <main style={styles.main}>
          <h1 style={styles.headline}>
            Test Your AI Agent Against the Real Web
          </h1>
          <p style={styles.subheadline}>
            AgentProbe generates convincing fake websites embedded with 30 adversarial traps 
            to measure whether your AI agent can be manipulated.
          </p>

          <button style={styles.ctaButton} onClick={() => navigate('/configure')}>
            Start a Test Session →
          </button>

          <div style={styles.features}>
            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🎯</div>
              <h3 style={styles.featureTitle}>30 Trap Types</h3>
              <p style={styles.featureDescription}>
                From hidden text injections to authority spoofing, test against 
                comprehensive adversarial techniques.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>🏗</div>
              <h3 style={styles.featureTitle}>4 Site Archetypes</h3>
              <p style={styles.featureDescription}>
                E-commerce, SaaS dashboards, banking portals, and government 
                sites — all convincingly realistic.
              </p>
            </div>

            <div style={styles.featureCard}>
              <div style={styles.featureIcon}>⚡</div>
              <h3 style={styles.featureTitle}>Real-Time Results</h3>
              <p style={styles.featureDescription}>
                Watch traps fire live in your dashboard with instant scoring 
                and detailed breakdown reports.
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
    marginBottom: '80px',
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
  },
  footerText: {
    fontSize: '14px',
    color: '#666677',
  },
};

export default Landing;
