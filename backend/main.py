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

# Include routers
app.include_router(sessions.router, prefix="/session", tags=["sessions"])
app.include_router(probe.router, prefix="/probe", tags=["probe"])
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/test/{session_id}/{archetype:path}")
async def get_test_page(session_id: str, request: Request, archetype: str = "shop"):
    """Serve multi-page archetype test pages with trap injection logging."""
    from trap_engine.multiframe import render_multiframe_page
    from trap_engine.traps import ALL_TRAPS, LOAD_TRAPS, URL_TO_TRAP, TRAP_INFO
    from database import SessionLocal
    from models import Session as SessionModel, TrapLog
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
        
        # Render the page with traps
        html_content = render_multiframe_page(db_archetype, session_id, selected_traps, page_path)

        # SERVER-SIDE TRAP FIRING: Auto-fire load traps when page is served
        user_agent = request.headers.get("user-agent", "unknown")
        traps_to_fire = []
        for trap_name in selected_traps:
            if trap_name in LOAD_TRAPS:
                for (ref, src), name in URL_TO_TRAP.items():
                    if name == trap_name:
                        existing = db.query(TrapLog).filter(
                            TrapLog.session_id == session_id,
                            TrapLog.trap_type == trap_name
                        ).first()
                        if not existing:
                            info = TRAP_INFO.get(trap_name, {"tier": 1, "severity": "medium"})
                            trap_log = TrapLog(
                                session_id=session_id,
                                trap_type=trap_name,
                                tier=info["tier"],
                                severity=info["severity"],
                                triggered_at=datetime.utcnow(),
                                user_agent=user_agent,
                                confidence=100,
                                trigger_type="load",
                                time_to_trigger=0
                            )
                            db.add(trap_log)
                            traps_to_fire.append(trap_name)
                        break

        db.commit()

        # Debug log
        logger.info(f"SESSION {session_id} | PAGE {archetype} | TRAPS INJECTED: {selected_traps}")
        if traps_to_fire:
            logger.info(f"  Auto-fired load traps: {traps_to_fire}")

        # Verify probe URLs in HTML
        probe_urls_found = "/t/" in html_content or "/probe/" in html_content
        if not probe_urls_found:
            logger.error(f"  ⚠️ WARNING: No probe URLs found in HTML for session {session_id}")

        response = HTMLResponse(content=html_content)
        response.headers["X-Traps-Injected"] = ",".join(selected_traps)
        response.headers["X-Session-ID"] = session_id
        return response
        
    except Exception as e:
        logger.error(f"Error serving test page: {e}")
        db.rollback()
        raise
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


@app.get("/debug/{session_id}/verify")
async def debug_verify(session_id: str):
    """Debug endpoint to verify trap injection across all pages served."""
    import os
    from database import SessionLocal
    from models import Session as SessionModel, TrapLog
    import json
    
    # Only allow in development
    if os.getenv("ENV") != "development" and os.getenv("DEBUG") != "true":
        raise HTTPException(status_code=403, detail="Debug endpoint only available in development")
    
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        selected_traps = json.loads(session.selected_traps)
        logs = db.query(TrapLog).filter(TrapLog.session_id == session_id).all()
        
        # Group logs by page (we'd need to track this separately)
        traps_triggered = list(set(log.trap_type for log in logs))
        
        return {
            "session_id": session_id,
            "archetype": session.archetype,
            "mode": session.mode,
            "pages_served": len(logs),  # Approximate
            "traps_selected": selected_traps,
            "traps_triggered": traps_triggered,
            "trigger_count": len(logs),
            "all_traps_fired": len(traps_triggered) == len(selected_traps),
            "ping_fired": "ping" in traps_triggered,
        }
    finally:
        db.close()


@app.get("/debug/{session_id}/traps")
async def debug_traps(session_id: str):
    """Debug endpoint to verify trap injection (development only)."""
    import os
    from database import SessionLocal
    from models import Session as SessionModel
    from trap_engine.traps import ALL_TRAPS, inject_traps
    import json
    
    # Only allow in development
    if os.getenv("ENV") != "development" and os.getenv("DEBUG") != "true":
        raise HTTPException(status_code=403, detail="Debug endpoint only available in development")
    
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        selected_traps = json.loads(session.selected_traps)
        injected_html = inject_traps(session_id, selected_traps)
        
        trap_details = []
        for trap_name in selected_traps:
            if trap_name in ALL_TRAPS:
                trap_html = ALL_TRAPS[trap_name](session_id)
                probe_urls = []
                import re
                urls = re.findall(r'https?://[^\s"\'<>]+', trap_html)
                for url in urls:
                    if '/t/' in url or '/probe/' in url:
                        probe_urls.append(url)
                
                trap_details.append({
                    "name": trap_name,
                    "injected": trap_html in injected_html,
                    "html_preview": trap_html[:100].replace("\n", " ").strip(),
                    "probe_urls": probe_urls,
                    "urls_in_final_html": all(url in injected_html for url in probe_urls)
                })
            else:
                trap_details.append({
                    "name": trap_name,
                    "injected": False,
                    "reason": "Unknown trap type"
                })
        
        return {
            "session_id": session_id,
            "archetype": session.archetype,
            "selected_traps": selected_traps,
            "trap_count": len(selected_traps),
            "traps": trap_details,
            "all_injected": all(t.get("injected", False) for t in trap_details),
            "all_urls_present": all(t.get("urls_in_final_html", False) for t in trap_details if t.get("injected"))
        }
    finally:
        db.close()


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
