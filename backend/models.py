from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    archetype = Column(String, nullable=False)
    selected_traps = Column(Text, nullable=False)  # JSON string (v1 legacy)
    selected_categories = Column(Text, nullable=True)  # JSON string (v2)
    primary_task = Column(Text, nullable=True)  # v2
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # V2 fields
    mode = Column(String, nullable=False, default="shotgun")  # shotgun/sniper/campaign/blind
    difficulty = Column(String, nullable=False, default="medium")  # easy/medium/hard/mixed
    seed = Column(Integer, nullable=False, default=0)
    campaign_id = Column(String, nullable=True)  # Links campaign sessions

    analytics_logs = relationship("AnalyticsLog", back_populates="session", cascade="all, delete-orphan")
    session_states = relationship("SessionState", back_populates="session", cascade="all, delete-orphan")
    campaign_sessions = relationship("CampaignSession", back_populates="session", cascade="all, delete-orphan")
    analysis_results = relationship("AnalysisResult", back_populates="session", cascade="all, delete-orphan")
    leaderboard_entry = relationship("LeaderboardEntry", back_populates="session", cascade="all, delete-orphan")


class AnalyticsLog(Base):
    __tablename__ = "analytics_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    event_type = Column(String, nullable=True)  # was trap_type
    category = Column(String, nullable=True)  # v2 methodology category
    signal_type = Column(String, nullable=False, default="triggered")  # control/triggered/identified
    tier = Column(Integer, nullable=False, default=1)
    severity = Column(String, nullable=False, default="medium")
    triggered_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String, nullable=True)
    
    # V2 fields
    confidence = Column(Integer, nullable=False, default=100)  # 0-100
    trigger_source = Column(String, nullable=False, default="load")  # was trigger_type
    time_to_trigger = Column(Integer, nullable=False, default=0)  # seconds since page load

    session = relationship("Session", back_populates="analytics_logs")


class SessionState(Base):
    __tablename__ = "session_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    state_key = Column(String, nullable=False)  # cart, contacts, transfers, etc.
    state_value = Column(Text, nullable=False)  # JSON string
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("Session", back_populates="session_states")


class CampaignSession(Base):
    __tablename__ = "campaign_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    session_number = Column(Integer, nullable=False)  # 1-5
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="campaign_sessions")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    raw_output = Column(Text, nullable=False)
    response_mode = Column(String, nullable=False)  # naive/defensive/resistant/inconsistent
    elements_identified = Column(Text, nullable=False)  # was traps_identified
    elements_acted_on = Column(Text, nullable=False)  # was traps_acted_on
    elements_ignored = Column(Text, nullable=False)  # was traps_ignored
    self_awareness_score = Column(Integer, nullable=False)
    self_awareness_explanation = Column(Text, nullable=True)
    key_finding = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    vulnerability_profile = Column(Text, nullable=False)  # JSON object
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="analysis_results")


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

    session = relationship("Session", back_populates="leaderboard_entry")
