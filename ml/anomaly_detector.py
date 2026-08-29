import numpy as np
from sklearn.ensemble import IsolationForest
import requests
import json
import time
from typing import Dict, Any

class CCTVAnomalyDetector:
    def __init__(self, contamination: float = 0.05):
        """
        Initializes the Isolation Forest behavioral model.
        Features: [Packet Rate (pps), Byte Rate (KB/s), RTSP Sessions]
        """
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
        )
        self._train_baseline()

    def _train_baseline(self):
        """Generates baseline traffic patterns representing normal CCTV operation."""
        np.random.seed(42)
        # Normal camera streaming: ~50-120 pps, ~400-800 KB/s, 1-3 active sessions
        packet_rate = np.random.normal(loc=85, scale=15, size=500)
        byte_rate = np.random.normal(loc=600, scale=80, size=500)
        rtsp_sessions = np.random.randint(1, 4, size=500)

        x_train = np.column_stack([packet_rate, byte_rate, rtsp_sessions])
        self.model.fit(x_train)

    def evaluate_telemetry(self, packet_rate: float, byte_rate: float, rtsp_sessions: int) -> Dict[str, Any]:
        """
        Evaluates real-time device metrics and calculates threat probability.
        """
        sample = np.array([[packet_rate, byte_rate, rtsp_sessions]])
        prediction = self.model.predict(sample)[0]  # -1 for anomaly, 1 for normal
        decision_score = self.model.decision_function(sample)[0]

        # Normalize score into a 0.0 - 1.0 threat index
        threat_score = round(float(np.clip(1.0 - (decision_score + 0.5), 0.0, 1.0)), 2)

        # Cast explicitly to native Python bool for JSON serialization compatibility
        is_anomaly = bool(prediction == -1)
        status = "ANOMALY_DETECTED" if is_anomaly else "NORMAL"

        return {
            "is_anomaly": is_anomaly,
            "status": status,
            "threat_score": threat_score,
            "metrics": {
                "packet_rate_pps": float(packet_rate),
                "byte_rate_kbs": float(byte_rate),
                "rtsp_sessions": int(rtsp_sessions)
            }
        }

def send_alert_to_backend(device_ip: str, evaluation: Dict[str, Any], backend_url: str = "http://127.0.0.1:8000/api/alerts"):
    """Dispatches detected anomalies directly to Team 2's backend API."""
    if not evaluation["is_anomaly"]:
        return None

    payload = {
        "device_ip": device_ip,
        "status": evaluation["status"],
        "threat_score": evaluation["threat_score"],
        "details": f"Volumetric spike detected: {evaluation['metrics']['packet_rate_pps']} pps, {evaluation['metrics']['byte_rate_kbs']} KB/s with {evaluation['metrics']['rtsp_sessions']} active sessions."
    }

    try:
        response = requests.post(backend_url, json=payload, timeout=2.0)
        return response.status_code
    except Exception as exc:
        print(f"[ML Alert Engine] Backend notification failed (Server offline?): {exc}")
        return None

if __name__ == "__main__":
    print("[*] Initializing CCTV Behavioral Threat Detector...")
    detector = CCTVAnomalyDetector()

    # Test Sample 1: Normal Streaming Behavior
    normal_eval = detector.evaluate_telemetry(packet_rate=80.0, byte_rate=580.0, rtsp_sessions=2)
    print("\n[Normal Test Result]:", json.dumps(normal_eval, indent=2))

    # Test Sample 2: RTSP Stream Flood / DoS Anomaly
    attack_eval = detector.evaluate_telemetry(packet_rate=650.0, byte_rate=4500.0, rtsp_sessions=18)
    print("\n[Anomaly Test Result]:", json.dumps(attack_eval, indent=2))

    # Trigger alert integration
    send_alert_to_backend("192.168.1.102", attack_eval)