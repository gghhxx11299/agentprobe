from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional
import os
import json
import logging
from datetime import datetime

# Import V2-specific database/models
from database import SessionLocal
from models import Session as SessionModel, AnalyticsLog

router = APIRouter(prefix="/v2", tags=["v2"])

# V2 ARCHETYPE MAP
ARCHETYPE_MAP = {
    "shop": "ecommerce",
    "crm": "saas",
    "bank": "banking",
    "gov": "government"
}

@router.get("/test/{session_id}/{archetype}/{path:path}")
@router.get("/test/{session_id}/{archetype}")
async def get_test_page_v2(session_id: str, archetype: str, request: Request, path: str = "/"):
    """Serve legacy V2 test pages with support for deep paths and state rehydration."""
    from trap_engine.multiframe import render_multiframe_page
    from database import SessionLocal
    from models import Session as SessionModel, SessionState
    
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            return HTMLResponse("<h1>V2 Session Not Found</h1>", status_code=404)

        # v3: Rehydrate State
        state_entries = db.query(SessionState).filter(SessionState.session_id == session_id).all()
        rehydrated_state = {}
        for entry in state_entries:
            try:
                rehydrated_state[entry.state_key] = json.loads(entry.state_value)
            except:
                rehydrated_state[entry.state_key] = entry.state_value

        selected_traps = json.loads(session.selected_traps or "[]")
        selected_categories = json.loads(session.selected_categories or "[]")
        
        # Ensure path starts with /
        if not path.startswith("/"):
            path = "/" + path
            
        # Determine base URL from request
        base_url = str(request.base_url).rstrip("/")
        
        # Render using the engine
        html_content = render_multiframe_page(
            ARCHETYPE_MAP.get(archetype, archetype), 
            session_id, 
            selected_traps, 
            path, 
            session.seed, 
            selected_categories,
            state=rehydrated_state,
            base_url=base_url
        )
        return HTMLResponse(content=html_content)
    finally:
        db.close()
