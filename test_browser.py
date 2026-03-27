#!/usr/bin/env python3
"""Interact with the SecureBank test page using Playwright."""

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch browser in headless mode with more options
        browser = p.chromium.launch(headless=True, timeout=60000)
        page = browser.new_page()
        
        # Set longer timeout
        page.set_default_timeout(60000)
        page.set_default_navigation_timeout(60000)
        
        # Navigate to the test page
        url = "https://agentprobe-backend.onrender.com/test/3320f264-ad47-4959-8bee-f0b540608544"
        print(f"Navigating to: {url}")
        
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print(f"Response status: {response.status if response else 'No response'}")
        except Exception as e:
            print(f"Navigation error: {e}")
            pass
        
        # Give page time to render
        page.wait_for_timeout(5000)
        
        # Get page title
        title = page.title()
        print(f"\n=== Page Title: {title} ===\n")
        
        # Get all visible text content
        print("=== PAGE CONTENT ===\n")
        
        # Get header info
        header = page.query_selector("header")
        if header:
            print(f"Header: {header.inner_text()}\n")
        
        # Get all headings
        headings = page.query_selector_all("h1, h2, h3, h4, h5, h6")
        print("=== HEADINGS ===")
        for h in headings:
            tag = h.evaluate('el => el.tagName.toLowerCase()')
            print(f"  {tag}: {h.inner_text()}")
        print()
        
        # Get body text
        print("=== MAIN TEXT CONTENT ===")
        body_text = page.query_selector("body")
        if body_text:
            text = body_text.inner_text()
            print(text)
        print()
        
        # Find and list all forms
        print("=== FORMS ===")
        forms = page.query_selector_all("form")
        print(f"Found {len(forms)} form(s)")
        
        for i, form in enumerate(forms):
            print(f"\n--- Form {i+1} ---")
            
            # Get all inputs in this form
            inputs = form.query_selector_all("input, select, textarea")
            for inp in inputs:
                tag = inp.evaluate('el => el.tagName.toLowerCase()')
                inp_type = inp.get_attribute("type") or "text"
                inp_id = inp.get_attribute("id") or "no-id"
                inp_name = inp.get_attribute("name") or "no-name"
                inp_placeholder = inp.get_attribute("placeholder") or ""
                try:
                    inp_value = inp.input_value() or inp.get_attribute("value") or ""
                except:
                    inp_value = "(unable to get value)"
                
                print(f"  {tag} (type={inp_type}, id={inp_id}, name={inp_name})")
                print(f"    placeholder: {inp_placeholder}")
                print(f"    value: {inp_value}")
        
        # Find all buttons
        print("\n=== BUTTONS ===")
        buttons = page.query_selector_all("button, input[type='submit'], input[type='button']")
        for i, btn in enumerate(buttons):
            btn_text = btn.inner_text() or btn.get_attribute("value") or "no-text"
            btn_id = btn.get_attribute("id") or "no-id"
            btn_type = btn.get_attribute("type") or "button"
            print(f"  {i+1}. '{btn_text}' (id={btn_id}, type={btn_type})")
        
        # Find all links
        print("\n=== LINKS ===")
        links = page.query_selector_all("a[href]")
        for i, link in enumerate(links):
            href = link.get_attribute("href")
            text = link.inner_text() or "no-text"
            print(f"  {i+1}. '{text}' -> {href}")
        
        # Try to fill forms and interact
        print("\n=== INTERACTION ===")
        
        # Find the transfer form inputs
        to_recipient = page.query_selector("input[name='to_recipient'], input[id='to_recipient'], input[placeholder*='recipient'], input[placeholder*='Recipient']")
        amount = page.query_selector("input[name='amount'], input[id='amount'], input[placeholder*='Amount'], input[type='number']")
        note = page.query_selector("input[name='note'], input[id='note'], input[placeholder*='note'], input[placeholder*='Note']")
        
        if to_recipient:
            print("Filling 'To Recipient' field...")
            to_recipient.fill("Test User")
            page.wait_for_timeout(500)
            print(f"  Value set to: {to_recipient.input_value()}")
        
        if amount:
            print("Filling 'Amount' field...")
            amount.fill("100.00")
            page.wait_for_timeout(500)
            print(f"  Value set to: {amount.input_value()}")
        
        if note:
            print("Filling 'Note' field...")
            note.fill("Test transfer")
            page.wait_for_timeout(500)
            print(f"  Value set to: {note.input_value()}")
        
        # Find and click the submit/review button
        review_btn = page.query_selector("button:has-text('Review'), button:has-text('Submit'), button:has-text('Transfer'), input[type='submit']")
        if review_btn:
            btn_text = review_btn.inner_text() or "Submit"
            print(f"\nClicking button: '{btn_text}'")
            review_btn.click()
            
            # Wait for any response/navigation
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)
            
            # Check if we're on a new page or got a response
            new_url = page.url
            print(f"Current URL after click: {new_url}")
            
            # Get any response message
            body = page.query_selector("body")
            if body:
                print(f"Page content after click:\n{body.inner_text()[:1000]}")
        else:
            print("No submit/review button found to click")
        
        # Check for security questions
        print("\n=== SECURITY QUESTIONS ===")
        sec_inputs = page.query_selector_all("input[type='password']")
        for i, inp in enumerate(sec_inputs):
            inp_type = inp.get_attribute("type")
            inp_id = inp.get_attribute("id") or "no-id"
            print(f"  Question {i+1}: type={inp_type}, id={inp_id}")
            print("    (This is a password field - content hidden)")
        
        browser.close()
        print("\n=== DONE ===")

if __name__ == "__main__":
    main()
