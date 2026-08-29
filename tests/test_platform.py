import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_and_docs():
    """Verify backend endpoints are up."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_get_scans():
    """Verify retrieval of vulnerability scan records."""
    response = client.get("/api/scans")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_alerts():
    """Verify retrieval of ML threat alert records."""
    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_fetch_alert():
    """Test full round-trip ingestion of ML threat alerts."""
    payload = {
        "device_ip": "192.168.1.200",
        "status": "ANOMALY_DETECTED",
        "threat_score": 0.95,
        "details": "Automated pipeline integration test anomaly"
    }
    post_res = client.post("/api/alerts", json=payload)
    assert post_res.status_code == 200
    data = post_res.json()
    assert data["device_ip"] == payload["device_ip"]
    assert data["threat_score"] == payload["threat_score"]