from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import Response, JSONResponse, HTMLResponse
from datetime import datetime
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from trap_engine import TRAP_INFO, URL_TO_TRAP

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

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

def log_signal(
    session_id: str,
    category: str,
    signal_type: str,
    user_agent: Optional[str] = None,
    confidence: int = 100,
    trigger_source: str = "load",
    time_to_trigger: int = 0,
    event_type: Optional[str] = None
):
    from database import SessionLocal
    from models import AnalyticsLog

    db = SessionLocal()
    try:
        # Check if this signal was already logged for this session/category/type
        existing = db.query(AnalyticsLog).filter(
            AnalyticsLog.session_id == session_id,
            AnalyticsLog.category == category,
            AnalyticsLog.signal_type == signal_type,
            AnalyticsLog.event_type == event_type
        ).first()

        if not existing:
            analytics_log = AnalyticsLog(
                session_id=session_id,
                category=category,
                event_type=event_type,
                signal_type=signal_type,
                triggered_at=datetime.utcnow(),
                user_agent=user_agent,
                confidence=confidence,
                trigger_source=trigger_source,
                time_to_trigger=time_to_trigger
            )
            db.add(analytics_log)
            db.commit()
    finally:
        db.close()


def validate_session(session_id: str) -> bool:
    """Quick validation that session exists without full DB overhead."""
    from database import SessionLocal
    from models import Session as SessionModel
    
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        return session is not None
    finally:
        db.close()


# ── THREE SIGNAL ENDPOINTS ──────────────────────────

@router.get("/t/{session_id}/control")
@limiter.limit("30/minute")
async def signal_control(request: Request, session_id: str, cat: str):
    if not validate_session(session_id):
        return JSONResponse(content={"status": "ok"})  # Silent fail for invalid sessions
    
    user_agent = request.headers.get("user-agent")
    log_signal(session_id, cat, "control", user_agent)
    return JSONResponse(content={"status": "ok"})

@router.get("/t/{session_id}/triggered")
@limiter.limit("30/minute")
async def signal_triggered(request: Request, session_id: str, cat: str, conf: int = 100, src: str = "load", time: int = 0):
    if not validate_session(session_id):
        return JSONResponse(content={"status": "ok"})
    
    user_agent = request.headers.get("user-agent")
    log_signal(session_id, cat, "triggered", user_agent, confidence=conf, trigger_source=src, time_to_trigger=time)
    return JSONResponse(content={"status": "ok"})

@router.get("/t/{session_id}/identified")
@limiter.limit("30/minute")
async def signal_identified(request: Request, session_id: str, cat: str, conf: int = 100):
    if not validate_session(session_id):
        return JSONResponse(content={"status": "ok"})
    
    user_agent = request.headers.get("user-agent")
    log_signal(session_id, cat, "identified", user_agent, confidence=conf)
    return JSONResponse(content={"status": "ok"})


# ── DISGUISED ENDPOINT ───────────────────────

def get_event_name(ref: str, src: str) -> Optional[str]:
    """Map ref+src to event name (formerly trap name)."""
    return URL_TO_TRAP.get((ref, src))

@router.get("/t/{session_id}/evt")
@limiter.limit("60/minute")
async def probe_evt(
    request: Request,
    session_id: str,
    ref: str = Query(...),
    src: str = Query(...),
    confidence: Optional[int] = Query(None),
    trigger: Optional[str] = Query(None),
    time: Optional[int] = Query(None)
):
    if not validate_session(session_id):
        return JSONResponse(content={"status": "ok"})
    
    event_type = get_event_name(ref, src)
    if not event_type:
        return JSONResponse(content={"status": "ok"})

    user_agent = request.headers.get("user-agent")
    conf = confidence if confidence is not None else 100
    trig = trigger if trigger else "load"
    ttf = time if time is not None else 0

    from database import SessionLocal
    from models import AnalyticsLog
    db = SessionLocal()
    try:
        existing = db.query(AnalyticsLog).filter(
            AnalyticsLog.session_id == session_id,
            AnalyticsLog.event_type == event_type
        ).first()
        if not existing:
            info = TRAP_INFO.get(event_type, {"tier": 1, "severity": "medium"})
            analytics_log = AnalyticsLog(
                session_id=session_id,
                event_type=event_type,
                signal_type="triggered",
                tier=info["tier"],
                severity=info["severity"],
                triggered_at=datetime.utcnow(),
                user_agent=user_agent,
                confidence=conf,
                trigger_source=trig,
                time_to_trigger=ttf
            )
            db.add(analytics_log)
            db.commit()
    finally:
        db.close()

    accept_header = request.headers.get("accept", "")
    if "image" in accept_header:
        return Response(content=TRANSPARENT_PNG, media_type="image/png")
    return JSONResponse(content={"status": "ok"})
