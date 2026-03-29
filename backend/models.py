import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    archetype = Column(String, nullable=False)
    selected_traps = Column(Text, nullable=False)
    selected_categories = Column(Text, nullable=True)
    primary_task = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    mode = Column(String, nullable=False, default="shotgun")
    difficulty = Column(String, nullable=False, default="medium")
    seed = Column(Integer, nullable=False, default=0)
    campaign_id = Column(String, nullable=True)
    
    # v3: Optimistic Locking & State Tracking
    version = Column(Integer, default=1)
    state = Column(JSON, default={})
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    signals = relationship("Signal", back_populates="session", cascade="all, delete-orphan")

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    event_type = Column(String, nullable=True) # e.g. "honeypot_link"
    category = Column(String, nullable=True) # e.g. "instruction_following"
    signal_type = Column(String, nullable=False, default="triggered") # triggered/identified/control/stale_interaction
    
    # v3: Intent Capture & Context
    reasoning = Column(Text, nullable=True) 
    version_at_trigger = Column(Integer, nullable=True)
    
    tier = Column(Integer, nullable=False, default=1)
    severity = Column(String, nullable=False, default="medium")
    triggered_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String, nullable=True)
    confidence = Column(Integer, nullable=False, default=100)
    trigger_source = Column(String, nullable=False, default="load")
    time_to_trigger = Column(Integer, nullable=False, default=0)
    
    session = relationship("Session", back_populates="signals")

class SessionState(Base):
    __tablename__ = "session_states"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    state_key = Column(String, nullable=False)
    state_value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CampaignSession(Base):
    __tablename__ = "campaign_sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    session_number = Column(Integer, nullable=False)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    framework = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    response_mode = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
