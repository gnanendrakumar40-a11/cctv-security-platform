from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AnomalyAlert
from app.schemas import AlertPayload, AlertResponse
from typing import List

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.post("", response_model=AlertResponse)
def receive_ml_alert(payload: AlertPayload, db: Session = Depends(get_db)):
    alert = AnomalyAlert(
        device_ip=payload.device_ip,
        status=payload.status,
        threat_score=payload.threat_score,
        details=payload.details
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.get("", response_model=List[AlertResponse])
def get_all_alerts(db: Session = Depends(get_db)):
    return db.query(AnomalyAlert).order_by(AnomalyAlert.id.desc()).all()