from pydantic import BaseModel

class SimulationRequest(BaseModel):
    target_ip: str
    scenario_type: str  # "volumetric_spike" | "auth_burst"

@router.post("/api/simulate")
def trigger_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    """Triggers an event simulation scenario and logs findings to database."""
    score = 0.85 if req.scenario_type == "volumetric_spike" else 0.72
    details = f"Simulated {req.scenario_type.replace('_', ' ').title()} against {req.target_ip}"
    
    new_alert = AlertRecord(
        device_ip=req.target_ip,
        status="SIMULATED_THREAT",
        threat_score=score,
        details=details
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return {"status": "success", "alert_id": new_alert.id, "scenario": req.scenario_type}