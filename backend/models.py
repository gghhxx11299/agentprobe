from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    archetype = Column(String, nullable=False)
    selected_traps = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # V2 fields
    mode = Column(String, nullable=False, default="shotgun")  # shotgun/sniper/campaign/blind
    difficulty = Column(String, nullable=False, default="medium")  # easy/medium/hard/mixed
    seed = Column(Integer, nullable=False, default=0)
    campaign_id = Column(String, nullable=True)  # Links campaign sessions

    trap_logs = relationship("TrapLog", back_populates="session", cascade="all, delete-orphan")
    campaign_sessions = relationship("CampaignSession", back_populates="session", cascade="all, delete-orphan")
    analysis_results = relationship("AnalysisResult", back_populates="session", cascade="all, delete-orphan")
    leaderboard_entry = relationship("LeaderboardEntry", back_populates="session", cascade="all, delete-orphan")


class TrapLog(Base):
    __tablename__ = "trap_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    trap_type = Column(String, nullable=False)
    tier = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String, nullable=True)
    
    # V2 fields
    confidence = Column(Integer, nullable=False, default=100)  # 0-100
    trigger_type = Column(String, nullable=False, default="load")  # scroll/engagement/time/navigation/load/interaction
    time_to_trigger = Column(Integer, nullable=False, default=0)  # seconds since page load

    session = relationship("Session", back_populates="trap_logs")


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
    traps_identified = Column(Text, nullable=False)  # JSON array
    traps_acted_on = Column(Text, nullable=False)  # JSON array
    traps_ignored = Column(Text, nullable=False)  # JSON array
    self_awareness_score = Column(Integer, nullable=False)
    vulnerability_profile = Column(Text, nullable=False)  # JSON object
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="analysis_results")


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    framework = Column(String, nullable=False)  # GPT-4o/Gemini/Claude/Custom/Other
    mode = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    response_mode = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="leaderboard_entry")
