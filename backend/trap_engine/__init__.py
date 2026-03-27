from .traps import ALL_TRAPS, inject_traps, BASE_URL, URL_TO_TRAP, get_trap_url, LOAD_TRAPS, TRAP_INFO, TRAP_TRIGGER_TYPES

__all__ = ["ALL_TRAPS", "inject_traps", "BASE_URL", "URL_TO_TRAP", "get_trap_url", "LOAD_TRAPS", "TRAP_INFO", "TRAP_TRIGGER_TYPES", "render_archetype"]


def render_archetype(archetype: str, session_id: str, selected_traps: list) -> str:
    """Render an archetype page with traps injected."""
    from .archetypes.ecommerce import render_ecommerce
    from .archetypes.saas import render_saas
    from .archetypes.banking import render_banking
    from .archetypes.government import render_government

    archetypes = {
        "ecommerce": render_ecommerce,
        "saas": render_saas,
        "banking": render_banking,
        "government": render_government,
    }

    renderer = archetypes.get(archetype, render_ecommerce)
    return renderer(session_id, selected_traps)
