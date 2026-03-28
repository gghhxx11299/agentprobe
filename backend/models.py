import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class SessionV3(Base):
    __tablename__ = "sessions_v3"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    archetype = Column(String, nullable=False)
    state = Column(JSON, default={})
    version = Column(Integer, default=1)
    seed = Column(Integer, default=0)
    primary_task = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    signals = relationship("SignalV3", back_populates="session", cascade="all, delete-orphan")

class SignalV3(Base):
    __tablename__ = "signals_v3"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions_v3.id"), nullable=False)
    trap_id = Column(String, nullable=False)
    category = Column(String, nullable=False)
    signal_type = Column(String, nullable=False) # triggered/identified/control/stale_interaction
    
    # INTENT CAPTURE (V3 Fix)
    reasoning = Column(Text, nullable=True) 
    
    method = Column(String, default="GET")
    path = Column(String)
    user_agent = Column(String)
    request_headers = Column(JSON, default={})
    triggered_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Integer, default=100)
    session = relationship("SessionV3", back_populates="signals")

# ── LEGACY V2 MODELS ────────────────────────────

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

class AnalyticsLog(Base):
    __tablename__ = "analytics_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    event_type = Column(String, nullable=True)
    category = Column(String, nullable=True)
    signal_type = Column(String, nullable=False, default="triggered")
    tier = Column(Integer, nullable=False, default=1)
    severity = Column(String, nullable=False, default="medium")
    triggered_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String, nullable=True)
    confidence = Column(Integer, nullable=False, default=100)
    trigger_source = Column(String, nullable=False, default="load")
    time_to_trigger = Column(Integer, nullable=False, default=0)

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

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    raw_output = Column(Text, nullable=False)
    response_mode = Column(String, nullable=False)
    elements_identified = Column(Text, nullable=False)
    elements_acted_on = Column(Text, nullable=False)
    elements_ignored = Column(Text, nullable=False)
    self_awareness_score = Column(Integer, nullable=False)
    self_awareness_explanation = Column(Text, nullable=True)
    key_finding = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    vulnerability_profile = Column(Text, nullable=False)
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
