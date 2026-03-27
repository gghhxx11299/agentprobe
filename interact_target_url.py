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
        
        # Fill the form
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
        
        # Take a screenshot after filling
        await page.screenshot(path="url_filled_state.png")
        
        # Click "Save Progress" button
        print("Clicking 'Save Progress'...")
        await page.click('button:has-text("Save Progress")')
        await asyncio.sleep(1) # Wait a bit for any feedback
        
        # Click "Continue →" (Submit)
        print("Submitting the form...")
        # The button is a submit button in the form
        await page.click('button[type="submit"]')
        
        # Wait for navigation or change
        await asyncio.sleep(3)
        
        # Take a final screenshot
        await page.screenshot(path="url_final_state.png")
        
        # Check new content
        content = await page.content()
        print("--- FINAL PAGE CONTENT START ---")
        print(content)
        print("--- FINAL PAGE CONTENT END ---")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
