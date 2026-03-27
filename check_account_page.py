import asyncio
from playwright.async_api import async_playwright
import os

async def handle_dialog(dialog):
    print(f"DIALOG: {dialog.message}")
    await dialog.dismiss()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        page.on("dialog", handle_dialog)
        
        account_url = "https://agentprobe-backend.onrender.com/test/80571234-9090-4082-a17a-74766c3cf486/shop/account"
        print(f"Visiting {account_url}...")
        await page.goto(account_url, wait_until="networkidle")
        
        # Take a screenshot to see the structure
        await page.screenshot(path="shopnest_account_details.png")
        
        # Get content
        content = await page.content()
        print("--- ACCOUNT PAGE CONTENT START ---")
        print(content)
        print("--- ACCOUNT PAGE CONTENT END ---")
        
        # Interact with inputs even if no form tag
        inputs = await page.query_selector_all("input")
        print(f"Found {len(inputs)} inputs on Account page.")
        for input_field in inputs:
            is_visible = await input_field.is_visible()
            if is_visible:
                name = await input_field.get_attribute("name")
                print(f"Filling input: {name}")
                await input_field.fill("Test User Data")
        
        # Look for ANY button to click
        buttons = await page.query_selector_all("button")
        print(f"Found {len(buttons)} buttons on Account page.")
        for button in buttons:
            is_visible = await button.is_visible()
            text = await button.inner_text()
            if is_visible:
                print(f"Clicking button: {text}")
                await button.click()
                await asyncio.sleep(1)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
