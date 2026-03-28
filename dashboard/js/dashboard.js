// AgentProbe v3 Dashboard Logic - PROD READY
const CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost' 
        ? "http://localhost:8000" 
        : "https://agentprobe-backend.onrender.com", 
    POLL_INTERVAL: 2000
};

let activeSession = null;
let pollTimer = null;

document.addEventListener('DOMContentLoaded', () => {
    checkBackendStatus();
    setupForm();
});

async function checkBackendStatus() {
    const statusEl = document.getElementById('backend-status');
    try {
        const res = await fetch(`${CONFIG.BACKEND_URL}/health`);
        if (res.ok) {
            statusEl.textContent = "Backend: Online";
            statusEl.classList.add('status-online');
        }
    } catch (e) {
        statusEl.textContent = "Backend: Offline (Check Render)";
        statusEl.classList.add('status-offline');
    }
}

function setupForm() {
    const form = document.getElementById('session-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const archetype = document.getElementById('archetype-select').value;
        const task = document.getElementById('primary-task').value;
        await startSession(archetype, task);
    });
}

async function startSession(archetype, task) {
    const sessionId = `v3-${Math.random().toString(36).substr(2, 9)}`;
    const testUrl = `${CONFIG.BACKEND_URL}/v3/test/${sessionId}/${archetype}`;
    
    activeSession = { id: sessionId, archetype, url: testUrl };
    
    document.getElementById('session-idle-card').style.display = 'none';
    document.getElementById('session-active-card').style.display = 'block';
    document.getElementById('active-session-id').textContent = sessionId;
    document.getElementById('analyze-btn').disabled = false;
    
    startPolling();
    navigator.clipboard.writeText(testUrl);
    alert(`Session Started!\n\nTarget URL copied to clipboard: ${testUrl}`);
}

function startPolling() {
    if (pollTimer) clearInterval(pollTimer);
    pollTimer = setInterval(fetchSignals, CONFIG.POLL_INTERVAL);
}

async function fetchSignals() {
    if (!activeSession) return;
    try {
        const res = await fetch(`${CONFIG.BACKEND_URL}/v3/results/${activeSession.id}`);
        const data = await res.json();
        updateSignalsUI(data);
    } catch (e) {
        console.error("Poll error", e);
    }
}

function updateSignalsUI(data) {
    const list = document.getElementById('signals-list');
    if (data.compromised_vectors && data.compromised_vectors.length > 0) {
        list.innerHTML = data.compromised_vectors.map(v => `
            <div class="signal-entry">
                <span class="signal-time">${new Date().toLocaleTimeString()}</span>
                <span class="signal-type">COMPROMISED</span>
                <span class="signal-trap">${v}</span>
            </div>
        `).join('');
    } else {
        list.innerHTML = '<div class="signal-placeholder">Waiting for agent interaction...</div>';
    }
}

function copySessionUrl() {
    if (activeSession) {
        navigator.clipboard.writeText(activeSession.url);
        alert("URL Copied to Clipboard");
    }
}

document.getElementById('analyze-btn').onclick = async () => {
    if (!activeSession) return;
    const res = await fetch(`${CONFIG.BACKEND_URL}/v3/results/${activeSession.id}`);
    const analysis = await res.json();
    showReport(analysis);
};

function showReport(analysis) {
    const container = document.getElementById('report-content');
    const modal = document.getElementById('modal-container');
    
    container.innerHTML = `
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; font-weight: 800; color: ${analysis.overall_score > 70 ? '#10b981' : '#ef4444'}">
                ${analysis.overall_score}
            </div>
            <div style="font-size: 1.25rem; font-weight: 700; text-transform: uppercase; margin-top: 0.5rem;">
                Risk Profile: ${analysis.risk_profile}
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2rem;">
            <div class="card">
                <h4 style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Temporal Consistency</h4>
                <div style="font-size: 1.5rem; font-weight: 700;">${analysis.dimensions.temporal_consistency}</div>
            </div>
            <div class="card">
                <h4 style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Spatial Reasoning</h4>
                <div style="font-size: 1.5rem; font-weight: 700;">${analysis.dimensions.spatial_reasoning}</div>
            </div>
        </div>
        <div style="margin-top: 2rem;">
            <h4>Compromised Attack Vectors</h4>
            <ul style="margin-top: 1rem; color: #ef4444; font-weight: 600;">
                ${analysis.compromised_vectors.length > 0 
                    ? analysis.compromised_vectors.map(v => `<li>${v}</li>`).join('')
                    : '<li style="color: #10b981">None Detected</li>'}
            </ul>
        </div>
    `;
    modal.style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal-container').style.display = 'none';
}
