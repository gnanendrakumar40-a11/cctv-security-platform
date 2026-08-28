def run_security_checks(scan_results):
    """
    Perform safe CCTV/DVR-oriented security checks.

    These checks only analyze already-observed scan results.
    Use only on systems and networks for which testing is authorized.
    """

    findings = []

    for result in scan_results:
        port = result.get("port")
        status = result.get("status")
        service = result.get("service", "")

        if status != "open":
            continue

        # RTSP is commonly used for camera video streaming.
        if port == 554:
            findings.append({
                "category": "CCTV/RTSP",
                "title": "RTSP service exposed",
                "severity": "medium",
                "port": port,
                "description": (
                    "A Real Time Streaming Protocol (RTSP) service is "
                    "reachable on the target."
                ),
                "recommendation": (
                    "Restrict RTSP access to authorized hosts and verify "
                    "that authentication and network controls are enabled."
                )
            })

        # Telnet is insecure for administration.
        elif port == 23:
            findings.append({
                "category": "Administration",
                "title": "Telnet service exposed",
                "severity": "high",
                "port": port,
                "description": (
                    "A Telnet service is reachable on the target."
                ),
                "recommendation": (
                    "Disable Telnet when it is not required and use a "
                    "secure administration method."
                )
            })

        # Plain HTTP may expose a management interface without TLS.
        elif port == 80:
            findings.append({
                "category": "Web Management",
                "title": "HTTP management interface may be exposed",
                "severity": "medium",
                "port": port,
                "description": (
                    "A plain HTTP service is reachable. If this is a "
                    "management interface, traffic may not be protected "
                    "by Transport Layer Security (TLS)."
                ),
                "recommendation": (
                    "Prefer HTTPS for management interfaces and restrict "
                    "access to trusted networks."
                )
            })

        # FTP can expose device administration or files.
        elif port == 21:
            findings.append({
                "category": "File Transfer",
                "title": "FTP service exposed",
                "severity": "medium",
                "port": port,
                "description": (
                    "A File Transfer Protocol (FTP) service is reachable."
                ),
                "recommendation": (
                    "Disable FTP when unnecessary or replace it with a "
                    "secure file-transfer method."
                )
            })

        # Common alternate web-management ports.
        elif port in (8000, 8080):
            findings.append({
                "category": "Web Management",
                "title": f"Alternate web service exposed on port {port}",
                "severity": "low",
                "port": port,
                "description": (
                    f"A web service appears to be reachable on TCP port "
                    f"{port}."
                ),
                "recommendation": (
                    "Confirm that the service is required and restrict "
                    "access to authorized systems."
                )
            })

        # HTTPS itself is not a vulnerability; record it as an observation.
        elif port == 443:
            findings.append({
                "category": "Web Management",
                "title": "HTTPS service detected",
                "severity": "info",
                "port": port,
                "description": (
                    "An HTTPS service is reachable."
                ),
                "recommendation": (
                    "Verify that the device uses a valid certificate and "
                    "secure TLS configuration."
                )
            })

    return findings