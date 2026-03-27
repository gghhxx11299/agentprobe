import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        url = "https://agentprobe-backend.onrender.com/test/0b4f0998-6824-4662-bb21-52b3c16b3fd6"
        print(f"Visiting {url}...")
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(3000) # Give it some time for JS
        
        # Check for iframes
        frames = page.frames
        print(f"Number of frames: {len(frames)}")
        for i, frame in enumerate(frames):
            print(f"Frame {i}: name='{frame.name}', url='{frame.url}'")
            # Try to see content in frames
            try:
                content = await frame.content()
                print(f"  Frame {i} content length: {len(content)}")
                # Find buttons/links in this frame
                btns = await frame.query_selector_all("button, a")
                print(f"  Frame {i} found {len(btns)} buttons/links.")
                for btn in btns:
                    text = await btn.inner_text()
                    href = await btn.get_attribute("href")
                    print(f"    - '{text.strip()}' (href: {href})")
            except:
                pass

        # Check main page again with wait_for_selector
        print("Checking main page elements...")
        try:
            # Wait for any button to be sure
            await page.wait_for_selector("button, a, input", timeout=5000)
            all_text = await page.evaluate("() => document.body.innerText")
            print("Main Page text snippet (first 500 chars):")
            print(all_text[:500])
            
            # Find all inputs
            inputs = await page.query_selector_all("input")
            print(f"Total inputs: {len(inputs)}")
            for inp in inputs:
                name = await inp.get_attribute("name")
                type_ = await inp.get_attribute("type")
                placeholder = await inp.get_attribute("placeholder")
                print(f"  Input: name='{name}', type='{type_}', placeholder='{placeholder}'")
        except Exception as e:
            print(f"Error finding main page elements: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
