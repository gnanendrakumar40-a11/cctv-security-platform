def calculate_risk(findings):
    """
    Calculate an overall risk score and risk level.

    This is a simple project-level prioritization model.
    It is not a replacement for a formal vulnerability standard.
    """

    severity_scores = {
        "high": 4,
        "medium": 3,
        "low": 2,
        "info": 0
    }

    total_score = 0

    for finding in findings:
        severity = finding.get("severity", "info").lower()
        total_score += severity_scores.get(severity, 0)

    if total_score >= 6:
        risk_level = "HIGH"
    elif total_score >= 3:
        risk_level = "MEDIUM"
    elif total_score > 0:
        risk_level = "LOW"
    else:
        risk_level = "INFO"

    return {
        "risk_score": total_score,
        "risk_level": risk_level
    }
