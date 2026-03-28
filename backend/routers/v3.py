from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
import os

from database import SessionLocal
from models import SessionV3, SignalV3
from engine.templates import render_page, TRAP_REGISTRY
from engine.scoring import ScoringEngineV3

router = APIRouter(prefix="/v3", tags=["v3"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SignalCreate(BaseModel):
    session_id: str
    version: int
    trap_id: str
    signal_type: str = "triggered"
    path: str
    reasoning: Optional[str] = None

class StateUpdate(BaseModel):
    session_id: str
    expected_version: int
    new_state: Dict

@router.get("/test/{session_id}/{archetype}")
async def get_test_page_v3(session_id: str, archetype: str, request: Request, db: Session = Depends(get_db)):
    session = db.query(SessionV3).filter(SessionV3.id == session_id).first()
    if not session:
        session = SessionV3(id=session_id, archetype=archetype)
        db.add(session)
        db.commit()

    context = {
        "session_id": session_id,
        "version": session.version,
        "base_url": os.getenv("BASE_URL", "http://localhost:8000"),
        "archetype": archetype,
        "contacts": [{"name": "Sarah Jenkins", "company": "Tech Corp", "email": "s@j.com"}],
        "products": [{"name": "V3 Pro Headphones", "price": 299.99}]
    }

    # Shadow DOM load signal
    db.add(SignalV3(session_id=session_id, trap_id="page_load", category="baseline", signal_type="control"))
    db.commit()

    template = f"archetypes/{archetype}_v3.html"
    html = render_page(template, context)
    return HTMLResponse(content=html)

# ── TRANSACTIONAL STATE (Optimistic Locking) ──────────

@router.post("/session/state")
async def update_state_v3(update: StateUpdate, db: Session = Depends(get_db)):
    """Fixed: Implemented Optimistic Locking for state updates."""
    session = db.query(SessionV3).filter(SessionV3.id == update.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if update.expected_version != session.version:
        raise HTTPException(status_code=409, detail="State conflict (version mismatch)")

    session.state = update.new_state
    session.version += 1
    db.commit()
    return {"status": "ok", "new_version": session.version}

# ── HARMONIZED TRAP ENDPOINTS ─────────────────────────

@router.get("/probe/nojs/{session_id}/{trap_slug}")
async def nojs_honeypot(session_id: str, trap_slug: str, db: Session = Depends(get_db)):
    signal = SignalV3(session_id=session_id, trap_id=f"nojs_{trap_slug}", category="action_boundary", signal_type="triggered")
    db.add(signal)
    db.commit()
    return JSONResponse({"status": "DETECTED", "type": f"NOJS_{trap_slug.upper()}"})

@router.get("/probe/shadow/{session_id}/{trap_slug}")
async def shadow_triggered(session_id: str, trap_slug: str, db: Session = Depends(get_db)):
    signal = SignalV3(session_id=session_id, trap_id=f"shadow_{trap_slug}", category="multimodal_consistency", signal_type="triggered")
    db.add(signal)
    db.commit()
    return JSONResponse({"status": "DETECTED", "type": f"SHADOW_{trap_slug.upper()}"})

@router.post("/probe/signal")
async def log_signal_v3(signal: SignalCreate, request: Request, db: Session = Depends(get_db)):
    session = db.query(SessionV3).filter(SessionV3.id == signal.session_id).first()
    if not session:
        raise HTTPException(status_code=404)
        
    signal_type = "stale_interaction" if signal.version < session.version else signal.signal_type
    
    db.add(SignalV3(
        session_id=signal.session_id,
        trap_id=signal.trap_id,
        category=TRAP_REGISTRY.get(signal.trap_id, {}).get("category", "unknown"),
        signal_type=signal_type,
        path=signal.path,
        reasoning=signal.reasoning,
        user_agent=request.headers.get("user-agent", "unknown")
    ))
    db.commit()
    return {"status": "ok"}

@router.get("/results/{session_id}")
async def get_results_v3(session_id: str, db: Session = Depends(get_db)):
    return ScoringEngineV3.calculate_vulnerability(db, session_id)
