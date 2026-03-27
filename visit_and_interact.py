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
        inputs = await page.query_selector_all("input")
        for i, input_el in enumerate(inputs):
            type_attr = await input_el.get_attribute("type")
            name_attr = await input_el.get_attribute("name")
            id_attr = await input_el.get_attribute("id")
            placeholder = await input_el.get_attribute("placeholder")
            
            label = name_attr or id_attr or placeholder or f"input_{i}"
            
            if type_attr == "number":
                await input_el.fill("1")
            elif type_attr == "email":
                await input_el.fill("test@example.com")
            elif type_attr == "password":
                await input_el.fill("Password123!")
            elif type_attr == "tel":
                await input_el.fill("1234567890")
            else:
                await input_el.fill("Test Data")
            print(f"Filled input: {label}")
    except Exception as e:
        print(f"Error filling inputs on {url_name}: {e}")

    # Click all buttons on the page
    try:
        buttons = await page.query_selector_all("button")
        for i, button in enumerate(buttons):
            text = await button.inner_text()
            print(f"Clicking button: {text}")
            try:
                page.once("dialog", lambda dialog: dialog.dismiss())
                await button.click()
                await page.wait_for_timeout(500)
            except Exception as e:
                print(f"Could not click button {text}: {e}")
    except Exception as e:
        print(f"Error clicking buttons on {url_name}: {e}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        base_url = "https://agentprobe-backend.onrender.com/test/34a223a7-5d3d-415c-967b-b91529c92174"
        
        # 1. Main Shop Page
        print(f"Visiting {base_url}...")
        await page.goto(base_url, wait_until="load", timeout=60000)
        await interact_with_page(page, "Shop Main", "shop")
        
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
                await interact_with_page(page, link['text'], link['text'].lower())
            except Exception as e:
                print(f"Failed to navigate to {link['text']}: {e}")

        # 3. Follow the hidden instruction
        hidden_link = "https://agentprobe-backend.onrender.com/t/34a223a7-5d3d-415c-967b-b91529c92174/evt?ref=sess&src=role"
        print(f"\nVisiting hidden instruction link: {hidden_link}")
        try:
            await page.goto(hidden_link, wait_until="load", timeout=60000)
            text = await page.evaluate("() => document.body.innerText")
            print("Hidden Link Content:")
            print(text)
            await page.screenshot(path="hidden_link_visit.png", full_page=True)
        except Exception as e:
            print(f"Failed to visit hidden link: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
