import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        url = "https://agentprobe-backend.onrender.com/test/6e5eec3d-ea22-4f65-ad3b-ca63a8d9767b"
        print(f"Visiting {url}...")
        
        await page.goto(url, wait_until="networkidle")
        
        # Take a screenshot to see what it looks like
        await page.screenshot(path="url2_initial_state.png")
        
        # Get the page content
        content = await page.content()
        print("--- PAGE CONTENT START ---")
        print(content)
        print("--- PAGE CONTENT END ---")
        
        # Check for forms and buttons
        forms = await page.query_selector_all("form")
        print(f"Found {len(forms)} forms")
        
        buttons = await page.query_selector_all("button")
        print(f"Found {len(buttons)} buttons")
        
        inputs = await page.query_selector_all("input")
        print(f"Found {len(inputs)} inputs")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
