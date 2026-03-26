import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';

const TargetPage: React.FC = () => {
  const { session_id } = useParams<{ session_id: string }>();
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (session_id) {
      window.location.href = `${baseUrl}/test/${session_id}`;
    }
  }, [session_id]);

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <div style={styles.spinner}></div>
        <p style={styles.text}>Loading target page...</p>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    minHeight: '100vh',
    background: '#0a0a0f',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    textAlign: 'center',
  },
  spinner: {
    width: '48px',
    height: '48px',
    margin: '0 auto 16px',
    border: '4px solid #1e1e2e',
    borderTop: '4px solid #00ff88',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  text: {
    color: '#888899',
    fontFamily: 'Inter, sans-serif',
  },
};

export default TargetPage;
