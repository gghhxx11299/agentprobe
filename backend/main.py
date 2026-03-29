from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
import os
from sqlalchemy.orm import Session

# Import Routers
from routers import v2, v3, sessions, probe, results, leaderboard, debug, state
from database import init_db, SessionLocal
from models import Session as SessionModel

# Fix: Disable trailing slash redirection which breaks CORS preflights
app = FastAPI(
    title="AgentProbe API - Multi-Version Entry Point",
    redirect_slashes=False
)

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
app.include_router(v2.router)
app.include_router(v3.router)

@app.get("/health")
def health():
    return {"status": "all_systems_go", "v2": "active", "v3": "active"}

# FIX: Correct redirect for single-parameter test URLs
@app.get("/test/{session_id}")
async def session_redirect(session_id: str, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        return HTMLResponse("<h1>Session Not Found</h1>", status_code=404)
    # Redirect to the v2 test page which handles the old engine
    return RedirectResponse(url=f"/v2/test/{session_id}/{session.archetype}")

@app.get("/test/{session_id}/{archetype}")
async def legacy_redirect(session_id: str, archetype: str):
    return RedirectResponse(url=f"/v2/test/{session_id}/{archetype}")

@app.get("/")
def read_root():
    return RedirectResponse(url="https://gghhxx11299.github.io")
