from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

# --- USER SCHEMAS ---
class UserAuth(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- SCAN SCHEMAS ---
class ScanRequest(BaseModel):
    target_ip: str
    target_port: int = 8081

class ScanResponse(BaseModel):
    id: int
    target_ip: str
    target_port: int
    device_banner: str
    risk_score: int
    risk_level: str
    findings: List[Any]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- ALERT SCHEMAS ---
class AlertPayload(BaseModel):
    device_ip: str
    status: str
    threat_score: float
    details: str

class AlertResponse(AlertPayload):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True