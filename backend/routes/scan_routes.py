from fastapi.responses import JSONResponse
import datetime

@router.get("/api/reports/export")
def export_security_report(db: Session = Depends(get_db)):
    """Exports a summarized VAPT security report with compliance scores."""
    scans = db.query(ScanRecord).all()
    alerts = db.query(AlertRecord).all()

    total_scans = len(scans)
    total_alerts = len(alerts)
    high_critical_count = sum(1 for s in scans if s.posture in ["HIGH", "CRITICAL"])
    
    # Calculate overall security posture grade
    if total_scans == 0:
        overall_grade = "N/A"
    elif high_critical_count == 0:
        overall_grade = "A (HARDENED)"
    elif high_critical_count <= 2:
        overall_grade = "B (NEEDS_ATTENTION)"
    else:
        overall_grade = "C (CRITICAL_RISK)"

    report_data = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "platform": "CCTV & DVR Automated VAPT Assessment Engine",
        "executive_summary": {
            "overall_posture_grade": overall_grade,
            "total_endpoints_audited": total_scans,
            "total_behavioral_threats_detected": total_alerts,
            "high_critical_vulnerabilities": high_critical_count
        },
        "vulnerability_scan_details": [
            {
                "target": f"{s.target_ip}:{s.port}",
                "posture": s.posture,
                "score": s.score,
                "banner": s.banner,
                "timestamp": str(s.created_at) if hasattr(s, 'created_at') else "N/A"
            }
            for s in scans
        ],
        "threat_detection_log": [
            {
                "device_ip": a.device_ip,
                "status": a.status,
                "threat_score": a.threat_score,
                "details": a.details
            }
            for a in alerts
        ]
    }
    return JSONResponse(content=report_data)