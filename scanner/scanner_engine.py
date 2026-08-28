import socket
import requests
from typing import Dict, Any, List
from scanner.config import is_target_authorized
from scanner.cve_rules import AUDIT_RULES

def check_port(ip: str, port: int, timeout: float = 1.5) -> bool:
    """Verifies TCP port reachability using low-overhead socket probes."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((ip, port)) == 0
    except Exception:
        return False

def grab_http_banner(ip: str, port: int) -> str:
    """Extracts non-sensitive service headers and title identifiers."""
    url = f"http://{ip}:{port}"
    try:
        response = requests.get(url, timeout=2.0, verify=False)
        server = response.headers.get("Server", "")
        title = ""
        if "<title>" in response.text.lower():
            start = response.text.lower().find("<title>") + 7
            end = response.text.lower().find("</title>")
            title = response.text[start:end].strip()
        
        banner_parts = [p for p in [server, title] if p]
        return " - ".join(banner_parts) if banner_parts else "Embedded Web Server"
    except Exception:
        return "Generic Network Device"

def run_vapt_scan(target_ip: str, target_port: int = 8081) -> Dict[str, Any]:
    """
    Main vulnerability assessment pipeline invoked by the backend API.
    """
    # 1. Enforce strict scope compliance
    if not is_target_authorized(target_ip):
        return {
            "status": "REJECTED",
            "message": f"Target {target_ip} is outside authorized scanning scope."
        }

    # 2. Check port reachability
    is_open = check_port(target_ip, target_port)
    if not is_open:
        return {
            "status": "COMPLETED",
            "device": {"banner": "Unreachable / Port Closed"},
            "findings": [],
            "risk_score": 0,
            "risk_level": "INFO"
        }

    # 3. Retrieve service banner
    banner = grab_http_banner(target_ip, target_port)

    # 4. Evaluate against audit signatures
    findings: List[Dict[str, Any]] = []
    total_risk = 0

    if target_port in [80, 8080, 8081]:
        rule = AUDIT_RULES[0]
        findings.append({
            "rule_id": rule["id"],
            "title": rule["title"],
            "severity": rule["severity"],
            "evidence": f"Port {target_port} responding with: {banner}",
            "remediation": rule["remediation"]
        })
        total_risk += rule["risk_points"]

    if target_port == 554:
        rule = AUDIT_RULES[1]
        findings.append({
            "rule_id": rule["id"],
            "title": rule["title"],
            "severity": rule["severity"],
            "evidence": "RTSP media transport listener active on default port 554",
            "remediation": rule["remediation"]
        })
        total_risk += rule["risk_points"]

    if target_port in [8000, 37777]:
        rule = AUDIT_RULES[2]
        findings.append({
            "rule_id": rule["id"],
            "title": rule["title"],
            "severity": rule["severity"],
            "evidence": f"Proprietary management port {target_port} open",
            "remediation": rule["remediation"]
        })
        total_risk += rule["risk_points"]

    # 5. Compute overall risk posture
    if total_risk >= 70:
        risk_level = "CRITICAL"
    elif total_risk >= 40:
        risk_level = "HIGH"
    elif total_risk >= 20:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "status": "COMPLETED",
        "device": {"banner": banner},
        "findings": findings,
        "risk_score": total_risk,
        "risk_level": risk_level
    }

if __name__ == "__main__":
    import json
    # Local CLI verification test
    test_result = run_vapt_scan("127.0.0.1", 8081)
    print(json.dumps(test_result, indent=2))