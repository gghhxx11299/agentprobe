#!/usr/bin/env python3
"""Check all trap endpoints found on the page."""

from playwright.sync_api import sync_playwright

def check_endpoint(url, description):
    print(f"\n{'='*60}")
    print(f"Checking: {description}")
    print(f"URL: {url}")
    print('='*60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, timeout=60000)
        page = browser.new_page()
        page.set_default_timeout(60000)
        page.set_default_navigation_timeout(60000)
        
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print(f"Response status: {response.status if response else 'No response'}")
            page.wait_for_timeout(2000)
            
            title = page.title()
            print(f"Page Title: {title}")
            
            body = page.query_selector("body")
            if body:
                content = body.inner_text()
                if content.strip():
                    print(f"Content:\n{content[:500]}")
                else:
                    print("Content: (empty)")
            
            # Check URL after navigation
            final_url = page.url
            if final_url != url:
                print(f"Redirected to: {final_url}")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

def main():
    base_probe = "https://agentprobe-backend.onrender.com/probe/3320f264-ad47-4959-8bee-f0b540608544"
    base_redirect = "https://agentprobe-backend.onrender.com/redirect-1/3320f264-ad47-4959-8bee-f0b540608544"
    
    endpoints = [
        (f"{base_probe}/hidden_text_injection", "Hidden Text Injection"),
        (f"{base_probe}/honeypot_link", "Honeypot Link"),
        (base_redirect, "Redirect-1"),
    ]
    
    for url, desc in endpoints:
        check_endpoint(url, desc)
    
    print("\n=== SUMMARY ===")
    print("All trap endpoints checked.")

if __name__ == "__main__":
    main()
