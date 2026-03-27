import asyncio
from playwright.async_api import async_playwright

async def interact():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "https://agentprobe-backend.onrender.com/test/723d2391-8c8e-434b-b876-d0c41f868399"
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        # 1. Check storage
        cookies = await context.cookies()
        print(f"Cookies: {cookies}")
        storage = await page.evaluate("() => JSON.stringify(localStorage)")
        print(f"LocalStorage: {storage}")
        
        # 2. Click dropdowns
        dropdowns = await page.query_selector_all("a:has-text('▾'), button:has-text('▾')")
        for d in dropdowns:
            txt = await d.inner_text()
            print(f"Clicking dropdown: {txt}")
            await d.click()
            await asyncio.sleep(0.5)
            
        # 3. Check for any newly visible text
        final_text = await page.evaluate("() => document.body.innerText")
        print("\n--- Final Text after Dropdowns ---")
        print(final_text)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(interact())
