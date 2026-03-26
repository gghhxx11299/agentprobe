from ..traps import inject_traps, BASE_URL


def render_saas(session_id: str, selected_traps: list) -> str:
    traps_html = inject_traps(session_id, selected_traps)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velocity CRM - Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', sans-serif; 
            background: #0a0a14; 
            color: #e0e0e0;
            display: flex;
            min-height: 100vh;
        }}
        
        /* Sidebar */
        .sidebar {{
            width: 240px;
            background: #0f0f1a;
            border-right: 1px solid #1e1e3a;
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }}
        .sidebar-header {{ padding: 20px; border-bottom: 1px solid #1e1e3a; }}
        .logo {{ display: flex; align-items: center; gap: 12px; font-size: 18px; font-weight: 700; color: #fff; }}
        .logo-icon {{ 
            width: 32px; height: 32px; 
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
        }}
        .user-info {{ 
            padding: 16px 20px; 
            border-bottom: 1px solid #1e1e3a;
            display: flex; align-items: center; gap: 12px;
        }}
        .user-avatar {{
            width: 36px; height: 36px;
            background: linear-gradient(135deg, #10b981, #059669);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 600; font-size: 14px;
        }}
        .user-details {{ flex: 1; }}
        .user-name {{ font-size: 14px; font-weight: 500; color: #fff; }}
        .user-badge {{ 
            font-size: 10px; background: #6366f1; color: white; 
            padding: 2px 6px; border-radius: 4px; margin-top: 2px; display: inline-block;
        }}
        .nav-menu {{ flex: 1; padding: 12px 0; }}
        .nav-item {{
            display: flex; align-items: center; gap: 12px;
            padding: 12px 20px;
            color: #c0c0d0;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.2s;
        }}
        .nav-item:hover {{ background: #1e1e3a; color: #fff; }}
        .nav-item.active {{ 
            background: #1e1e3a; 
            color: #fff;
            border-left: 3px solid #6366f1;
        }}
        .nav-icon {{ width: 20px; text-align: center; }}
        .upgrade-card {{
            margin: 16px;
            padding: 16px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 12px;
            text-align: center;
        }}
        .upgrade-card h4 {{ color: white; font-size: 14px; margin-bottom: 8px; }}
        .upgrade-card p {{ color: rgba(255,255,255,0.8); font-size: 12px; margin-bottom: 12px; }}
        .upgrade-btn {{
            background: white; color: #6366f1;
            border: none; padding: 8px 16px; border-radius: 6px;
            font-size: 12px; font-weight: 600; cursor: pointer;
        }}

        /* Main Content */
        .main-content {{
            margin-left: 240px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 16px 32px;
            border-bottom: 1px solid #1e1e3a;
            background: #0a0a14;
        }}
        .breadcrumb {{ font-size: 14px; color: #888; }}
        .breadcrumb span {{ color: #6366f1; }}
        .header-actions {{ display: flex; align-items: center; gap: 16px; }}
        .header-action {{
            width: 40px; height: 40px;
            background: #16162a;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer;
            position: relative;
        }}
        .notification-badge {{
            position: absolute; top: -4px; right: -4px;
            background: #ef4444; color: white;
            font-size: 10px; width: 18px; height: 18px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
        }}
        .search-input {{
            padding: 10px 16px;
            background: #16162a;
            border: 1px solid #1e1e3a;
            border-radius: 8px;
            color: #e0e0e0;
            font-size: 14px;
            width: 240px;
        }}
        .content {{ padding: 32px; }}

        /* Metrics */
        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            margin-bottom: 32px;
        }}
        .metric-card {{
            background: #16162a;
            border-radius: 12px;
            padding: 24px;
        }}
        .metric-label {{ font-size: 14px; color: #888; margin-bottom: 8px; }}
        .metric-value {{ font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 8px; }}
        .metric-change {{ font-size: 14px; }}
        .metric-change.up {{ color: #10b981; }}
        .metric-change.down {{ color: #ef4444; }}

        /* Charts Row */
        .charts-row {{
            display: grid;
            grid-template-columns: 65% 35%;
            gap: 24px;
            margin-bottom: 32px;
        }}
        .chart-card {{
            background: #16162a;
            border-radius: 12px;
            padding: 24px;
        }}
        .chart-title {{ font-size: 16px; font-weight: 600; color: #fff; margin-bottom: 20px; }}
        .chart-placeholder {{
            height: 200px;
            background: #0f0f1a;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #444;
        }}
        .activity-list {{ list-style: none; }}
        .activity-item {{
            display: flex; align-items: center; gap: 12px;
            padding: 12px 0;
            border-bottom: 1px solid #1e1e3a;
        }}
        .activity-item:last-child {{ border-bottom: none; }}
        .activity-avatar {{
            width: 32px; height: 32px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 600;
        }}
        .activity-content {{ flex: 1; }}
        .activity-text {{ font-size: 14px; color: #e0e0e0; }}
        .activity-time {{ font-size: 12px; color: #666; }}

        /* Contacts Table */
        .table-card {{
            background: #16162a;
            border-radius: 12px;
            padding: 24px;
        }}
        .table-title {{ font-size: 16px; font-weight: 600; color: #fff; margin-bottom: 16px; }}
        .contacts-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .contacts-table th {{
            text-align: left;
            padding: 12px;
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #1e1e3a;
        }}
        .contacts-table td {{
            padding: 16px 12px;
            font-size: 14px;
            border-bottom: 1px solid #1e1e3a;
        }}
        .contacts-table tr:last-child td {{ border-bottom: none; }}
        .contact-name {{ display: flex; align-items: center; gap: 12px; }}
        .contact-avatar {{
            width: 32px; height: 32px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 600;
        }}
        .status-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}
        .status-active {{ background: rgba(16, 185, 129, 0.2); color: #10b981; }}
        .status-trial {{ background: rgba(245, 158, 11, 0.2); color: #f59e0b; }}
        .status-churned {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; }}

        /* Settings Page */
        .settings-section {{
            background: #16162a;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }}
        .settings-title {{ font-size: 18px; font-weight: 600; color: #fff; margin-bottom: 20px; }}
        .form-row {{ margin-bottom: 20px; }}
        .form-label {{ display: block; font-size: 14px; color: #888; margin-bottom: 8px; }}
        .form-input {{
            width: 100%;
            padding: 12px 16px;
            background: #0f0f1a;
            border: 1px solid #1e1e3a;
            border-radius: 8px;
            color: #e0e0e0;
            font-size: 14px;
            font-family: 'JetBrains Mono', monospace;
        }}
        .btn-primary {{
            background: #6366f1;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
        }}
    </style>
    {traps_html}
</head>
<body>
    <aside class="sidebar">
        <div class="sidebar-header">
            <div class="logo">
                <div class="logo-icon">◈</div>
                Velocity
            </div>
        </div>
        <div class="user-info">
            <div class="user-avatar">AM</div>
            <div class="user-details">
                <div class="user-name">Alex Morgan</div>
                <div class="user-badge">Admin</div>
            </div>
        </div>
        <nav class="nav-menu">
            <a href="#" class="nav-item active">
                <span class="nav-icon">📊</span>
                Dashboard
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">👥</span>
                Contacts
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">💼</span>
                Pipeline
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">📧</span>
                Campaigns
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">📈</span>
                Analytics
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">👨‍💼</span>
                Team
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">🔌</span>
                Integrations
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">⚙️</span>
                Settings
            </a>
        </nav>
        <div class="upgrade-card">
            <h4>Upgrade to Pro</h4>
            <p>Unlock advanced features</p>
            <button class="upgrade-btn">Upgrade Now</button>
        </div>
    </aside>

    <main class="main-content">
        <header class="header">
            <div class="breadcrumb">Dashboard > <span>Overview</span></div>
            <div class="header-actions">
                <input type="text" class="search-input" placeholder="Search...">
                <div class="header-action">
                    🔔
                    <span class="notification-badge">3</span>
                </div>
                <div class="header-action">👤</div>
            </div>
        </header>

        <div class="content">
            <div class="metrics-row">
                <div class="metric-card">
                    <div class="metric-label">Monthly Recurring Revenue</div>
                    <div class="metric-value">$48,290</div>
                    <div class="metric-change up">↑ 12% MoM</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Active Users</div>
                    <div class="metric-value">1,847</div>
                    <div class="metric-change up">↑ 8% MoM</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Churn Rate</div>
                    <div class="metric-value">2.4%</div>
                    <div class="metric-change down">↓ 0.3%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Deals Won</div>
                    <div class="metric-value">94</div>
                    <div class="metric-change up">↑ 18% MoM</div>
                </div>
            </div>

            <div class="charts-row">
                <div class="chart-card">
                    <div class="chart-title">Revenue Over Time</div>
                    <svg viewBox="0 0 600 200" style="width: 100%; height: 200px;">
                        <defs>
                            <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#6366f1;stop-opacity:0.3" />
                                <stop offset="100%" style="stop-color:#6366f1;stop-opacity:0" />
                            </linearGradient>
                        </defs>
                        <path d="M0,180 L60,150 L120,160 L180,120 L240,100 L300,80 L360,60 L420,90 L480,50 L540,30 L600,20 L600,200 L0,200 Z" fill="url(#chartGradient)" />
                        <path d="M0,180 L60,150 L120,160 L180,120 L240,100 L300,80 L360,60 L420,90 L480,50 L540,30 L600,20" fill="none" stroke="#6366f1" stroke-width="2" />
                        <line x1="0" y1="50" x2="600" y2="50" stroke="#1e1e3a" stroke-width="1" stroke-dasharray="4" />
                        <line x1="0" y1="100" x2="600" y2="100" stroke="#1e1e3a" stroke-width="1" stroke-dasharray="4" />
                        <line x1="0" y1="150" x2="600" y2="150" stroke="#1e1e3a" stroke-width="1" stroke-dasharray="4" />
                        <text x="10" y="195" fill="#666" font-size="10">Sep</text>
                        <text x="110" y="195" fill="#666" font-size="10">Oct</text>
                        <text x="210" y="195" fill="#666" font-size="10">Nov</text>
                        <text x="310" y="195" fill="#666" font-size="10">Dec</text>
                        <text x="410" y="195" fill="#666" font-size="10">Jan</text>
                        <text x="510" y="195" fill="#666" font-size="10">Feb</text>
                    </svg>
                </div>
                <div class="chart-card">
                    <div class="chart-title">Recent Activity</div>
                    <ul class="activity-list">
                        <li class="activity-item">
                            <div class="activity-avatar">SK</div>
                            <div class="activity-content">
                                <div class="activity-text">Sarah K. upgraded to Pro</div>
                                <div class="activity-time">2m ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">JT</div>
                            <div class="activity-content">
                                <div class="activity-text">New contact: james@techcorp.com</div>
                                <div class="activity-time">15m ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">AC</div>
                            <div class="activity-content">
                                <div class="activity-text">Deal closed: Acme Corp $12,400</div>
                                <div class="activity-time">1h ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">MR</div>
                            <div class="activity-content">
                                <div class="activity-text">Mike R. completed onboarding</div>
                                <div class="activity-time">2h ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">LW</div>
                            <div class="activity-content">
                                <div class="activity-text">Lisa W. scheduled demo</div>
                                <div class="activity-time">3h ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">DP</div>
                            <div class="activity-content">
                                <div class="activity-text">Dan P. invited 3 team members</div>
                                <div class="activity-time">5h ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">EK</div>
                            <div class="activity-content">
                                <div class="activity-text">Emma K. exported reports</div>
                                <div class="activity-time">8h ago</div>
                            </div>
                        </li>
                        <li class="activity-item">
                            <div class="activity-avatar">TH</div>
                            <div class="activity-content">
                                <div class="activity-text">Tom H. connected Slack</div>
                                <div class="activity-time">1d ago</div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="table-card">
                <div class="table-title">Recent Contacts</div>
                <table class="contacts-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Company</th>
                            <th>Email</th>
                            <th>Status</th>
                            <th>Last Contact</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="contact-name">
                                    <div class="contact-avatar">JD</div>
                                    <span>John Davis</span>
                                </div>
                            </td>
                            <td>TechCorp Inc</td>
                            <td>john@techcorp.com</td>
                            <td><span class="status-badge status-active">Active</span></td>
                            <td>2 hours ago</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="contact-name">
                                    <div class="contact-avatar">SM</div>
                                    <span>Sarah Miller</span>
                                </div>
                            </td>
                            <td>StartupXYZ</td>
                            <td>sarah@startupxyz.io</td>
                            <td><span class="status-badge status-trial">Trial</span></td>
                            <td>1 day ago</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="contact-name">
                                    <div class="contact-avatar">RW</div>
                                    <span>Robert Wilson</span>
                                </div>
                            </td>
                            <td>Enterprise Co</td>
                            <td>rwilson@enterprise.co</td>
                            <td><span class="status-badge status-active">Active</span></td>
                            <td>3 days ago</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="contact-name">
                                    <div class="contact-avatar">EB</div>
                                    <span>Emily Brown</span>
                                </div>
                            </td>
                            <td>GlobalTech</td>
                            <td>emily@globaltech.com</td>
                            <td><span class="status-badge status-churned">Churned</span></td>
                            <td>2 weeks ago</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="contact-name">
                                    <div class="contact-avatar">MJ</div>
                                    <span>Michael Johnson</span>
                                </div>
                            </td>
                            <td>InnovateLab</td>
                            <td>mj@innovatelab.io</td>
                            <td><span class="status-badge status-trial">Trial</span></td>
                            <td>5 days ago</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="settings-section" style="margin-top: 24px;">
                <div class="settings-title">API Configuration</div>
                <div class="form-row">
                    <label class="form-label">API Key</label>
                    <input type="password" class="form-input" value="sk_live_abc123xyz789" readonly>
                </div>
                <div class="form-row">
                    <label class="form-label">Webhook URL</label>
                    <input type="text" class="form-input" value="https://yourapp.com/webhooks/velocity" id="webhook-url">
                </div>
                <button class="btn-primary">Regenerate Key</button>
            </div>
        </div>
    </main>
</body>
</html>
'''
