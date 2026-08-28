from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="ANALYST")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, default=80)
    device_type = Column(String, default="IP_CAMERA")
    is_authorized = Column(Integer, default=1)


class ScanRecord(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target_ip = Column(String, nullable=False)
    target_port = Column(Integer, nullable=False)
    device_banner = Column(String, default="Unknown")
    risk_score = Column(Integer, default=0)
    risk_level = Column(String, default="LOW")
    findings = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnomalyAlert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_ip = Column(String, nullable=False)
    status = Column(String, nullable=False)
    threat_score = Column(Float, nullable=False)
    details = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())