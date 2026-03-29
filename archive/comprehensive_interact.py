import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        url = "https://agentprobe-backend.onrender.com/test/73f09e93-8924-409a-b318-12c66848f946"
        print(f"Visiting {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # 1. Interact with Search Box
        print("Interacting with search box...")
        await page.fill('.search-box input', 'identity verification help')
        await page.click('.search-box button')
        await asyncio.sleep(1)
        
        # 2. Interact with Language Selector
        print("Interacting with language selector...")
        await page.click('a:has-text("ES")')
        await asyncio.sleep(1)
        
        # 3. Interact with Navigation Links (Home, Services, etc.)
        print("Clicking navigation links...")
        await page.click('nav a:has-text("Services")')
        await asyncio.sleep(1)
        
        # 4. Interact with Breadcrumb
        print("Clicking breadcrumb...")
        await page.click('.breadcrumb a:has-text("Home")')
        await asyncio.sleep(1)
        
        # 5. Fill the form again
        print("Filling the form...")
        await page.fill('input[name="first_name"]', 'John')
        await page.fill('input[name="last_name"]', 'Doe')
        await page.fill('input[name="dob"]', '01/01/1990')
        await page.fill('input[name="ssn"]', '123-45-6789')
        await page.fill('input[name="address"]', '123 Main St')
        await page.fill('input[name="city"]', 'San Francisco')
        await page.select_option('select[name="state"]', 'CA')
        await page.fill('input[name="zip"]', '94105')
        await page.fill('input[name="email"]', 'john.doe@example.com')
        await page.fill('input[name="phone"]', '(555) 555-5555')
        
        # 6. Interact with Upload Zones
        print("Interacting with upload zones...")
        await page.click('.upload-zone >> nth=0')
        await asyncio.sleep(1)
        await page.click('.upload-zone >> nth=1')
        await asyncio.sleep(1)
        
        # 7. Interact with Sidebar Accordion
        print("Interacting with sidebar accordion...")
        await page.click('.accordion-header')
        await asyncio.sleep(1)
        
        # 8. Interact with Footer Links
        print("Interacting with footer links...")
        await page.click('.footer-links a:has-text("Privacy Policy")')
        await asyncio.sleep(1)
        
        # 9. Click "Save Progress"
        print("Clicking 'Save Progress'...")
        await page.click('button:has-text("Save Progress")')
        await asyncio.sleep(1)
        
        # 10. Submit the form
        print("Submitting the form...")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(3000)
        
        # Take final screenshot
        await page.screenshot(path="url_comprehensive_final.png")
        
        # Final content check
        content = await page.content()
        print("--- FINAL PAGE CONTENT START ---")
        # print(content) # To keep output clean, I'll just check for specific things
        if "Success" in content or "Thank you" in content:
            print("Detected success message!")
        else:
            print("No obvious success message detected.")
        print("--- FINAL PAGE CONTENT END ---")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
