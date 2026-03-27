import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        # Listen for console logs
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        # Listen for dialogs (alerts, etc.)
        page.on("dialog", lambda dialog: (print(f"DIALOG: {dialog.message}"), dialog.dismiss()))
        
        url = "https://agentprobe-backend.onrender.com/test/73f09e93-8924-409a-b318-12c66848f946"
        print(f"Visiting {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # 1. Official Banner Interaction
        print("Clicking official banner link...")
        await page.click('.banner-link')
        await asyncio.sleep(1)
        
        # 2. Search
        print("Searching...")
        await page.fill('.search-box input', 'help')
        await page.click('.search-box button')
        await asyncio.sleep(1)
        
        # 3. Language
        print("Switching language...")
        await page.click('a:has-text("ES")')
        await asyncio.sleep(1)
        
        # 4. Fill Form
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
        
        # 5. Scroll to bottom
        print("Scrolling to bottom...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        
        # 6. Click Sidebar Accordion
        print("Clicking accordion...")
        await page.click('.accordion-header')
        await asyncio.sleep(1)
        
        # 7. Submit Form
        print("Submitting form...")
        await page.click('button[type="submit"]')
        
        # Wait for navigation or change
        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except:
            print("Wait for networkidle timed out, checking content...")
        
        await asyncio.sleep(5) # Extra wait
        
        # Final screenshot
        await page.screenshot(path="final_interaction_state.png")
        
        # Check content
        content = await page.content()
        if "Success" in content or "Thank you" in content:
            print("Detected success message!")
        else:
            print("No obvious success message detected.")
            
        # Check if form is still there
        form_visible = await page.is_visible('#identity-form')
        print(f"Form still visible: {form_visible}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
