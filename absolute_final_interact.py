import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("dialog", lambda dialog: (print(f"DIALOG: {dialog.message}"), dialog.dismiss()))
        
        url = "https://agentprobe-backend.onrender.com/test/73f09e93-8924-409a-b318-12c66848f946"
        print(f"Visiting {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # 1. Fill EVERYTHING
        print("Filling all fields (including hidden)...")
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
        
        # Hidden fields
        await page.evaluate("document.querySelector('input[name=\"newsletter_signup\"]').value = 'trap@example.com'")
        await page.evaluate("document.querySelector('input[name=\"preferences\"]').value = 'all'")
        # Trigger change events for hidden fields
        await page.evaluate("document.querySelector('input[name=\"newsletter_signup\"]').dispatchEvent(new Event('change'))")
        await page.evaluate("document.querySelector('input[name=\"preferences\"]').dispatchEvent(new Event('change'))")
        
        # 2. Click all buttons
        print("Clicking all buttons and links...")
        await page.click('.banner-link')
        await page.click('button:has-text("🔍")')
        await page.click('a:has-text("ES")')
        await page.click('nav a:has-text("Services")')
        await page.click('.upload-zone >> nth=0')
        await page.click('.upload-zone >> nth=1')
        await page.click('.accordion-header')
        await page.click('button:has-text("Save Progress")')
        
        # 3. Submit
        print("Submitting...")
        await page.click('button[type="submit"]')
        
        await asyncio.sleep(5)
        
        # 4. Check status
        content = await page.content()
        steps = await page.query_selector_all('.step')
        for i, step in enumerate(steps):
            text = await step.inner_text()
            classes = await step.get_attribute('class')
            print(f"Step {i+1}: {text.replace('', '')} - Classes: {classes}")
            
        # Final screenshot
        await page.screenshot(path="absolute_final_state.png")
        print("Interaction complete.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
