from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import json
from datetime import datetime
import time

from database import SessionLocal
from models import SessionState

router = APIRouter()


class StateHistoryEntry(BaseModel):
    """Represents a single state change entry."""
    timestamp: float
    delta: Dict[str, Any]
    previous_value: Any
    new_value: Any


class StateUpdateRequest(BaseModel):
    key: str
    value: Any
    delta: Optional[Dict[str, Any]] = None  # What changed


class StateHistoryResponse(BaseModel):
    key: str
    current_value: Any
    history: List[StateHistoryEntry]
    version: int


# In-memory history store (could be moved to DB for production)
_state_history: Dict[str, List[dict]] = {}
_state_versions: Dict[str, int] = {}


def _get_history_key(session_id: str, state_key: str) -> str:
    return f"{session_id}:{state_key}"


@router.post("/{session_id}/update")
async def update_state(session_id: str, request: StateUpdateRequest):
    """Update state with history tracking."""
    db = SessionLocal()
    try:
        existing = db.query(SessionState).filter(
            SessionState.session_id == session_id,
            SessionState.state_key == request.key
        ).first()

        json_val = json.dumps(request.value)
        history_key = _get_history_key(session_id, request.key)
        
        # Get previous value for history
        previous_value = None
        if existing:
            try:
                previous_value = json.loads(existing.state_value)
            except:
                previous_value = None
        
        # Track history
        if history_key not in _state_history:
            _state_history[history_key] = []
        
        if history_key not in _state_versions:
            _state_versions[history_key] = 0
        
        _state_versions[history_key] += 1
        
        # Record history entry
        history_entry = {
            "timestamp": time.time(),
            "delta": request.delta or {"full_update": True},
            "previous_value": previous_value,
            "new_value": request.value,
            "version": _state_versions[history_key]
        }
        _state_history[history_key].append(history_entry)
        
        # Keep only last 50 entries per state key
        if len(_state_history[history_key]) > 50:
            _state_history[history_key] = _state_history[history_key][-50:]

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
        return {"status": "ok", "version": _state_versions[history_key]}
    finally:
        db.close()


@router.get("/{session_id}/{key}")
async def get_state(session_id: str, key: str):
    """Get current state value."""
    db = SessionLocal()
    try:
        state = db.query(SessionState).filter(
            SessionState.session_id == session_id,
            SessionState.state_key == key
        ).first()

        if not state:
            return {"value": None, "version": 0}

        history_key = _get_history_key(session_id, key)
        version = _state_versions.get(history_key, 0)

        return {"value": json.loads(state.state_value), "version": version}
    finally:
        db.close()


@router.get("/{session_id}/{key}/history")
async def get_state_history(session_id: str, key: str, limit: int = 20):
    """Get state change history for debugging/analysis."""
    history_key = _get_history_key(session_id, key)
    history = _state_history.get(history_key, [])
    
    # Get current value
    db = SessionLocal()
    try:
        state = db.query(SessionState).filter(
            SessionState.session_id == session_id,
            SessionState.state_key == key
        ).first()
        current_value = json.loads(state.state_value) if state else None
    finally:
        db.close()
    
    return {
        "key": key,
        "current_value": current_value,
        "history": history[-limit:],  # Last N entries
        "version": _state_versions.get(history_key, 0)
    }


@router.get("/{session_id}/all")
async def get_all_states(session_id: str):
    """Get all state values for a session."""
    db = SessionLocal()
    try:
        states = db.query(SessionState).filter(
            SessionState.session_id == session_id
        ).all()

        result = {}
        for state in states:
            try:
                result[state.state_key] = json.loads(state.state_value)
            except:
                result[state.state_key] = None

        return {"states": result}
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
