from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.alert import Alert
from backend.app.core.response import success_response
from backend.app.repositories.alert_repository import list_alert_rows, create_alert

router = APIRouter(prefix="/alerts", tags=["Alerts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_alerts(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    rows = list_alert_rows(db, limit=limit)
    data = [
        {
            "id": r.id,
            "target_id": r.target_id,
            "domain": r.domain,
            "message": r.message,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
    return success_response("Alerts fetched", data)

@router.get("/test")
def create_test_alert(
    domain: str = "example.com",
    target_id: int | None = None,
    port: int = 22,
    db: Session = Depends(get_db),
):
    create_alert(
        db,
        target_id=target_id,
        domain=domain,
        message=f"⚠️ Test Alert: New port opened {port}",
    )
    return success_response("Test alert created")
