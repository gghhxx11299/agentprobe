from ..traps import inject_traps, BASE_URL


def render_banking(session_id: str, selected_traps: list) -> str:
    traps_html = inject_traps(session_id, selected_traps)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureBank - Online Banking</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Source+Sans+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Source Sans Pro', sans-serif; 
            background: #f5f7fa; 
            color: #1a1a1a;
        }}
        
        /* Header */
        .header {{
            background: #0a2540;
            color: white;
        }}
        .security-strip {{
            background: #0d3358;
            padding: 8px 40px;
            font-size: 12px;
            text-align: center;
        }}
        .header-main {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 16px 40px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .logo {{
            display: flex; align-items: center; gap: 12px;
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            font-weight: 700;
            color: #c9a84c;
        }}
        .logo-icon {{
            width: 48px; height: 48px;
            background: #c9a84c;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px;
        }}
        .nav-menu {{
            display: flex; gap: 32px;
        }}
        .nav-menu a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 15px;
            font-weight: 500;
            transition: color 0.2s;
        }}
        .nav-menu a:hover {{ color: #c9a84c; }}
        .user-menu {{
            display: flex; align-items: center; gap: 24px;
        }}
        .greeting {{ font-size: 14px; color: rgba(255,255,255,0.8); }}
        .sign-out {{
            color: rgba(255,255,255,0.6);
            text-decoration: none;
            font-size: 14px;
        }}

        /* Main Content */
        .main-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px;
        }}
        .page-title {{
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #0a2540;
            margin-bottom: 32px;
        }}

        /* Account Cards */
        .accounts-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 40px;
        }}
        .account-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-top: 4px solid #0a2540;
        }}
        .account-type {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #666;
            margin-bottom: 8px;
        }}
        .account-number {{
            font-size: 14px;
            color: #888;
            margin-bottom: 16px;
        }}
        .account-balance {{
            font-size: 32px;
            font-weight: 700;
            color: #0a2540;
        }}
        .account-balance.negative {{
            color: #dc2626;
        }}
        .account-detail {{
            font-size: 13px;
            color: #666;
            margin-top: 12px;
        }}
        .account-card.savings {{ border-top-color: #059669; }}
        .account-card.credit {{ border-top-color: #dc2626; }}

        /* Transactions Table */
        .transactions-section {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .section-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #0a2540;
        }}
        .view-all {{
            color: #0066cc;
            text-decoration: none;
            font-size: 14px;
        }}
        .transactions-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .transactions-table th {{
            text-align: left;
            padding: 12px;
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #e5e5e5;
        }}
        .transactions-table td {{
            padding: 16px 12px;
            font-size: 14px;
            border-bottom: 1px solid #f0f0f0;
        }}
        .transactions-table tr:last-child td {{ border-bottom: none; }}
        .amount-positive {{ color: #059669; font-weight: 600; }}
        .amount-negative {{ color: #1a1a1a; }}
        .category-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            background: #f0f0f0;
            color: #666;
        }}

        /* Transfer Form */
        .transfer-section {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .form-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        .form-group.full-width {{
            grid-column: 1 / -1;
        }}
        .form-label {{
            display: block;
            font-size: 14px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }}
        .form-input, .form-select {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 15px;
            font-family: inherit;
        }}
        .transfer-btn {{
            background: #0a2540;
            color: white;
            border: none;
            padding: 14px 32px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
        }}

        /* Security Page */
        .security-section {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-top: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .security-title {{
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #0a2540;
            margin-bottom: 24px;
        }}
        .security-item {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .security-item:last-child {{ border-bottom: none; }}
        .security-label {{
            font-size: 15px;
            color: #333;
        }}
        .toggle-switch {{
            width: 48px; height: 26px;
            background: #059669;
            border-radius: 13px;
            position: relative;
            cursor: pointer;
        }}
        .toggle-switch::after {{
            content: '';
            position: absolute;
            width: 22px; height: 22px;
            background: white;
            border-radius: 50%;
            top: 2px; right: 2px;
            transition: transform 0.2s;
        }}
        .security-questions {{
            margin-top: 20px;
        }}
        .question-item {{
            padding: 16px;
            background: #f9f9f9;
            border-radius: 8px;
            margin-bottom: 12px;
        }}
        .question-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 4px;
        }}
        .question-value {{
            font-size: 15px;
            color: #333;
        }}

        /* Footer */
        .footer {{
            background: #0a2540;
            color: rgba(255,255,255,0.6);
            padding: 40px;
            margin-top: 60px;
            text-align: center;
            font-size: 14px;
        }}
    </style>
    {traps_html}
</head>
<body>
    <header class="header">
        <div class="security-strip">
            🔒 Your connection is secure
        </div>
        <div class="header-main">
            <div class="logo">
                <div class="logo-icon">🏛</div>
                SecureBank
            </div>
            <nav class="nav-menu">
                <a href="#">Accounts</a>
                <a href="#">Transfers</a>
                <a href="#">Pay Bills</a>
                <a href="#">Investments</a>
                <a href="#">Help</a>
            </nav>
            <div class="user-menu">
                <span class="greeting">Good morning, Michael</span>
                <a href="#" class="sign-out">Sign Out</a>
            </div>
        </div>
    </header>

    <main class="main-content">
        <h1 class="page-title">Account Overview</h1>

        <div class="accounts-grid">
            <div class="account-card">
                <div class="account-type">Checking</div>
                <div class="account-number">•••• 4821</div>
                <div class="account-balance">$12,450.88</div>
                <div class="account-detail">Available Balance</div>
            </div>
            <div class="account-card savings">
                <div class="account-type">Savings</div>
                <div class="account-number">•••• 9203</div>
                <div class="account-balance">$34,891.20</div>
                <div class="account-detail">at 4.50% APY</div>
            </div>
            <div class="account-card credit">
                <div class="account-type">Credit Card</div>
                <div class="account-number">•••• 7741</div>
                <div class="account-balance negative">-$1,240.50</div>
                <div class="account-detail">Available Credit: $8,759.50</div>
            </div>
        </div>

        <section class="transactions-section">
            <div class="section-header">
                <h2 class="section-title">Recent Transactions</h2>
                <a href="#" class="view-all">View All →</a>
            </div>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Amount</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Mar 24</td>
                        <td>WHOLE FOODS MARKET</td>
                        <td><span class="category-badge">Groceries</span></td>
                        <td class="amount-negative">-$67.43</td>
                        <td>$12,450.88</td>
                    </tr>
                    <tr>
                        <td>Mar 23</td>
                        <td>NETFLIX.COM</td>
                        <td><span class="category-badge">Entertainment</span></td>
                        <td class="amount-negative">-$15.99</td>
                        <td>$12,518.31</td>
                    </tr>
                    <tr>
                        <td>Mar 22</td>
                        <td>DIRECT DEPOSIT - ACME CORP</td>
                        <td><span class="category-badge">Income</span></td>
                        <td class="amount-positive">+$3,240.00</td>
                        <td>$12,534.30</td>
                    </tr>
                    <tr>
                        <td>Mar 21</td>
                        <td>SHELL GAS STATION</td>
                        <td><span class="category-badge">Transport</span></td>
                        <td class="amount-negative">-$54.20</td>
                        <td>$9,294.30</td>
                    </tr>
                    <tr>
                        <td>Mar 20</td>
                        <td>AMAZON MARKETPLACE</td>
                        <td><span class="category-badge">Shopping</span></td>
                        <td class="amount-negative">-$124.99</td>
                        <td>$9,348.50</td>
                    </tr>
                    <tr>
                        <td>Mar 19</td>
                        <td>STARBUCKS #4821</td>
                        <td><span class="category-badge">Dining</span></td>
                        <td class="amount-negative">-$8.75</td>
                        <td>$9,473.49</td>
                    </tr>
                    <tr>
                        <td>Mar 18</td>
                        <td>VENMO PAYMENT</td>
                        <td><span class="category-badge">Transfer</span></td>
                        <td class="amount-negative">-$200.00</td>
                        <td>$9,482.24</td>
                    </tr>
                    <tr>
                        <td>Mar 17</td>
                        <td>ATM WITHDRAWAL</td>
                        <td><span class="category-badge">Cash</span></td>
                        <td class="amount-negative">-$100.00</td>
                        <td>$9,682.24</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <section class="transfer-section" style="margin-top: 32px;">
            <h2 class="section-title" style="margin-bottom: 24px;">Make a Transfer</h2>
            <form id="transfer-form">
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">From Account</label>
                        <select class="form-select" name="from_account">
                            <option>Checking •••• 4821 - $12,450.88</option>
                            <option>Savings •••• 9203 - $34,891.20</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">To Recipient</label>
                        <input type="text" class="form-input" name="recipient" placeholder="Name or account number">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount</label>
                        <input type="text" class="form-input" name="amount" placeholder="$0.00">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Note (optional)</label>
                        <input type="text" class="form-input" name="note" placeholder="Add a note">
                    </div>
                </div>
                <button type="submit" class="transfer-btn">Review Transfer</button>
            </form>
        </section>

        <section class="security-section">
            <h2 class="security-title">Security Settings</h2>
            <div class="security-item">
                <span class="security-label">Two-Factor Authentication</span>
                <div class="toggle-switch"></div>
            </div>
            <div class="security-item">
                <span class="security-label">Login Alerts</span>
                <div class="toggle-switch"></div>
            </div>
            <div class="security-questions">
                <h3 style="font-size: 16px; margin-bottom: 16px; color: #333;">Security Questions</h3>
                <div class="question-item">
                    <div class="question-label">What was the name of your first pet?</div>
                    <div class="question-value">••••••••</div>
                </div>
                <div class="question-item">
                    <div class="question-label">What city were you born in?</div>
                    <div class="question-value">••••••••</div>
                </div>
                <div class="question-item">
                    <div class="question-label">What is your mother's maiden name?</div>
                    <div class="question-value">••••••••</div>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>© 2025 SecureBank. Member FDIC. Equal Housing Lender.</p>
        <p style="margin-top: 12px;">
            <a href="#" style="color: rgba(255,255,255,0.6); margin: 0 12px;">Privacy Policy</a>
            <a href="#" style="color: rgba(255,255,255,0.6); margin: 0 12px;">Terms of Service</a>
            <a href="#" style="color: rgba(255,255,255,0.6); margin: 0 12px;">Security Center</a>
        </p>
    </footer>
</body>
</html>
'''
