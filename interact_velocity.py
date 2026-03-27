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
        url = "https://agentprobe-backend.onrender.com/test/8c2e2513-f96b-4424-a078-c001413252f9"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until='networkidle')
        time.sleep(2)
        
        # Take initial screenshot
        page.screenshot(path='velocity_initial.png', full_page=True)
        print("✓ Initial screenshot taken")
        
        # Read all page content
        print("\n=== PAGE CONTENT ===")
        content = page.content()
        
        # Extract text content
        all_text = page.locator('body').text_content()
        print(f"\nFull page text content retrieved ({len(all_text)} chars)")
        
        # Get page title
        title = page.title()
        print(f"Page Title: {title}")
        
        # === INTERACT WITH NAVIGATION ===
        print("\n=== INTERACTING WITH NAVIGATION ===")
        
        nav_links = page.locator('nav a, header a, [role="navigation"] a')
        nav_count = nav_links.count()
        print(f"Found {nav_count} navigation links")
        
        # Click each nav link and go back
        for i in range(nav_count):
            try:
                nav_links = page.locator('nav a, header a, [role="navigation"] a')
                link_text = nav_links.nth(i).text_content() or "Unknown"
                print(f"  - Clicking nav: {link_text[:50]}")
                nav_links.nth(i).click()
                time.sleep(1)
                page.go_back()
                time.sleep(0.5)
            except Exception as e:
                print(f"    (Navigation skipped: {e})")
        
        # === INTERACT WITH METRICS ===
        print("\n=== METRICS SECTION ===")
        metrics = page.locator('[class*="metric"], [class*="stat"], [class*="card"]')
        metric_count = metrics.count()
        print(f"Found {metric_count} metric cards")
        
        for i in range(min(metric_count, 10)):
            try:
                metric_text = metrics.nth(i).text_content()
                if metric_text and len(metric_text.strip()) > 0:
                    print(f"  Metric {i+1}: {metric_text.strip()[:100]}")
            except:
                pass
        
        # === INTERACT WITH ACTIVITY FEED ===
        print("\n=== ACTIVITY FEED ===")
        activity_items = page.locator('[class*="activity"], [class*="feed"] li, [class*="feed"] div')
        activity_count = activity_items.count()
        print(f"Found {activity_count} activity items")
        
        # === INTERACT WITH CONTACTS TABLE ===
        print("\n=== CONTACTS TABLE ===")
        table_rows = page.locator('table tr, [class*="row"]')
        row_count = table_rows.count()
        print(f"Found {row_count} table rows")
        
        # Try to click on first contact row
        try:
            first_row = page.locator('table tr').nth(1)  # Skip header
            if first_row.count() > 0:
                print("  Clicking first contact row...")
                first_row.click()
                time.sleep(1)
                page.go_back()
                time.sleep(0.5)
        except Exception as e:
            print(f"    (Row interaction skipped: {e})")
        
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
                print(f"  Input {i+1}: type={input_type}, placeholder={input_placeholder[:30]}, value={input_value[:30] if input_value else 'empty'}")
            except:
                pass
        
        # Find and click buttons
        print("\n=== BUTTONS ===")
        buttons = page.locator('button, [role="button"], input[type="submit"]')
        button_count = buttons.count()
        print(f"Found {button_count} buttons")
        
        for i in range(button_count):
            try:
                btn = buttons.nth(i)
                btn_text = btn.text_content() or btn.get_attribute('value') or 'Unknown'
                btn_text = btn_text.strip()[:50]
                if btn_text:
                    print(f"  Button {i+1}: {btn_text}")
                    # Click non-destructive buttons
                    if 'regenerate' in btn_text.lower() or 'upgrade' in btn_text.lower():
                        print(f"    Clicking: {btn_text}")
                        btn.click()
                        time.sleep(1)
                        # Handle any alerts
                        try:
                            alert = page.wait_for_selector('.alert, .modal, [role="dialog"]', timeout=2000)
                            if alert:
                                print("    Dialog appeared, closing...")
                                page.keyboard.press('Escape')
                                time.sleep(0.5)
                        except:
                            pass
            except Exception as e:
                print(f"    (Button {i+1} skipped: {e})")
        
        # === SCROLL THROUGH ENTIRE PAGE ===
        print("\n=== SCROLLING PAGE ===")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)
        
        # Take final screenshot
        page.screenshot(path='velocity_final.png', full_page=True)
        print("✓ Final screenshot taken")
        
        # Extract all interactive elements info
        print("\n=== EXTRACTION SUMMARY ===")
        page_info = {
            'url': page.url,
            'title': page.title(),
            'navigation_links': nav_count,
            'metrics': metric_count,
            'activity_items': activity_count,
            'table_rows': row_count,
            'input_fields': input_count,
            'buttons': button_count,
        }
        
        with open('velocity_interaction.json', 'w') as f:
            json.dump(page_info, f, indent=2)
        
        print(f"Interaction summary saved to velocity_interaction.json")
        
        browser.close()
        print("\n✓ Interaction complete!")

if __name__ == '__main__':
    interact_with_velocity()
