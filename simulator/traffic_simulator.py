import time
import random
import requests

API_URL = "http://127.0.0.1:8000/api/alerts"

def generate_telemetry_event(scenario: str) -> dict:
    """Generates synthetic network telemetry based on selected profile."""
    if scenario == "normal":
        return {
            "packets_per_sec": random.uniform(15.0, 45.0),
            "bandwidth_kbps": random.uniform(200.0, 600.0),
            "active_sessions": random.randint(1, 3),
            "profile": "NORMAL_OPERATION"
        }
    elif scenario == "volumetric_spike":
        return {
            "packets_per_sec": random.uniform(600.0, 1200.0),
            "bandwidth_kbps": random.uniform(4000.0, 8500.0),
            "active_sessions": random.randint(15, 30),
            "profile": "SYNTHETIC_DDoS_SPIKE"
        }
    elif scenario == "auth_burst":
        return {
            "packets_per_sec": random.uniform(200.0, 400.0),
            "bandwidth_kbps": random.uniform(800.0, 1500.0),
            "active_sessions": random.randint(40, 80),
            "profile": "SYNTHETIC_AUTH_FLOOD"
        }
    else:
        raise ValueError(f"Unknown scenario: {scenario}")

def run_simulation(device_ip: str = "192.168.1.105", scenario: str = "volumetric_spike"):
    """Runs a simulated anomaly scenario and forwards telemetry to the security pipeline."""
    print(f"[*] Starting Security Event Simulation: [{scenario.upper()}] against {device_ip}")
    telemetry = generate_telemetry_event(scenario)
    
    print(f"    - Rate: {telemetry['packets_per_sec']:.1f} pps")
    print(f"    - Throughput: {telemetry['bandwidth_kbps']:.1f} KB/s")
    print(f"    - Concurrent Sessions: {telemetry['active_sessions']}")

    payload = {
        "device_ip": device_ip,
        "status": "SIMULATED_ATTACK_DETECTED",
        "threat_score": 0.88 if scenario != "normal" else 0.05,
        "details": f"Simulated {telemetry['profile']} pattern: {telemetry['packets_per_sec']:.1f} pps, {telemetry['bandwidth_kbps']:.1f} KB/s, {telemetry['active_sessions']} sessions."
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[+] Alert logged successfully to Backend API (ID: {response.json().get('id')})")
        else:
            print(f"[-] Backend returned status code {response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"[-] Failed to connect to Backend API at {API_URL}: {err}")

if __name__ == "__main__":
    print("=" * 60)
    print("      CCTV PLATFORM - ATTACK SIMULATION HARNESS")
    print("=" * 60)
    # Execute a simulated flood event
    run_simulation(scenario="volumetric_spike")
    time.sleep(2)
    # Execute a simulated session burst event
    run_simulation(scenario="auth_burst")