#!/usr/bin/env python3
"""Check the hidden text injection endpoint."""

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, timeout=60000)
        page = browser.new_page()
        
        page.set_default_timeout(60000)
        page.set_default_navigation_timeout(60000)
        
        url = "https://agentprobe-backend.onrender.com/probe/3320f264-ad47-4959-8bee-f0b540608544/hidden_text_injection"
        print(f"Navigating to: {url}")
        
        response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print(f"Response status: {response.status if response else 'No response'}")
        
        page.wait_for_timeout(3000)
        
        title = page.title()
        print(f"\n=== Page Title: {title} ===\n")
        
        body = page.query_selector("body")
        if body:
            print("=== FULL PAGE CONTENT ===")
            print(body.inner_text())
        
        # Check for any hidden elements
        print("\n=== CHECKING FOR HIDDEN ELEMENTS ===")
        all_elements = page.query_selector_all("*")
        for i, el in enumerate(all_elements):
            is_hidden = el.evaluate('''el => {
                const style = window.getComputedStyle(el);
                return style.display === 'none' || 
                       style.visibility === 'hidden' || 
                       style.opacity === '0' ||
                       el.offsetWidth === 0 ||
                       el.offsetHeight === 0
            }''')
            if is_hidden:
                tag = el.evaluate('el => el.tagName.toLowerCase()')
                text = el.inner_text()[:100] if el.inner_text else ""
                print(f"  Hidden element {i}: <{tag}> - Text: {text}")
        
        browser.close()
        print("\n=== DONE ===")

if __name__ == "__main__":
    main()
