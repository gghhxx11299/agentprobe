from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Any, Dict
import json
from datetime import datetime

from database import SessionLocal
from models import SessionState

router = APIRouter()

class StateUpdateRequest(BaseModel):
    key: str
    value: Any

@router.post("/{session_id}/update")
async def update_state(session_id: str, request: StateUpdateRequest):
    db = SessionLocal()
    try:
        existing = db.query(SessionState).filter(
            SessionState.session_id == session_id,
            SessionState.state_key == request.key
        ).first()
        
        json_val = json.dumps(request.value)
        
        if existing:
            existing.state_value = json_val
            existing.updated_at = datetime.utcnow()
        else:
            new_state = SessionState(
                session_id=session_id,
                state_key=request.key,
                state_value=json_val
            )
            db.add(new_state)
        
        db.commit()
        return {"status": "ok"}
    finally:
        db.close()

@router.get("/{session_id}/{key}")
async def get_state(session_id: str, key: str):
    db = SessionLocal()
    try:
        state = db.query(SessionState).filter(
            SessionState.session_id == session_id,
            SessionState.state_key == key
        ).first()
        
        if not state:
            return {"value": None}
            
        return {"value": json.loads(state.state_value)}
    finally:
        db.close()

def get_session_state_internal(session_id: str, key: str, default: Any = None) -> Any:
    """Helper for internal backend use."""
    db = SessionLocal()
    try:
        state = db.query(SessionState).filter(
            SessionState.session_id == session_id,
            SessionState.state_key == key
        ).first()
        return json.loads(state.state_value) if state else default
    finally:
        db.close()
