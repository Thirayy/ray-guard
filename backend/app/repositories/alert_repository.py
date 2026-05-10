from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from backend.app.models.alert import Alert


def create_alert(db, *, target_id: int | None, domain: str, message: str) -> Alert:
    # Be resilient to schema drift (e.g., existing DB without `target_id` column).
    row = Alert(domain=domain, message=message, created_at=datetime.utcnow())
    if target_id is not None:
        row.target_id = target_id

    db.add(row)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        # Retry without setting `target_id` (for older DB schemas)
        row = Alert(domain=domain, message=message, created_at=datetime.utcnow())
        db.add(row)
        db.commit()

    db.refresh(row)
    return row


def list_alert_rows(db, *, limit: int = 50):
    q = db.query(Alert).order_by(Alert.id.desc())
    if limit:
        q = q.limit(limit)
    return q.all()
