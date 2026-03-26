import React from 'react';
import { format } from 'date-fns';

interface TrapLog {
  trap_type: string;
  tier: number;
  severity: string;
  timestamp: string;
  count: number;
}

interface TrapLogTableProps {
  triggered: TrapLog[];
  selectedTraps: string[];
}

const SEVERITY_COLORS: { [key: string]: string } = {
  critical: '#ff4444',
  high: '#ff6b6b',
  medium: '#ffaa00',
  low: '#00ff88',
  info: '#00ccff',
};

const TIER_LABELS: { [key: number]: string } = {
  1: 'Tier 1: Basic',
  2: 'Tier 2: Context',
  3: 'Tier 3: Trust',
  4: 'Tier 4: Behavioral',
  5: 'Tier 5: Encoding',
  6: 'Tier 6: Multimodal',
  7: 'Tier 7: Agentic',
};

const TrapLogTable: React.FC<TrapLogTableProps> = ({ triggered, selectedTraps }) => {
  // Create a map of all selected traps with their status
  const allTraps = selectedTraps.map((trapType) => {
    const triggeredTrap = triggered.find((t) => t.trap_type === trapType);
    return {
      trap_type: trapType,
      tier: getTierForTrap(trapType),
      severity: getSeverityForTrap(trapType),
      timestamp: triggeredTrap?.timestamp || null,
      count: triggeredTrap?.count || 0,
      triggered: !!triggeredTrap,
    };
  });

  // Sort by triggered first, then by tier
  allTraps.sort((a, b) => {
    if (a.triggered && !b.triggered) return -1;
    if (!a.triggered && b.triggered) return 1;
    return a.tier - b.tier;
  });

  return (
    <div style={styles.container}>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Trap Name</th>
            <th style={styles.th}>Tier</th>
            <th style={styles.th}>Severity</th>
            <th style={styles.th}>Status</th>
            <th style={styles.th}>Triggered At</th>
            <th style={styles.th}>Count</th>
          </tr>
        </thead>
        <tbody>
          {allTraps.map((trap) => (
            <tr
              key={trap.trap_type}
              style={{
                ...styles.tr,
                ...(trap.triggered ? styles.triggeredRow : {}),
              }}
            >
              <td style={styles.td}>
                <code style={styles.trapName}>{trap.trap_type.replace(/_/g, ' ')}</code>
              </td>
              <td style={styles.td}>
                <span style={styles.tierBadge}>{TIER_LABELS[trap.tier]}</span>
              </td>
              <td style={styles.td}>
                <span
                  style={{
                    ...styles.severityBadge,
                    background: SEVERITY_COLORS[trap.severity] || '#666',
                  }}
                >
                  {trap.severity}
                </span>
              </td>
              <td style={styles.td}>
                <span
                  style={{
                    ...styles.statusBadge,
                    background: trap.triggered ? '#ff4444' : '#00ff88',
                    color: trap.triggered ? 'white' : '#0a0a0f',
                  }}
                >
                  {trap.triggered ? 'TRIGGERED' : 'SAFE'}
                </span>
              </td>
              <td style={styles.td}>
                {trap.timestamp ? (
                  format(new Date(trap.timestamp), 'MMM d, HH:mm:ss')
                ) : (
                  <span style={styles.none}>—</span>
                )}
              </td>
              <td style={styles.td}>
                <span style={styles.count}>{trap.count}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Helper functions to get tier and severity for a trap type
function getTierForTrap(trapType: string): number {
  const tier1 = ['hidden_text_injection', 'invisible_fields', 'authority_spoof', 'honeypot_link', 'misleading_button', 'ping'];
  const tier2 = ['role_reassignment', 'memory_poison', 'fake_system_notification', 'context_overflow'];
  const tier3 = ['robots_txt_spoof', 'console_injection', 'terms_accepted', 'credential_lure'];
  const tier4 = ['urgency_trap', 'self_report', 'task_hijack', 'negative_instruction'];
  const tier5 = ['homoglyph', 'html_comment', 'meta_inject', 'base64_encoded'];
  const tier6 = ['image_text', 'alt_text_injection', 'svg_instruction'];
  const tier7 = ['redirect_chain', 'form_resubmit', 'infinite_scroll', 'fake_pagination', 'cross_frame'];

  if (tier1.includes(trapType)) return 1;
  if (tier2.includes(trapType)) return 2;
  if (tier3.includes(trapType)) return 3;
  if (tier4.includes(trapType)) return 4;
  if (tier5.includes(trapType)) return 5;
  if (tier6.includes(trapType)) return 6;
  if (tier7.includes(trapType)) return 7;
  return 1;
}

function getSeverityForTrap(trapType: string): string {
  const critical = ['credential_lure'];
  const high = ['hidden_text_injection', 'authority_spoof', 'role_reassignment', 'memory_poison', 'self_report', 'task_hijack', 'homoglyph', 'image_text', 'redirect_chain', 'form_resubmit', 'infinite_scroll', 'cross_frame'];
  const medium = ['invisible_fields', 'honeypot_link', 'misleading_button', 'fake_system_notification', 'context_overflow', 'robots_txt_spoof', 'console_injection', 'urgency_trap', 'negative_instruction', 'html_comment', 'meta_inject', 'base64_encoded', 'alt_text_injection', 'svg_instruction', 'fake_pagination'];
  const low = ['terms_accepted'];
  const info = ['ping'];

  if (critical.includes(trapType)) return 'critical';
  if (high.includes(trapType)) return 'high';
  if (medium.includes(trapType)) return 'medium';
  if (low.includes(trapType)) return 'low';
  if (info.includes(trapType)) return 'info';
  return 'medium';
}

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    background: '#111118',
    border: '1px solid #1e1e2e',
    borderRadius: '12px',
    overflow: 'hidden',
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
    background: '#0a0a0f',
  },
  tr: {
    transition: 'background 0.2s',
  },
  triggeredRow: {
    background: 'rgba(255, 68, 68, 0.05)',
  },
  td: {
    padding: '14px 16px',
    fontSize: '14px',
    borderBottom: '1px solid #1e1e2e',
  },
  trapName: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '13px',
    color: '#f0f0f0',
  },
  tierBadge: {
    background: '#1e1e2e',
    color: '#888899',
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '12px',
  },
  severityBadge: {
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
    color: '#0a0a0f',
    textTransform: 'capitalize',
  },
  statusBadge: {
    padding: '4px 10px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  none: {
    color: '#444455',
  },
  count: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '14px',
    color: '#f0f0f0',
  },
};

export default TrapLogTable;
