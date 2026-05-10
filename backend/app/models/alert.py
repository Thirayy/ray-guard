from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, index=True, nullable=True)
    domain = Column(String, index=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
