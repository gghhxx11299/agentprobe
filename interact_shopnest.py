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
        
        # Listen for dialogs correctly
        page.on("dialog", handle_dialog)
        
        base_url = "https://agentprobe-backend.onrender.com/test/80571234-9090-4082-a17a-74766c3cf486"
        print(f"Visiting {base_url}...")
        await page.goto(base_url, wait_until="networkidle")
        
        # 1. Click all "Add to Cart" buttons
        buttons = await page.query_selector_all('button:has-text("Add to Cart")')
        print(f"Found {len(buttons)} Add to Cart buttons.")
        for i, button in enumerate(buttons):
            print(f"Clicking button {i+1}...")
            await button.click()
            await asyncio.sleep(0.5)
            
        # 2. Scroll to the bottom
        print("Scrolling to bottom...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        
        # 3. Get all navigation links
        nav_links = await page.query_selector_all('nav a')
        link_hrefs = []
        for link in nav_links:
            href = await link.get_attribute('href')
            if href:
                link_hrefs.append(href)
        
        print(f"Found navigation links: {link_hrefs}")
        
        # 4. Visit each navigation link
        for href in link_hrefs:
            full_url = f"https://agentprobe-backend.onrender.com{href}"
            print(f"Visiting {full_url}...")
            await page.goto(full_url, wait_until="networkidle")
            
            # Check for forms on these pages
            forms = await page.query_selector_all("form")
            print(f"Page {href} has {len(forms)} forms.")
            
            # If there's a form, fill it
            if "checkout" in href or "account" in href:
                inputs = await page.query_selector_all("input")
                print(f"Page {href} has {len(inputs)} inputs.")
                for input_field in inputs:
                    name = await input_field.get_attribute("name")
                    type_attr = await input_field.get_attribute("type")
                    is_visible = await input_field.is_visible()
                    if is_visible and type_attr not in ["submit", "button", "checkbox", "radio"]:
                        await input_field.fill("Test Data")
                
                submit_btn = await page.query_selector('button[type="submit"], input[type="submit"]')
                if submit_btn:
                    print("Submitting form...")
                    await submit_btn.click()
                    await asyncio.sleep(2)

            await page.screenshot(path=f"shopnest_{href.split('/')[-1]}.png")
            await asyncio.sleep(1)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
