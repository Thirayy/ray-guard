from sqlalchemy import Column, Integer, String, DateTime, Text
from backend.app.core.database import Base
import datetime

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)

    ip = Column(String)
    ports = Column(Text)  # store csv
    risk = Column(Integer, default=0)

    ssl_issuer = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
