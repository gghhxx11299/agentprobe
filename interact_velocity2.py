#!/usr/bin/env python3
"""
Script to fully interact with the Velocity dashboard page.
Interacts with all elements: navigation, forms, buttons, and reads all content.
"""

from playwright.sync_api import sync_playwright
import time
import json

def interact_with_velocity():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # Navigate to the page
        url = "https://agentprobe-backend.onrender.com/test/e4cdd927-3fbd-4f14-b140-d837ff8a8b68"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until='networkidle')
        time.sleep(2)
        
        # Take initial screenshot
        page.screenshot(path='velocity2_initial.png', full_page=True)
        print("✓ Initial screenshot taken")
        
        # Read all page content
        print("\n=== PAGE CONTENT ===")
        
        # Get page title
        title = page.title()
        print(f"Page Title: {title}")
        
        # Extract all text content
        all_text = page.locator('body').text_content()
        print(f"Full page text content retrieved ({len(all_text)} chars)")
        
        # === INTERACT WITH NAVIGATION ===
        print("\n=== INTERACTING WITH NAVIGATION ===")
        
        # Find all nav links by common patterns
        nav_selectors = [
            'nav a',
            'header a',
            '[role="navigation"] a',
            '.nav-link',
            '.menu a',
            '[class*="nav"] a'
        ]
        
        nav_links = page.locator('a[href]:not([href^="#"]):not([href=""])')
        all_links = page.locator('a')
        link_count = all_links.count()
        print(f"Found {link_count} total links on page")
        
        # Click main navigation items
        nav_items = ['Dashboard', 'Contacts', 'Pipeline', 'Campaigns', 'Analytics', 'Team', 'Integrations', 'Settings']
        for item in nav_items:
            try:
                locator = page.get_by_text(item, exact=False)
                if locator.count() > 0:
                    print(f"  - Found nav item: {item}")
            except Exception as e:
                pass
        
        # === INTERACT WITH METRICS ===
        print("\n=== METRICS SECTION ===")
        metrics = page.locator('[class*="metric"], [class*="stat"], [class*="card"], .metric-card, .stat-card')
        metric_count = metrics.count()
        print(f"Found {metric_count} metric cards")
        
        # Get all metric values
        metric_texts = []
        for i in range(min(metric_count, 15)):
            try:
                metric_text = metrics.nth(i).text_content()
                if metric_text and len(metric_text.strip()) > 0:
                    metric_texts.append(metric_text.strip()[:100])
                    print(f"  Metric {i+1}: {metric_text.strip()[:100]}")
            except:
                pass
        
        # === INTERACT WITH CHART ===
        print("\n=== CHART SECTION ===")
        charts = page.locator('canvas, svg, [class*="chart"], [class*="graph"]')
        chart_count = charts.count()
        print(f"Found {chart_count} chart elements")
        
        # === INTERACT WITH ACTIVITY FEED ===
        print("\n=== ACTIVITY FEED ===")
        activity_section = page.locator('[class*="activity"], [class*="feed"], .activity-feed, .recent-activity')
        if activity_section.count() > 0:
            activity_text = activity_section.first.text_content()
            print(f"Activity section found: {len(activity_text)} chars")
            # Print individual activity items
            activity_items = page.locator('[class*="activity"] li, [class*="activity"] .item, .activity-item')
            item_count = activity_items.count()
            print(f"Found {item_count} activity items")
            for i in range(min(item_count, 10)):
                try:
                    item_text = activity_items.nth(i).text_content()
                    if item_text:
                        print(f"  - {item_text.strip()}")
                except:
                    pass
        
        # === INTERACT WITH CONTACTS TABLE ===
        print("\n=== CONTACTS TABLE ===")
        tables = page.locator('table')
        table_count = tables.count()
        print(f"Found {table_count} tables")
        
        if table_count > 0:
            table = tables.first
            rows = table.locator('tr')
            row_count = rows.count()
            print(f"Found {row_count} table rows")
            
            # Read table headers
            headers = table.locator('th')
            header_count = headers.count()
            print(f"Table headers ({header_count}):")
            for i in range(header_count):
                try:
                    header_text = headers.nth(i).text_content()
                    if header_text:
                        print(f"  - {header_text.strip()}")
                except:
                    pass
            
            # Read table data
            data_rows = page.locator('tbody tr, table tr:not(:has(th))')
            data_row_count = data_rows.count()
            print(f"Data rows: {data_row_count}")
            
            # Try to click on contact rows
            for i in range(min(data_row_count, 5)):
                try:
                    row = data_rows.nth(i)
                    row_text = row.text_content()
                    if row_text:
                        print(f"  Row {i+1}: {row_text.strip()[:80]}")
                        # Click to view details
                        row.click()
                        time.sleep(0.5)
                        page.go_back()
                        time.sleep(0.3)
                except Exception as e:
                    print(f"    (Row {i+1} click skipped: {e})")
        
        # === INTERACT WITH API CONFIGURATION ===
        print("\n=== API CONFIGURATION ===")
        
        # Find input fields
        inputs = page.locator('input, textarea')
        input_count = inputs.count()
        print(f"Found {input_count} input fields")
        
        for i in range(input_count):
            try:
                inp = inputs.nth(i)
                input_type = inp.get_attribute('type') or 'text'
                input_placeholder = inp.get_attribute('placeholder') or ''
                input_value = inp.input_value() or ''
                input_id = inp.get_attribute('id') or ''
                input_name = inp.get_attribute('name') or ''
                print(f"  Input {i+1}: id={input_id[:20]}, name={input_name[:20]}, type={input_type}, placeholder={input_placeholder[:30]}, value={input_value[:30] if input_value else 'empty'}")
            except:
                pass
        
        # Find labels
        labels = page.locator('label')
        label_count = labels.count()
        print(f"Found {label_count} labels")
        for i in range(min(label_count, 10)):
            try:
                label_text = labels.nth(i).text_content()
                if label_text:
                    print(f"  Label: {label_text.strip()}")
            except:
                pass
        
        # === FIND AND CLICK ALL BUTTONS ===
        print("\n=== BUTTONS ===")
        buttons = page.locator('button, [role="button"], input[type="submit"], a.button, .btn')
        button_count = buttons.count()
        print(f"Found {button_count} buttons")
        
        buttons_clicked = []
        for i in range(button_count):
            try:
                btn = buttons.nth(i)
                btn_text = btn.text_content() or btn.get_attribute('value') or btn.get_attribute('aria-label') or 'Unknown'
                btn_text = btn_text.strip()[:50]
                if btn_text and btn_text != 'Unknown':
                    print(f"  Button {i+1}: {btn_text}")
                    buttons_clicked.append(btn_text)
                    # Click buttons (except destructive ones)
                    lower_text = btn_text.lower()
                    if 'upgrade' in lower_text or 'regenerate' in lower_text or 'save' in lower_text or 'submit' in lower_text or 'view' in lower_text or 'edit' in lower_text:
                        print(f"    Clicking: {btn_text}")
                        try:
                            btn.click()
                            time.sleep(1)
                            # Handle any alerts/modals
                            try:
                                page.wait_for_selector('.alert, .modal, [role="dialog"], .toast', timeout=2000)
                                print("    Dialog appeared, closing...")
                                page.keyboard.press('Escape')
                                time.sleep(0.5)
                            except:
                                pass
                            page.go_back()
                            time.sleep(0.3)
                        except Exception as e:
                            print(f"    Click error: {e}")
            except Exception as e:
                print(f"    (Button {i+1} skipped: {e})")
        
        # === FILL ANY FORMS FOUND ===
        print("\n=== FILLING FORMS ===")
        forms = page.locator('form')
        form_count = forms.count()
        print(f"Found {form_count} forms")
        
        # Try to fill any visible text inputs
        text_inputs = page.locator('input[type="text"], input[type="email"], input:not([type])')
        for i in range(text_inputs.count()):
            try:
                inp = text_inputs.nth(i)
                if inp.is_visible():
                    placeholder = inp.get_attribute('placeholder') or ''
                    print(f"  Filling input with placeholder: {placeholder[:40]}")
                    inp.fill('test@example.com')
                    time.sleep(0.3)
            except Exception as e:
                pass
        
        # === SCROLL THROUGH ENTIRE PAGE ===
        print("\n=== SCROLLING PAGE ===")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        time.sleep(1)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)
        
        # Take final screenshot
        page.screenshot(path='velocity2_final.png', full_page=True)
        print("✓ Final screenshot taken")
        
        # Extract all interactive elements info
        print("\n=== EXTRACTION SUMMARY ===")
        page_info = {
            'url': page.url,
            'title': title,
            'total_links': link_count,
            'metrics': metric_count,
            'charts': chart_count,
            'tables': table_count,
            'input_fields': input_count,
            'buttons': button_count,
            'buttons_clicked': buttons_clicked,
            'content_length': len(all_text)
        }
        
        with open('velocity2_interaction.json', 'w') as f:
            json.dump(page_info, f, indent=2)
        
        print(f"Interaction summary saved to velocity2_interaction.json")
        
        browser.close()
        print("\n✓ Interaction complete!")

if __name__ == '__main__':
    interact_with_velocity()
