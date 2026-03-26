from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import random
import uuid

router = APIRouter()

# In-memory store for sessions (will use DB in production)
sessions_store = {}


class SessionCreateRequest(BaseModel):
    selected_traps: List[str]
    archetype: Optional[str] = None


class SessionCreateResponse(BaseModel):
    session_id: str
    target_url: str
    archetype: str
    created_at: str


@router.post("/create", response_model=SessionCreateResponse)
async def create_session(request: SessionCreateRequest):
    from database import SessionLocal
    from models import Session as SessionModel

    session_id = str(uuid.uuid4())
    archetype = request.archetype or random.choice(["ecommerce", "saas", "banking", "government"])

    db = SessionLocal()
    try:
        session = SessionModel(
            id=session_id,
            archetype=archetype,
            selected_traps=json.dumps(request.selected_traps),
            created_at=datetime.utcnow()
        )
        db.add(session)
        db.commit()
    finally:
        db.close()

    from trap_engine.traps import BASE_URL
    target_url = f"{BASE_URL}/test/{session_id}"

    return SessionCreateResponse(
        session_id=session_id,
        target_url=target_url,
        archetype=archetype,
        created_at=datetime.utcnow().isoformat()
    )
