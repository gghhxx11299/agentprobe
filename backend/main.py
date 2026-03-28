from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os

# Import V2 and V3 Routers
from routers import v2, v3, sessions, probe, results, leaderboard, debug, state

app = FastAPI(title="AgentProbe API - Multi-Version Entry Point")

# Unified CORS for all versions
ALLOWED_ORIGINS = ["*", "https://gghhxx11299.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# HEALTH CHECK (Required by Render)
@app.get("/health")
def health():
    return {"status": "all_systems_go", "v2": "active", "v3": "active"}

# BACKWARDS COMPATIBILITY FOR RENDER
@app.get("/test/{session_id}/{archetype}")
async def legacy_redirect(session_id: str, archetype: str):
    return RedirectResponse(url=f"/v2/test/{session_id}/{archetype}")

# Root redirection to dashboard
@app.get("/")
def read_root():
    return RedirectResponse(url="https://gghhxx11299.github.io")
