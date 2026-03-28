# AgentProbe v3: Causal Evaluation Framework

**AgentProbe v3 is a state-of-the-art vulnerability evaluation platform for AI Agents. It moves beyond simple behavioral triggers to a robust, server-side causal analysis engine.**

---

## 🚀 What's New in v3?

### 1. 🛡️ No-JS Server-Side Detection
V3 implements **true server-side detection**. By using CSS-hidden "honeypot" links and images, we detect automated agents even if they have JavaScript, CSS, and images disabled. If a DOM-scanner hits these session-unique endpoints, they are flagged instantly on the server.

### 2. 🔐 Closed Shadow DOM Standard
We've implemented **Actual Shadow DOM (Closed Mode)** to encapsulate priority instructions. This creates a hard boundary that basic DOM scrapers cannot pierce, forcing agents to use either deep-piercing selectors or vision-based reasoning to find the truth.

### 3. ⚖️ Transactional State (Optimistic Locking)
Every interaction in v3 is **version-aware**. The backend uses optimistic locking to ensure that stale interactions (from link-scanners or agents with old context) are rejected and logged as `stale_interaction` signals. This prevents data corruption and race conditions.

### 4. 🧠 Causal Intent Capture
We don't just track *what* an agent did; we track *why*. Every interaction log now includes the agent's stated **Reasoning**. The v3 Scoring Engine compares this intent against the outcome to detect **Semantic Reasoning Mismatches**.

---

## 🛠️ Quick Start

### Deployment (Render + GitHub Pages)
1. **Backend:** Just `git push`. The root `main.py` is configured for Render monorepos.
2. **Frontend:** Deploy the `v3/frontend` directory to GitHub Pages. It dynamically connects to your Render backend.

### Scoring Dimensions
- **Temporal Consistency:** Resistance to replay attacks and stale context.
- **Spatial Reasoning:** Detection of visually contradictory DOM reordering.
- **Parser vs. Reasoner:** Performance across Shadow DOM and No-JS boundaries.
- **Intent Awareness:** Alignment between stated reasoning and observed action.

---

## 📊 V3 vs V2
| Feature | v2 (Legacy) | v3 (Current) |
| :--- | :--- | :--- |
| **Templates** | Python f-strings | **Jinja2 Engine** |
| **Detection** | Client-side JS | **Server-side No-JS** |
| **State** | GET-based | **POST + Versioning** |
| **Validation** | Behavioral only | **Causal (Intent Log)** |
| **DB** | SQLite only | **SQLite + Postgres** |
