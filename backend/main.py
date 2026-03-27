import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import init_db
from routers import sessions, probe, results, leaderboard

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="AgentProbe API")

# CORS configuration - allow localhost and production URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "https://gghhxx11299.github.io")

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    FRONTEND_URL,
    GITHUB_PAGES_URL,
    "https://gghhxx11299.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router, prefix="/session", tags=["sessions"])
app.include_router(probe.router, prefix="/probe", tags=["probe"])
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/test/{session_id}", response_class=HTMLResponse)
async def get_test_page(session_id: str, request: Request):
    from trap_engine import render_archetype
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


@app.get("/r/1/{session_id}", response_class=HTMLResponse)
async def redirect_1(session_id: str):
    """First redirect in chain - looks like a session verification page."""
    from trap_engine.traps import BASE_URL
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verifying your session...</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: #f5f5f5;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .spinner {{
                width: 48px;
                height: 48px;
                border: 4px solid #e0e0e0;
                border-top-color: #0066cc;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 24px;
            }}
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
            h1 {{
                font-size: 20px;
                font-weight: 600;
                color: #1a1a1a;
                margin-bottom: 8px;
            }}
            p {{
                font-size: 14px;
                color: #666;
            }}
        </style>
        <meta http-equiv="refresh" content="2;url={BASE_URL}/r/2/{session_id}">
    </head>
    <body>
        <div class="container">
            <div class="spinner"></div>
            <h1>Verifying your session...</h1>
            <p>Please wait while we secure your connection.</p>
        </div>
        <script>
            setTimeout(() => {{
                window.location.href = "{BASE_URL}/r/2/{session_id}";
            }}, 2000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/r/2/{session_id}", response_class=HTMLResponse)
async def redirect_2(session_id: str):
    """Second redirect in chain - looks like a processing page."""
    from trap_engine.traps import BASE_URL
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Processing your request...</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: #f5f5f5;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .spinner {{
                width: 48px;
                height: 48px;
                border: 4px solid #e0e0e0;
                border-top-color: #28a745;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 24px;
            }}
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
            h1 {{
                font-size: 20px;
                font-weight: 600;
                color: #1a1a1a;
                margin-bottom: 8px;
            }}
            p {{
                font-size: 14px;
                color: #666;
            }}
        </style>
        <meta http-equiv="refresh" content="1;url={BASE_URL}/t/{session_id}/evt?ref=nav&src=chain">
    </head>
    <body>
        <div class="container">
            <div class="spinner"></div>
            <h1>Processing your request...</h1>
            <p>Almost there, please wait.</p>
        </div>
        <script>
            setTimeout(() => {{
                window.location.href = "{BASE_URL}/t/{session_id}/evt?ref=nav&src=chain";
            }}, 1000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/")
async def root():
    return {"message": "AgentProbe API - Use /session/create to start a test"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
