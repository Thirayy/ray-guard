from apscheduler.schedulers.background import BackgroundScheduler
from backend.app.core.database import SessionLocal
from backend.app.models.target import Target
from backend.app.services.scan_service import run_full_scan

def auto_scan():
    db = SessionLocal()

    targets = db.query(Target).all()

    for t in targets:
        try:
            run_full_scan(db, target_id=t.id, domain=t.domain)
        except:
            pass

    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(auto_scan, "interval", minutes=30)
