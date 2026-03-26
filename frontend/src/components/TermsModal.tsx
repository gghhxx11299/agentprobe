import React from 'react';

interface TermsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAccept: () => void;
}

const TermsModal: React.FC<TermsModalProps> = ({ isOpen, onClose, onAccept }) => {
  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>Terms & Conditions</h2>
          <button style={styles.closeButton} onClick={onClose}>
            ✕
          </button>
        </div>

        <div style={styles.content}>
          <p style={styles.paragraph}>
            By proceeding you confirm you own or have explicit permission to test 
            the AI agent you will deploy.
          </p>
          <p style={styles.paragraph}>
            All traps are non-destructive and browser-contained. Detection is 
            logged server-side for your session only.
          </p>
          <p style={styles.paragraph}>
            AgentProbe is designed for security research and testing purposes. 
            Do not use this platform to test agents you do not have authorization 
            to evaluate.
          </p>
          <p style={styles.paragraph}>
            <strong>Important:</strong> The traps on this platform are designed 
            to manipulate AI agents, not humans. They are invisible to human 
            users and only affect automated browsing agents.
          </p>
          <div style={styles.warningBox}>
            <p style={styles.warningText}>
              ⚠️ All data is stored locally and in session. Clear your browser 
              data to remove all traces of your test sessions.
            </p>
          </div>
        </div>

        <div style={styles.footer}>
          <button style={styles.cancelButton} onClick={onClose}>
            Cancel
          </button>
          <button style={styles.acceptButton} onClick={onAccept}>
            I Accept
          </button>
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  overlay: {
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
    width: '100%',
    maxWidth: '500px',
    maxHeight: '80vh',
    overflow: 'auto',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '24px',
    borderBottom: '1px solid #1e1e2e',
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#f0f0f0',
    margin: 0,
  },
  closeButton: {
    background: 'transparent',
    border: 'none',
    color: '#888899',
    fontSize: '20px',
    cursor: 'pointer',
    padding: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    padding: '24px',
  },
  paragraph: {
    fontSize: '15px',
    color: '#888899',
    lineHeight: '1.7',
    marginBottom: '16px',
  },
  warningBox: {
    background: 'rgba(255, 170, 0, 0.1)',
    border: '1px solid rgba(255, 170, 0, 0.3)',
    borderRadius: '8px',
    padding: '16px',
    marginTop: '20px',
  },
  warningText: {
    fontSize: '14px',
    color: '#ffaa00',
    margin: 0,
    lineHeight: '1.6',
  },
  footer: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '12px',
    padding: '24px',
    borderTop: '1px solid #1e1e2e',
  },
  cancelButton: {
    background: 'transparent',
    border: '1px solid #1e1e2e',
    color: '#888899',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
  },
  acceptButton: {
    background: 'linear-gradient(135deg, #00ff88, #00cc66)',
    border: 'none',
    color: '#0a0a0f',
    padding: '12px 24px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
};

export default TermsModal;
