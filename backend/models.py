from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
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

    trap_logs = relationship("TrapLog", back_populates="session", cascade="all, delete-orphan")


class TrapLog(Base):
    __tablename__ = "trap_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    trap_type = Column(String, nullable=False)
    tier = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String, nullable=True)

    session = relationship("Session", back_populates="trap_logs")
