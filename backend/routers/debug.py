from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Session as SessionModel, AnalyticsLog
import json

router = APIRouter()

@router.get("/{session_id}/verify")
async def verify_session(session_id: str):
    """Debug endpoint to verify session existence and analytics logs."""
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        logs = db.query(AnalyticsLog).filter(AnalyticsLog.session_id == session_id).all()
        
        return {
            "status": "valid",
            "session": {
                "id": session.id,
                "archetype": session.archetype,
                "mode": session.mode,
                "difficulty": session.difficulty,
                "seed": session.seed,
                "selected_categories": json.loads(session.selected_categories or "[]"),
                "selected_traps": json.loads(session.selected_traps or "[]"),
                "created_at": session.created_at.isoformat()
            },
            "logs_count": len(logs),
            "events": [
                {
                    "type": log.event_type or log.category,
                    "signal": log.signal_type,
                    "confidence": log.confidence,
                    "triggered_at": log.triggered_at.isoformat()
                }
                for log in logs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
