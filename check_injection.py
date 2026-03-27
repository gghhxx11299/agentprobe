import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        # Try the injection link directly
        url = "https://agentprobe-backend.onrender.com/probe/0b4f0998-6824-4662-bb21-52b3c16b3fd6/hidden_text_injection"
        print(f"Visiting {url}...")
        
        try:
            await page.goto(url, wait_until="load", timeout=120000)
            
            # Wait for content to appear
            print("Waiting for content to load...")
            # We can wait for any text that isn't the Render logo or 'APPLICATION LOADING'
            try:
                # Wait for any element that looks like the result
                await page.wait_for_timeout(10000) # Give it some fixed time
                
                # Check for specific confirmation text
                content = await page.evaluate("() => document.body.innerText")
                print("Page content (first 1000 chars):")
                print(content[:1000])
                
                if "INJECTION_CONFIRMED" in content:
                    print("Report: INJECTION_CONFIRMED")
                
                # Try to scroll and wait more if needed
                if "APPLICATION LOADING" in content:
                     print("Still loading, waiting another 15 seconds...")
                     await page.wait_for_timeout(15000)
                     content = await page.evaluate("() => document.body.innerText")
                     print("Updated page content:")
                     print(content[:1000])
                     if "INJECTION_CONFIRMED" in content:
                        print("Report: INJECTION_CONFIRMED")

            except Exception as e:
                print(f"Error during waiting: {e}")
            
            await page.screenshot(path="injection_link_final.png")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
