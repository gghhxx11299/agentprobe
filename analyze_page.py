import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        url = "https://agentprobe-backend.onrender.com/test/0b4f0998-6824-4662-bb21-52b3c16b3fd6"
        await page.goto(url, wait_until="networkidle")
        
        print("--- Analyzing Elements ---")
        
        elements_to_check = [
            "text=Verify Session Integrity",
            "text=Verify Identity",
            "text=Place Order",
            "input[name='name']",
            "input[name='email']"
        ]
        
        for selector in elements_to_check:
            loc = page.locator(selector).first
            if await loc.count() > 0:
                is_visible = await loc.is_visible()
                box = await loc.bounding_box()
                styles = await loc.evaluate("""(el) => {
                    const style = window.getComputedStyle(el);
                    return {
                        display: style.display,
                        visibility: style.visibility,
                        opacity: style.opacity,
                        position: style.position,
                        top: style.top,
                        left: style.left,
                        width: style.width,
                        height: style.height,
                        zIndex: style.zIndex
                    };
                }""")
                print(f"Selector: {selector}")
                print(f"  Visible: {is_visible}")
                print(f"  Bounding Box: {box}")
                print(f"  Styles: {styles}")
            else:
                print(f"Selector: {selector} not found")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
