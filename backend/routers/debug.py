from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Session as SessionModel, TrapLog
import json

router = APIRouter()

@router.get("/{session_id}/verify")
async def verify_session(session_id: str):
    """Debug endpoint to verify session existence and trap logs."""
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        logs = db.query(TrapLog).filter(TrapLog.session_id == session_id).all()
        
        return {
            "status": "valid",
            "session": {
                "id": session.id,
                "archetype": session.archetype,
                "mode": session.mode,
                "difficulty": session.difficulty,
                "seed": session.seed,
                "selected_traps": json.loads(session.selected_traps),
                "created_at": session.created_at.isoformat()
            },
            "logs_count": len(logs),
            "triggered_traps": [log.trap_type for log in logs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
