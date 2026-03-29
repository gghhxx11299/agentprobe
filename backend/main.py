from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os

# Import V2 and V3 Routers
from routers import v2, v3, sessions, probe, results, leaderboard, debug, state
from database import init_db

# Fix: Disable trailing slash redirection which breaks CORS preflights
app = FastAPI(
    title="AgentProbe API - Multi-Version Entry Point",
    redirect_slashes=False
)

# Explicit CORS: Correct list of origins
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

@app.on_event("startup")
def startup_event():
    init_db()

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

# BACKWARDS COMPATIBILITY FOR RENDER
@app.get("/test/{session_id}/{archetype}")
async def legacy_redirect(session_id: str, archetype: str):
    return RedirectResponse(url=f"/v2/test/{session_id}/{archetype}")

@app.get("/")
def read_root():
    return RedirectResponse(url="https://gghhxx11299.github.io")
