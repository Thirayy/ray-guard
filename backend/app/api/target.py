from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.core.response import success_response
from backend.app.models.target import Target
from backend.app.schemas.target import TargetCreate, TargetUpdate

router = APIRouter(prefix="/targets", tags=["Targets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_target(payload: TargetCreate, db: Session = Depends(get_db)):

    existing = db.query(Target).filter(Target.domain == payload.domain).first()

    if existing:
        raise HTTPException(status_code=400, detail="Target already exists")

    row = Target(domain=payload.domain)

    db.add(row)
    db.commit()
    db.refresh(row)

    return success_response("Target created", {
        "id": row.id,
        "domain": row.domain
    })


@router.get("/")
def list_targets(db: Session = Depends(get_db)):

    rows = db.query(Target).order_by(Target.id.desc()).all()

    data = [{"id": r.id, "domain": r.domain} for r in rows]

    return success_response("Targets fetched", data)


@router.put("/{target_id}")
def update_target(target_id: int, payload: TargetUpdate, db: Session = Depends(get_db)):

    row = db.query(Target).filter(Target.id == target_id).first()

    if not row:
        raise HTTPException(status_code=404, detail="Target not found")

    row.domain = payload.domain
    db.commit()

    return success_response("Target updated", {
        "id": row.id,
        "domain": row.domain
    })


@router.delete("/{target_id}")
def delete_target(target_id: int, db: Session = Depends(get_db)):

    row = db.query(Target).filter(Target.id == target_id).first()

    if not row:
        raise HTTPException(status_code=404, detail="Target not found")

    db.delete(row)
    db.commit()

    return success_response("Target deleted")
