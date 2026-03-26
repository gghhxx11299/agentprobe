import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import init_db
from routers import sessions, probe, results

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="AgentProbe API")

# CORS configuration - allow localhost and production URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    FRONTEND_URL,
]

# Add GitHub Pages URL if set
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL")
if GITHUB_PAGES_URL:
    ALLOWED_ORIGINS.append(GITHUB_PAGES_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router, prefix="/session", tags=["sessions"])
app.include_router(probe.router, prefix="/probe", tags=["probe"])
app.include_router(results.router, prefix="/results", tags=["results"])


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/test/{session_id}", response_class=HTMLResponse)
async def get_test_page(session_id: str, request: Request):
    from trap_engine.traps import render_archetype
    from database import SessionLocal
    from models import Session as SessionModel
    import json

    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            return HTMLResponse("<h1>Session not found</h1>", status_code=404)

        selected_traps = json.loads(session.selected_traps)
        html_content = render_archetype(session.archetype, session_id, selected_traps)
        return HTMLResponse(content=html_content)
    finally:
        db.close()


@app.get("/redirect-1/{session_id}", response_class=HTMLResponse)
async def redirect_1(session_id: str):
    from trap_engine.traps import BASE_URL
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url={BASE_URL}/redirect-2/{session_id}">
        <script>window.location.href = "{BASE_URL}/redirect-2/{session_id}";</script>
    </head>
    <body>Redirecting...</body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/redirect-2/{session_id}", response_class=HTMLResponse)
async def redirect_2(session_id: str):
    from trap_engine.traps import BASE_URL
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url={BASE_URL}/probe/{session_id}/redirect_chain">
        <script>window.location.href = "{BASE_URL}/probe/{session_id}/redirect_chain";</script>
    </head>
    <body>Redirecting...</body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/")
async def root():
    return {"message": "AgentProbe API - Use /session/create to start a test"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
