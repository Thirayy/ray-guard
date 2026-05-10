from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.target import Target
from backend.app.services.scan_service import run_full_scan
from backend.app.core.response import success_response
from fastapi import BackgroundTasks
from backend.app.core.job_store import jobs
from backend.app.services.async_scan_service import process_scan, create_job
from backend.app.core.response import success_response

router = APIRouter(prefix="/scan", tags=["Scanner"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{target_id}")
def run_scan(target_id: int, db: Session = Depends(get_db)):

    target = db.query(Target).filter(Target.id == target_id).first()

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    result = run_full_scan(db, target_id=target.id, domain=target.domain)

    return success_response("Scan completed", result)

@router.post("/{target_id}/start")
def start_scan(
    target_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    target = db.query(Target).filter(Target.id == target_id).first()

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    job_id = create_job()

    jobs[job_id] = {
        "status": "queued",
        "target_id": target.id,
        "target": target.domain
    }

    background_tasks.add_task(
        process_scan,
        job_id,
        target.id,
        target.domain
    )

    return success_response("Scan queued", {
        "job_id": job_id,
        "status": "queued"
    })


@router.get("/job/{job_id}")
def get_job(job_id: str):

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return success_response("Job status", jobs[job_id])

@router.get("/")
def health():
    return success_response("Health check passed", {"status": "Ray-Guard AI Scanner Active"})
