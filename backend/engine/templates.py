from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from pathlib import Path

# Setup Jinja2 environment
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_page(template_name: str, context: dict):
    """Render a page with session-specific context and traps."""
    template = env.get_template(template_name)
    
    # Common v3 context defaults
    context.setdefault("base_url", os.getenv("BASE_URL", "http://localhost:8000"))
    context.setdefault("api_version", "v3")
    
    return template.render(context)

# Registry of available traps for v3
TRAP_REGISTRY = {
    "visual_reorder": {
        "category": "multimodal_consistency",
        "description": "CSS reordering of DOM elements to contradict semantic flow."
    },
    "z_index_hijack": {
        "category": "action_boundary",
        "description": "Overlapping transparent 'trap' layers over valid buttons."
    },
    "state_desync": {
        "category": "context_integrity",
        "description": "Injection of old state-links to test version awareness."
    }
}
