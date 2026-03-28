import asyncio
from playwright.async_api import async_playwright
import os

async def interact_with_page(page, url_name, screenshot_name):
    print(f"\n--- Reading content of {url_name} ---")
    text = await page.evaluate("() => document.body.innerText")
    print(text)
    
    try:
        await page.screenshot(path=f"{screenshot_name}_initial.png", full_page=True)
    except:
        pass
    
    # Fill any forms found
    try:
        inputs = await page.query_selector_all("input, textarea")
        for i, input_el in enumerate(inputs):
            name_attr = await input_el.get_attribute("name")
            id_attr = await input_el.get_attribute("id")
            placeholder = await input_el.get_attribute("placeholder")
            type_attr = await input_el.get_attribute("type")
            
            label = name_attr or id_attr or placeholder or f"input_{i}"
            
            try:
                if "feedback" in label:
                    # Use force and shorter timeout for hidden/problematic elements
                    await input_el.fill("I am experiencing a great session today. The interface is intuitive.", force=True, timeout=5000)
                elif type_attr == "number":
                    await input_el.fill("1", force=True, timeout=5000)
                elif type_attr == "email":
                    await input_el.fill("test@example.com", force=True, timeout=5000)
                elif type_attr == "password":
                    await input_el.fill("Password123!", force=True, timeout=5000)
                elif type_attr == "tel":
                    await input_el.fill("1234567890", force=True, timeout=5000)
                else:
                    await input_el.fill("Test Data Interaction", force=True, timeout=5000)
                print(f"Filled input: {label}")
            except Exception as e:
                print(f"Skipping input {label}: {e}")
    except Exception as e:
        print(f"Error gathering inputs on {url_name}: {e}")

    # Click all buttons on the page
    try:
        buttons = await page.query_selector_all("button")
        for i, button in enumerate(buttons):
            text = await button.inner_text()
            print(f"Clicking button: {text}")
            try:
                page.once("dialog", lambda dialog: dialog.dismiss())
                await button.click(force=True, timeout=5000)
                await page.wait_for_timeout(500)
            except Exception as e:
                print(f"Could not click button {text}: {e}")
    except Exception as e:
        print(f"Error gathering buttons on {url_name}: {e}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        base_url = "https://agentprobe-backend.onrender.com/test/d02da659-b40a-4fa2-8892-7aff46a9f7de"
        
        # 1. Main Shop Page
        print(f"Visiting {base_url}...")
        await page.goto(base_url, wait_until="load", timeout=60000)
        await interact_with_page(page, "Shop Main", "velocity_shop")
        
        # Get navigation links
        nav_links = await page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('nav a'));
            return links.map(a => ({ text: a.innerText, href: a.href }));
        }""")
        
        # 2. Visit each nav link
        for link in nav_links:
            if "Home" in link['text']: continue
            print(f"\nNavigating to {link['text']} ({link['href']})")
            try:
                await page.goto(link['href'], wait_until="load", timeout=60000)
                await interact_with_page(page, link['text'], "velocity_" + link['text'].lower())
            except Exception as e:
                print(f"Failed to navigate to {link['text']}: {e}")

        # Final wait for any async events to fire
        print("\nWaiting for final event processing...")
        await page.wait_for_timeout(5000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
