from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
import os
from sqlalchemy.orm import Session

# Import Routers
from routers import v2, v3, sessions, probe, results, leaderboard, debug, state
from database import init_db, SessionLocal
from models import Session as SessionModel

# Fix: Enable trailing slash redirection
app = FastAPI(
    title="AgentProbe API - Multi-Version Entry Point",
    redirect_slashes=True
)

# v3: Middleware to handle Render/Proxy HTTPS headers
@app.middleware("http")
async def secure_proxy_middleware(request: Request, call_next):
    # If Render is passing X-Forwarded-Proto as https, ensure the request reflects that
    if request.headers.get("x-forwarded-proto") == "https":
        # This is a bit of a hack for FastAPI's immutable request scope
        # but it works for generating correct base_urls in routers
        request.scope["scheme"] = "https"
    response = await call_next(request)
    return response

@app.on_event("startup")
def startup_event():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Explicit CORS
ALLOWED_ORIGINS = [
    "https://gghhxx11299.github.io",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ── LEGACY V2 ROUTERS (Root Prefix) ──────────────────
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(sessions.router, prefix="/session", tags=["sessions"])
app.include_router(probe.router, prefix="/probe", tags=["probe"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])
app.include_router(state.router, prefix="/state", tags=["state"])

# ── VERSIONED ROUTERS ───────────────────────────────
app.include_router(v2.router) # /v2/test/...
app.include_router(v3.router) # /v3/test/...

@app.get("/health")
def health():
    return {"status": "all_systems_go", "v2": "active", "v3": "active"}

# ARCHETYPE SLUGS (both short and long versions to avoid double slugs)
ARCHETYPE_SLUGS = [
    "shop", "crm", "bank", "gov", "health", "hr", "cloud", "legal", "travel", "univ", "crypto", "real",
    "ecommerce", "saas", "banking", "government", "healthcare", "university", "realestate"
]

# FIX: Correct redirect for single-parameter test URLs with deep paths and slug stripping
@app.get("/test/{session_id}/{path:path}")
@app.get("/test/{session_id}")
async def session_redirect(session_id: str, request: Request, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        return HTMLResponse("<h1>Session Not Found</h1>", status_code=404)
    
    # Get the sub-path if it exists
    full_path = request.url.path
    # Remove the base /test/{id} part
    sub_path = full_path.replace(f"/test/{session_id}", "", 1)
    
    # If sub_path starts with an archetype slug, strip it
    # e.g. /test/{id}/gov/apply -> /apply
    for slug in ARCHETYPE_SLUGS:
        if sub_path.startswith(f"/{slug}"):
            sub_path = sub_path.replace(f"/{slug}", "", 1)
            break
            
    # Normalize sub_path to not have trailing slash if it's the root
    if not sub_path or sub_path == "/":
        sub_path = ""
    elif not sub_path.startswith("/"):
        sub_path = "/" + sub_path
        
    return RedirectResponse(url=f"/v2/test/{session_id}/{session.archetype}{sub_path}")

@app.get("/")
def read_root():
    return RedirectResponse(url="https://gghhxx11299.github.io")
