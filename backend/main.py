from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os

# Import V2 and V3 Routers
from routers import v2, v3 

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

# Include Routers
app.include_router(v2.router)
app.include_router(v3.router)

# HEALTH CHECK (Required by Render)
@app.get("/health")
def health():
    return {"status": "all_systems_go", "v2": "active", "v3": "active"}

# BACKWARDS COMPATIBILITY FOR RENDER
# Redirect the OLD root test URLs to the new versioned path
@app.get("/test/{session_id}/{archetype}")
async def legacy_redirect(session_id: str, archetype: str):
    return RedirectResponse(url=f"/v2/test/{session_id}/{archetype}")

# Root redirection to dashboard if hit directly
@app.get("/")
def read_root():
    return RedirectResponse(url="https://gghhxx11299.github.io")
