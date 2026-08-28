import sys
import os

# Guarantee root directory resolution for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import scan_routes, alert_routes

# Create database schema on server startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NTRO CCTV/DVR Security Platform - Backend Engine",
    description="Core REST API for orchestration, scan persistence, and ML alert ingestion.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan_routes.router)
app.include_router(alert_routes.router)

@app.get("/health")
def health_check():
    return {"status": "ONLINE", "service": "CCTV VAPT API Engine"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)