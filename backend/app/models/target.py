from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.app.core.database import Base


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
