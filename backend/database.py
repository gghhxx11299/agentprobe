import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Use SQLite for local development, PostgreSQL for production (Render)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentprobe_v3.db")

# Fix for Render/PostgreSQL if it starts with 'postgres://' (SQLAlchemy 1.4+ expects 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from models import Base
    Base.metadata.create_all(bind=engine)
