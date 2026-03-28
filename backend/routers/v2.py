from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional
import os
import json
import logging
from datetime import datetime

# Import V2-specific database/models if separate, otherwise use root
from database import SessionLocal
from models import Session as SessionModel, AnalyticsLog

router = APIRouter(prefix="/v2", tags=["v2"])

# V2 ARCHETYPE MAP (ShopNest, Velocity, etc.)
ARCHETYPE_MAP = {
    "shop": "ecommerce",
    "crm": "saas",
    "bank": "banking",
    "gov": "government"
}

@router.get("/test/{session_id}/{archetype}")
async def get_test_page_v2(session_id: str, archetype: str, request: Request):
    """Serve legacy V2 test pages."""
    # This will use the OLD v2 trap engine and old logic
    from trap_engine.multiframe import render_multiframe_page
    from trap_engine import ALL_TRAPS, LOAD_TRAPS, TRAP_INFO
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            return HTMLResponse("<h1>V2 Session Not Found</h1>", status_code=404)

        selected_traps = json.loads(session.selected_traps or "[]")
        
        # Render using the OLD engine
        html_content = render_multiframe_page(
            ARCHETYPE_MAP.get(archetype, archetype), 
            session_id, 
            selected_traps, 
            "/", 
            session.seed, 
            []
        )
        return HTMLResponse(content=html_content)
    finally:
        db.close()

# Include other V2 routes as needed
