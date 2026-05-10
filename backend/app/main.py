from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from backend.app.core.database import Base, engine
from backend.app.core.scheduler import scheduler
from backend.app.core.response import error_response
from sqlalchemy import text

from backend.app.api.target import router as target_router
from backend.app.api.scanner import router as scanner_router
from backend.app.api.alerts import router as alerts_router

from dotenv import load_dotenv

load_dotenv()

# create tables
Base.metadata.create_all(bind=engine)

# lightweight schema sync for dev (create_all won't add new columns)
try:
    with engine.begin() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS rayguard"))
        conn.execute(text("USE rayguard"))
        conn.execute(text("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS target_id INTEGER"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_alerts_target_id ON alerts (target_id)"))
except Exception:
    pass

# start scheduler
scheduler.start()

app = FastAPI(
    title="Ray-Guard API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(target_router)
app.include_router(scanner_router)
app.include_router(alerts_router)

# global error
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response("Internal server error", 500)
    )

# frontend dashboard
@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse("index.html")
