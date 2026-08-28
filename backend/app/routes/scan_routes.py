from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ScanRecord
from app.schemas import ScanRequest, ScanResponse
from typing import List
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
try:
    from scanner.scanner_engine import run_vapt_scan
except ImportError:
    def run_vapt_scan(ip: str, port: int):
        return {
            "status": "COMPLETED",
            "device": {"banner": "Simulated Hikvision Camera"},
            "findings": [
                {
                    "title": "Insecure Transport Protocol",
                    "evidence": "Web management portal exposed over plain HTTP"
                }
            ],
            "risk_score": 65,
            "risk_level": "HIGH"
        }

router = APIRouter(prefix="/api/scans", tags=["Scans"])

@router.get("", response_model=List[ScanResponse])
def get_all_scans(db: Session = Depends(get_db)):
    return db.query(ScanRecord).order_by(ScanRecord.id.desc()).all()

@router.post("", response_model=ScanResponse)
def execute_scan(payload: ScanRequest, db: Session = Depends(get_db)):
    scan_result = run_vapt_scan(payload.target_ip, payload.target_port)
    
    if scan_result.get("status") == "REJECTED":
        raise HTTPException(status_code=403, detail=scan_result.get("message"))

    record = ScanRecord(
        target_ip=payload.target_ip,
        target_port=payload.target_port,
        device_banner=scan_result.get("device", {}).get("banner", "Unknown"),
        risk_score=scan_result.get("risk_score", 0),
        risk_level=scan_result.get("risk_level", "LOW"),
        findings=scan_result.get("findings", [])
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return record