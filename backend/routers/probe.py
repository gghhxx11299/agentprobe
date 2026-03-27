from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import Response, JSONResponse, HTMLResponse
from datetime import datetime
from typing import Optional

from trap_engine.traps import TRAP_INFO, URL_TO_TRAP

router = APIRouter()

# 1x1 transparent PNG
TRANSPARENT_PNG = bytes([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
    0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
    0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
    0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
    0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
    0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
    0x42, 0x60, 0x82
])

# URL_TO_TRAP is imported from trap_engine.traps


def get_trap_name(ref: str, src: str) -> Optional[str]:
    """Map ref+src to trap name."""
    return URL_TO_TRAP.get((ref, src))


def log_trap(
    session_id: str, 
    trap_type: str, 
    user_agent: Optional[str] = None,
    confidence: int = 100,
    trigger_type: str = "load",
    time_to_trigger: int = 0
):
    from database import SessionLocal
    from models import TrapLog

    info = TRAP_INFO.get(trap_type, {"tier": 1, "severity": "medium"})

    db = SessionLocal()
    try:
        # Check if this trap was already logged for this session
        existing = db.query(TrapLog).filter(
            TrapLog.session_id == session_id,
            TrapLog.trap_type == trap_type
        ).first()
        
        if existing:
            # Update count only, don't duplicate
            existing.count = getattr(existing, 'count', 1) + 1
            db.commit()
        else:
            trap_log = TrapLog(
                session_id=session_id,
                trap_type=trap_type,
                tier=info["tier"],
                severity=info["severity"],
                triggered_at=datetime.utcnow(),
                user_agent=user_agent,
                confidence=confidence,
                trigger_type=trigger_type,
                time_to_trigger=time_to_trigger
            )
            db.add(trap_log)
            db.commit()
    finally:
        db.close()


# ── NEW DISGUISED ENDPOINT ──────────────────────────

@router.get("/t/{session_id}/evt")
async def probe_evt(
    session_id: str,
    request: Request,
    ref: str = Query(...),
    src: str = Query(...),
    confidence: Optional[int] = Query(None),
    trigger: Optional[str] = Query(None),
    time: Optional[int] = Query(None)
):
    """Disguised analytics endpoint - maps ref+src to trap name."""
    trap_type = get_trap_name(ref, src)
    if not trap_type:
        return JSONResponse(content={"status": "ok"}, status_code=200)

    user_agent = request.headers.get("user-agent")
    
    # Use provided values or defaults
    conf = confidence if confidence is not None else 100
    trig = trigger if trigger else "load"
    ttf = time if time is not None else 0
    
    log_trap(session_id, trap_type, user_agent, conf, trig, ttf)

    # Return transparent PNG for image requests
    accept_header = request.headers.get("accept", "")
    if "image" in accept_header:
        return Response(content=TRANSPARENT_PNG, media_type="image/png")

    # Return JSON for fetch requests
    return JSONResponse(content={"status": "ok"})


@router.post("/t/{session_id}/evt")
async def probe_evt_post(
    session_id: str,
    request: Request,
    ref: str = Query(...),
    src: str = Query(...),
    confidence: Optional[int] = Query(None),
    trigger: Optional[str] = Query(None),
    time: Optional[int] = Query(None)
):
    """Disguised analytics endpoint (POST)."""
    trap_type = get_trap_name(ref, src)
    if not trap_type:
        return JSONResponse(content={"status": "ok"}, status_code=200)

    user_agent = request.headers.get("user-agent")
    
    conf = confidence if confidence is not None else 100
    trig = trigger if trigger else "interaction"
    ttf = time if time is not None else 0
    
    log_trap(session_id, trap_type, user_agent, conf, trig, ttf)
    return JSONResponse(content={"status": "ok"})


# ── LEGACY ENDPOINTS (kept for backward compatibility) ──────────────────────────

@router.get("/{session_id}/{trap_type}")
async def probe_trap(session_id: str, trap_type: str, request: Request):
    user_agent = request.headers.get("user-agent")
    log_trap(session_id, trap_type, user_agent)

    accept_header = request.headers.get("accept", "")
    if "image" in accept_header or trap_type == "ping":
        return Response(content=TRANSPARENT_PNG, media_type="image/png")

    return JSONResponse(content={"status": "ok"})


@router.post("/{session_id}/{trap_type}")
async def probe_trap_post(session_id: str, trap_type: str, request: Request):
    user_agent = request.headers.get("user-agent")
    log_trap(session_id, trap_type, user_agent)
    return JSONResponse(content={"status": "ok"})
