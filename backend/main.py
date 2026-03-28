import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from database import init_db
from routers import sessions, probe, results, leaderboard, debug, state

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="AgentProbe API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error", "detail": str(exc)},
    )

# CORS configuration - allow localhost and production URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "https://gghhxx11299.github.io")

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://gghhxx11299.github.io",
    FRONTEND_URL,
    GITHUB_PAGES_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Custom middleware to allow GitHub Pages subdomains dynamically
@app.middleware("http")
async def allow_github_pages(request, call_next):
    origin = request.headers.get("origin", "")
    if origin.endswith(".github.io"):
        request.scope["headers"].append((b"origin", origin.encode()))
    response = await call_next(request)
    if origin.endswith(".github.io"):
        response.headers["Access-Control-Allow-Origin"] = origin
    return response

# Session Cookie Middleware
@app.middleware("http")
async def session_cookie_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # If path is a test page, set the session cookie
    if request.url.path.startswith("/test/"):
        parts = request.url.path.split("/")
        if len(parts) >= 3:
            session_id = parts[2]
            response.set_cookie(
                key="ap_session_id",
                value=session_id,
                httponly=True,
                max_age=3600,
                samesite="lax"
            )
    return response


# Include routers
app.include_router(sessions.router, prefix="/session", tags=["sessions"])
app.include_router(probe.router, prefix="/probe", tags=["probe"])
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])
app.include_router(state.router, prefix="/state", tags=["state"])

@app.get("/t/{session_id}/state")
async def update_session_state_simple(session_id: str, key: str, val: str):
    """Simple GET-based state update for archetype interaction."""
    from routers.state import update_state, StateUpdateRequest
    await update_state(session_id, StateUpdateRequest(key=key, value=val))
    return JSONResponse(content={"status": "ok"})

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/test/{session_id}/{archetype:path}")
async def get_test_page(session_id: str, request: Request, archetype: str = "shop"):
    """Serve multi-page archetype test pages with state persistence and signal logging."""
    from trap_engine.multiframe import render_multiframe_page
    from trap_engine import ALL_TRAPS, LOAD_TRAPS, URL_TO_TRAP, TRAP_INFO
    from database import SessionLocal
    from models import Session as SessionModel, AnalyticsLog
    from routers.state import get_session_state_internal
    import json
    import logging
    from datetime import datetime
    from urllib.parse import unquote

    logger = logging.getLogger("agentprobe")
    
    # Decode archetype path
    archetype = unquote(archetype)
    
    # Parse archetype and page path
    parts = archetype.split("/", 1)
    archetype_name = parts[0]
    page_path = "/" + parts[1] if len(parts) > 1 else "/"
    
    # Map archetype names
    archetype_map = {
        "shop": "ecommerce",
        "crm": "saas",
        "bank": "banking",
        "gov": "government",
        "health": "healthcare",
        "hr": "hr",
        "cloud": "cloud",
        "legal": "legal",
        "travel": "travel",
        "uni": "university",
        "crypto": "crypto",
        "realestate": "realestate",
    }
    db_archetype = archetype_map.get(archetype_name, archetype_name)

    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            return HTMLResponse("<h1>Session not found</h1>", status_code=404)

        selected_traps = json.loads(session.selected_traps)
        selected_categories = json.loads(session.selected_categories) if session.selected_categories else []
        
        # Fetch current state for persistence
        cart_data = get_session_state_internal(session_id, "cart", [])
        form_data = get_session_state_internal(session_id, "form", {})
        
        # Render the page with traps and state
        html_content = render_multiframe_page(
            db_archetype, 
            session_id, 
            selected_traps, 
            page_path, 
            session.seed, 
            selected_categories,
            state={"cart": cart_data, "form": form_data}
        )

        # SERVER-SIDE SIGNAL FIRING: Auto-fire load triggers
        user_agent = request.headers.get("user-agent", "unknown")
        events_to_fire = []
        for trap_name in selected_traps:
            if trap_name in LOAD_TRAPS:
                existing = db.query(AnalyticsLog).filter(
                    AnalyticsLog.session_id == session_id,
                    AnalyticsLog.event_type == trap_name
                ).first()
                if not existing:
                    info = TRAP_INFO.get(trap_name, {"tier": 1, "severity": "medium"})
                    log = AnalyticsLog(
                        session_id=session_id,
                        event_type=trap_name,
                        signal_type="triggered",
                        tier=info["tier"],
                        severity=info["severity"],
                        triggered_at=datetime.utcnow(),
                        user_agent=user_agent,
                        confidence=100,
                        trigger_source="load"
                    )
                    db.add(log)
                    events_to_fire.append(trap_name)
        
        # ALSO FIRE CONTROL SIGNALS FOR METHODOLOGY CATEGORIES
        for cat in selected_categories:
            # Fire control signal for baseline categories on page load
            if cat in ["trust_hierarchy", "uncertainty_decision", "persistence", "action_boundary", "multimodal_consistency"]:
                existing_control = db.query(AnalyticsLog).filter(
                    AnalyticsLog.session_id == session_id,
                    AnalyticsLog.category == cat,
                    AnalyticsLog.signal_type == "control"
                ).first()
                if not existing_control:
                    log = AnalyticsLog(
                        session_id=session_id,
                        category=cat,
                        signal_type="control",
                        triggered_at=datetime.utcnow(),
                        user_agent=user_agent,
                        confidence=100,
                        trigger_source="load"
                    )
                    db.add(log)
            
            # PERSISTENCE TRACKING: Track page progression for persistence category
            if cat == "persistence":
                # Calculate page depth for persistence tracking
                page_depth = len(page_path.strip("/").split("/")) if page_path and page_path != "/" else 1
                
                # Log page view for persistence tracking
                existing_page_log = db.query(AnalyticsLog).filter(
                    AnalyticsLog.session_id == session_id,
                    AnalyticsLog.category == "persistence",
                    AnalyticsLog.event_type == f"page_{page_depth}_viewed"
                ).first()
                
                if not existing_page_log:
                    log = AnalyticsLog(
                        session_id=session_id,
                        category="persistence",
                        signal_type="control",
                        event_type=f"page_{page_depth}_viewed",
                        triggered_at=datetime.utcnow(),
                        user_agent=user_agent,
                        confidence=100,
                        trigger_source="navigation",
                        time_to_trigger=page_depth * 5  # Estimate 5s per page
                    )
                    db.add(log)

        db.commit()

        # Debug log
        logger.info(f"SESSION {session_id} | PAGE {archetype} | EVENTS INJECTED: {selected_traps}")
        
        response = HTMLResponse(content=html_content)
        response.headers["X-Events-Injected"] = ",".join(selected_traps)
        response.headers["X-Session-ID"] = session_id
        return response
        
    except Exception as e:
        logger.error(f"Error serving test page: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
