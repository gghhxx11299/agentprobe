from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import random
import uuid
import hashlib

from trap_engine import BASE_URL

router = APIRouter()

# In-memory store for sessions (will use DB in production)
sessions_store = {}


class SessionCreateRequest(BaseModel):
    selected_traps: Optional[List[str]] = None
    selected_categories: Optional[List[str]] = None
    primary_task: Optional[str] = None
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
    primary_task: Optional[str]
    created_at: str


class CampaignCreateResponse(BaseModel):
    campaign_id: str
    session_ids: List[str]
    target_urls: List[str]
    archetype: str
    mode: str
    difficulty: str
    primary_task: Optional[str]
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
    
    # v2: Handle categories and primary task
    selected_categories = request.selected_categories or []
    primary_task = request.primary_task
    
    # v1 legacy support
    selected_traps = request.selected_traps or []
    
    # Select traps based on mode
    if mode == "sniper":
        if selected_categories:
            selected_categories = [random.choice(selected_categories)]
        if selected_traps:
            selected_traps = [random.choice(selected_traps)]
    elif mode == "blind":
        if selected_categories:
            random.shuffle(selected_categories)
            selected_categories = selected_categories[:2]
    
    random.seed()  # Reset random state
    
    db = SessionLocal()
    try:
        session = SessionModel(
            id=session_id,
            archetype=archetype,
            selected_traps=json.dumps(selected_traps),
            selected_categories=json.dumps(selected_categories),
            primary_task=primary_task,
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

    from trap_engine import BASE_URL
    target_url = f"{BASE_URL}/test/{session_id}"

    return SessionCreateResponse(
        session_id=session_id,
        target_url=target_url,
        archetype=archetype,
        mode=mode,
        difficulty=difficulty,
        seed=seed,
        primary_task=primary_task,
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
    primary_task = request.primary_task
    
    # Select categories/traps for campaign
    shuffled_items = (request.selected_categories or request.selected_traps or []).copy()
    random.shuffle(shuffled_items)
    campaign_items = shuffled_items[:5]
    
    if len(campaign_items) < 5 and shuffled_items:
        while len(campaign_items) < 5:
            campaign_items.append(random.choice(shuffled_items))
    
    session_ids = []
    target_urls = []
    
    db = SessionLocal()
    try:
        for i, item in enumerate(campaign_items):
            session_id = str(uuid.uuid4())
            session_seed = seed + i
            
            # Check if item is category or trap
            is_category = request.selected_categories and item in request.selected_categories
            
            session = SessionModel(
                id=session_id,
                archetype=archetype,
                selected_traps=json.dumps([item] if not is_category else []),
                selected_categories=json.dumps([item] if is_category else []),
                primary_task=primary_task,
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
        primary_task=primary_task,
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
            selected_categories=original.selected_categories,
            primary_task=original.primary_task,
            created_at=datetime.utcnow(),
            mode=original.mode,
            difficulty=original.difficulty,
            seed=original.seed,  # Same seed for identical conditions
            campaign_id=original.campaign_id
        )
        db.add(session)
        db.commit()
        
        from trap_engine import BASE_URL
        return {
            "session_id": new_session_id,
            "target_url": f"{BASE_URL}/test/{new_session_id}",
            "archetype": original.archetype,
            "mode": original.mode,
            "difficulty": original.difficulty,
            "seed": original.seed,
            "primary_task": original.primary_task,
            "created_at": datetime.utcnow().isoformat()
        }
    finally:
        db.close()
