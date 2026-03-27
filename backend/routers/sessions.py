from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import random
import uuid
import hashlib

router = APIRouter()

# In-memory store for sessions (will use DB in production)
sessions_store = {}


class SessionCreateRequest(BaseModel):
    selected_traps: List[str]
    mode: Optional[str] = "shotgun"  # shotgun/sniper/campaign/blind
    difficulty: Optional[str] = "medium"  # easy/medium/hard/mixed
    archetype: Optional[str] = None


class SessionCreateResponse(BaseModel):
    session_id: str
    target_url: str
    archetype: str
    mode: str
    difficulty: str
    seed: int
    created_at: str


class CampaignCreateResponse(BaseModel):
    campaign_id: str
    session_ids: List[str]
    target_urls: List[str]
    archetype: str
    mode: str
    difficulty: str
    created_at: str


def generate_seed() -> int:
    """Generate a random seed for reproducibility."""
    return random.randint(0, 2**31 - 1)


def select_trap_for_difficulty(trap_name: str, difficulty: str) -> bool:
    """Determine if a trap should be included based on difficulty."""
    # Trap difficulty mapping
    easy_traps = {"ping", "html_comment", "meta_inject", "alt_text_injection", "svg_instruction"}
    hard_traps = {"credential_lure", "self_report", "redirect_chain", "cross_frame", "base64_encoded"}
    
    if difficulty == "easy":
        return trap_name in easy_traps or random.random() > 0.7
    elif difficulty == "hard":
        return trap_name in hard_traps or random.random() > 0.3
    else:  # medium or mixed
        return True


@router.post("/create", response_model=SessionCreateResponse)
async def create_session(request: SessionCreateRequest):
    from database import SessionLocal
    from models import Session as SessionModel

    session_id = str(uuid.uuid4())
    seed = generate_seed()
    random.seed(seed)
    
    # Handle mode selection
    mode = request.mode or "shotgun"
    difficulty = request.difficulty or "medium"
    archetype = request.archetype or random.choice(["ecommerce", "saas", "banking", "government"])
    
    # Select traps based on mode
    if mode == "sniper":
        # Select exactly ONE trap randomly
        selected_trap = random.choice(request.selected_traps)
        selected_traps = [selected_trap]
    elif mode == "blind":
        # Randomly select trap categories based on difficulty
        selected_traps = [t for t in request.selected_traps if select_trap_for_difficulty(t, difficulty)]
        if not selected_traps:
            selected_traps = request.selected_traps[:5]  # Fallback to first 5
    else:
        # shotgun or campaign - use all selected traps
        selected_traps = request.selected_traps
    
    random.seed()  # Reset random state
    
    db = SessionLocal()
    try:
        session = SessionModel(
            id=session_id,
            archetype=archetype,
            selected_traps=json.dumps(selected_traps),
            created_at=datetime.utcnow(),
            mode=mode,
            difficulty=difficulty,
            seed=seed,
            campaign_id=None
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
        mode=mode,
        difficulty=difficulty,
        seed=seed,
        created_at=datetime.utcnow().isoformat()
    )


@router.post("/campaign", response_model=CampaignCreateResponse)
async def create_campaign(request: SessionCreateRequest):
    """Create a campaign with 5 linked sessions, one trap per session."""
    from database import SessionLocal
    from models import Session as SessionModel, CampaignSession as CampaignSessionModel
    
    campaign_id = str(uuid.uuid4())
    seed = generate_seed()
    random.seed(seed)
    
    archetype = request.archetype or random.choice(["ecommerce", "saas", "banking", "government"])
    difficulty = request.difficulty or "medium"
    
    # Shuffle and select 5 traps for the campaign
    shuffled_traps = request.selected_traps.copy()
    random.shuffle(shuffled_traps)
    campaign_traps = shuffled_traps[:5]
    
    if len(campaign_traps) < 5:
        # If fewer than 5 traps selected, repeat some
        while len(campaign_traps) < 5:
            campaign_traps.append(random.choice(request.selected_traps))
    
    session_ids = []
    target_urls = []
    
    db = SessionLocal()
    try:
        for i, trap in enumerate(campaign_traps):
            session_id = str(uuid.uuid4())
            session_seed = seed + i  # Related seed for reproducibility
            
            session = SessionModel(
                id=session_id,
                archetype=archetype,
                selected_traps=json.dumps([trap]),
                created_at=datetime.utcnow(),
                mode="campaign",
                difficulty=difficulty,
                seed=session_seed,
                campaign_id=campaign_id
            )
            db.add(session)
            
            campaign_session = CampaignSessionModel(
                id=str(uuid.uuid4()),
                campaign_id=campaign_id,
                session_number=i + 1,
                session_id=session_id,
                created_at=datetime.utcnow()
            )
            db.add(campaign_session)
            
            session_ids.append(session_id)
            target_urls.append(f"{BASE_URL}/test/{session_id}")
        
        db.commit()
    finally:
        db.close()
    
    random.seed()  # Reset random state

    return CampaignCreateResponse(
        campaign_id=campaign_id,
        session_ids=session_ids,
        target_urls=target_urls,
        archetype=archetype,
        mode="campaign",
        difficulty=difficulty,
        created_at=datetime.utcnow().isoformat()
    )


@router.post("/retest/{session_id}")
async def retest_session(session_id: str):
    """Create a new session with the same seed and config for retesting."""
    from database import SessionLocal
    from models import Session as SessionModel
    
    db = SessionLocal()
    try:
        original = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not original:
            raise HTTPException(status_code=404, detail="Session not found")
        
        new_session_id = str(uuid.uuid4())
        
        session = SessionModel(
            id=new_session_id,
            archetype=original.archetype,
            selected_traps=original.selected_traps,
            created_at=datetime.utcnow(),
            mode=original.mode,
            difficulty=original.difficulty,
            seed=original.seed,  # Same seed for identical conditions
            campaign_id=original.campaign_id
        )
        db.add(session)
        db.commit()
        
        from trap_engine.traps import BASE_URL
        return {
            "session_id": new_session_id,
            "target_url": f"{BASE_URL}/test/{new_session_id}",
            "archetype": original.archetype,
            "mode": original.mode,
            "difficulty": original.difficulty,
            "seed": original.seed,
            "created_at": datetime.utcnow().isoformat()
        }
    finally:
        db.close()
