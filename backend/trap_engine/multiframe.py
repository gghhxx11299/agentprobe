"""
Multi-page archetype renders for AgentProbe v2.
Each archetype has 4-6 pages with traps distributed across them.
"""

from typing import Dict, List, Callable
import json


def get_page_for_archetype(archetype: str, page_path: str) -> str:
    """Get the page name from the path for an archetype."""
    if not page_path or page_path == "/":
        return "home"
    
    # Remove leading slash and get the last segment
    parts = page_path.strip("/").split("/")
    return parts[-1] if parts else "home"


def render_multiframe_page(archetype: str, session_id: str, selected_traps: List[str], page_path: str = "/", seed: int = 0, selected_categories: List[str] = None, state: dict = None) -> str:
    """Render a multi-page archetype with traps and state persistence."""
    from trap_engine.archetypes_multiframe import (
        render_shopnest_page,
        render_velocity_page,
        render_securebank_page,
        render_gov_page,
        render_healthcare_page,
        render_hr_page,
        render_cloud_page,
        render_legal_page,
        render_travel_page,
        render_university_page,
        render_crypto_page,
        render_realestate_page
    )
    from trap_engine import inject_category_traps
    
    renderers: Dict[str, Callable] = {
        "ecommerce": render_shopnest_page,
        "saas": render_velocity_page,
        "banking": render_securebank_page,
        "government": render_gov_page,
        "healthcare": render_healthcare_page,
        "hr": render_hr_page,
        "cloud": render_cloud_page,
        "legal": render_legal_page,
        "travel": render_travel_page,
        "university": render_university_page,
        "crypto": render_crypto_page,
        "realestate": render_realestate_page,
    }
    
    renderer = renderers.get(archetype, render_shopnest_page)
    html = renderer(session_id, selected_traps, page_path, seed, state=state)
    
    # Inject category traps if present
    if selected_categories:
        category_html = ""
        for cat in selected_categories:
            category_html += inject_category_traps(session_id, cat, seed, page_path)
        
        # Inject before </body>
        if "</body>" in html:
            html = html.replace("</body>", f"{category_html}</body>")
        else:
            html += category_html

            
    return html

