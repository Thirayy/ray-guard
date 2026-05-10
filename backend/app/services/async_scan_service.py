import uuid
from backend.app.core.job_store import jobs
from backend.app.services.scan_service import run_full_scan
from backend.app.core.database import SessionLocal

def process_scan(job_id, target_id, domain):
    db = SessionLocal()

    try:
        jobs[job_id]["status"] = "running"

        result = run_full_scan(db, target_id=target_id, domain=domain)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

    finally:
        db.close()


def create_job():
    return str(uuid.uuid4())
