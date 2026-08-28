AUDIT_RULES = [
    {
        "id": "RULE-CCTV-001",
        "title": "Cleartext Management Interface (HTTP)",
        "severity": "MEDIUM",
        "risk_points": 25,
        "description": "Administrative web console is operating over unencrypted HTTP (Port 80/8081).",
        "remediation": "Enforce HTTPS with TLS 1.2+ and disable unencrypted HTTP management endpoints."
    },
    {
        "id": "RULE-CCTV-002",
        "title": "Exposed RTSP Media Stream",
        "severity": "HIGH",
        "risk_points": 40,
        "description": "RTSP media streaming service (Port 554) is accessible without transport encryption.",
        "remediation": "Enforce network access control lists (ACLs) or transition to encrypted RTSPS streams."
    },
    {
        "id": "RULE-CCTV-003",
        "title": "Default Proprietary Management Port Exposed",
        "severity": "MEDIUM",
        "risk_points": 20,
        "description": "Standard proprietary camera management port is exposed on default port assignment.",
        "remediation": "Isolate surveillance hardware onto dedicated VLANs and modify default port assignments."
    }
]