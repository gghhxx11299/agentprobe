import asyncio
import argparse
import json
import os
import re
from playwright.async_api import async_playwright

class AgentProbeRunner:
    """
    A standardized, autonomous agent runner for AgentProbe.
    Simulates an LLM agent by using generic discovery rather than hardcoded IDs.
    """
    def __init__(self, session_id, base_url="http://localhost:8000"):
        self.session_id = session_id
        self.base_url = base_url.rstrip('/')
        self.target_url = f"{self.base_url}/test/{session_id}"
        self.reasoning_log = []

    def log_reasoning(self, thought):
        print(f"[AGENT THOUGHT]: {thought}")
        self.reasoning_log.append(thought)

    async def run_task(self, primary_task):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent="AgentProbe-Evaluator/1.0 (Autonomous-Adversarial-Test)"
            )
            page = await context.new_page()

            try:
                self.log_reasoning(f"Navigating to {self.target_url}")
                await page.goto(self.target_url, wait_until="networkidle")
                
                # 1. Page Discovery
                title = await page.title()
                self.log_reasoning(f"Target page loaded: {title}. Primary Task: {primary_task}")

                # 2. Autonomous Interaction (Generic Discovery)
                # Instead of hardcoded IDs, we look for anything that looks like a task requirement
                self.log_reasoning("Scanning page for actionable elements...")
                
                # Discovery: Find all visible links and buttons
                elements = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('a, button, input[type="button"], input[type="submit"]'))
                        .filter(el => {
                            const rect = el.getBoundingClientRect();
                            return rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';
                        })
                        .map(el => ({
                            tag: el.tagName,
                            text: el.innerText || el.value || el.placeholder || el.alt || "",
                            href: el.href || null,
                            type: el.type || null
                        }));
                }''')

                # Logic: If any element text matches a "security" or "identity" prompt, 
                # a 'naive' agent might follow it thinking it's required for the session.
                for el in elements:
                    text = el['text'].lower()
                    if any(keyword in text for keyword in ["verify", "identity", "security", "session", "confirm"]):
                        self.log_reasoning(f"Noticed a security-related element: '{el['text']}'. Attempting to verify to ensure session continuity.")
                        try:
                            # Use Playwright's generic text locator
                            await page.get_by_text(el['text']).first.click(timeout=3000)
                            await page.wait_for_timeout(1000)
                            self.log_reasoning(f"Successfully interacted with '{el['text']}'.")
                            
                            # If we navigated away, go back to the primary task
                            if page.url != self.target_url:
                                await page.goto(self.target_url, wait_until="networkidle")
                        except:
                            continue

                # 3. Form Completion (Generic)
                self.log_reasoning("Proceeding to complete the primary task.")
                inputs = await page.query_selector_all("input:not([type='hidden']), textarea, select")
                for field in inputs:
                    if await field.is_visible():
                        label = await field.evaluate("el => el.placeholder || el.name || el.id || ''")
                        val = "Test User"
                        if "email" in label.lower(): val = "test@example.com"
                        elif "amount" in label.lower(): val = "100.00"
                        
                        await field.fill(val)

                # 4. Final Submission
                submit_btn = page.locator("button:has-text('Submit'), button:has-text('Order'), button:has-text('Transfer'), .btn")
                if await submit_btn.first.count() > 0:
                    self.log_reasoning("Attempting to submit the final action.")
                    await submit_btn.first.click()
                    await page.wait_for_timeout(2000)

                self.log_reasoning("Task completed. Capturing final state.")
                await page.screenshot(path=f"test_results/{self.session_id}_final.png")

            except Exception as e:
                self.log_reasoning(f"Error during execution: {str(e)}")
            finally:
                await browser.close()
                return "\n".join(self.reasoning_log)

async def submit_analysis(session_id, reasoning, base_url):
    import requests
    url = f"{base_url}/results/{session_id}/analyze"
    try:
        res = requests.post(url, json={"raw_output": reasoning})
        print(f"\n[ANALYSIS RESULT]: {json.dumps(res.json(), indent=2)}")
    except Exception as e:
        print(f"Failed to submit analysis: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--task", default="Complete the primary transaction on the page.")
    parser.add_argument("--host", default="http://localhost:8000")
    args = parser.parse_args()

    os.makedirs("test_results", exist_ok=True)
    runner = AgentProbeRunner(args.session, args.host)
    reasoning = asyncio.run(runner.run_task(args.task))
    asyncio.run(submit_analysis(args.session, reasoning, args.host))
