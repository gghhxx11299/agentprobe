import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "https://agentprobe-backend.onrender.com/test/8c2e2513-f96b-4424-a078-c001413252f9"
        print(f"Navigating to {url}...")
        
        try:
            await page.goto(url, wait_until="networkidle")
            
            # Wait a bit for any dynamic content
            await page.wait_for_timeout(2000)
            
            content = await page.content()
            title = await page.title()
            print(f"Page Title: {title}")
            
            # Check for frames
            frames = page.frames
            print(f"Number of frames: {len(frames)}")
            
            # Take a screenshot
            await page.screenshot(path="target_screenshot.png", full_page=True)
            print("Screenshot saved as target_screenshot.png")
            
            # List all buttons and inputs
            buttons = await page.query_selector_all("button")
            inputs = await page.query_selector_all("input")
            links = await page.query_selector_all("a")
            
            print(f"Found {len(buttons)} buttons, {len(inputs)} inputs, {len(links)} links.")
            
            for i, button in enumerate(buttons):
                text = await button.inner_text()
                print(f"Button {i}: '{text.strip()}'")
                
            for i, input_el in enumerate(inputs):
                type_attr = await input_el.get_attribute("type")
                name_attr = await input_el.get_attribute("name")
                id_attr = await input_el.get_attribute("id")
                print(f"Input {i}: type='{type_attr}', name='{name_attr}', id='{id_attr}'")
                
            # Print page text
            body_text = await page.inner_text("body")
            print("--- PAGE TEXT ---")
            print(body_text)
            print("--- END PAGE TEXT ---")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
