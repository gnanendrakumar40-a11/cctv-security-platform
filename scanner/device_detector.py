def identify_device(open_ports):
    """Identify a possible device type from open ports."""

    ports = [
        result["port"]
        for result in open_ports
        if result["status"] == "open"
    ]

    if 554 in ports:
        return "Possible CCTV camera or RTSP-enabled device"

    if 80 in ports or 443 in ports:
        return "Possible web-managed device"

    if 8000 in ports or 8080 in ports:
        return "Possible DVR, NVR, or web service"

    return "Unknown device"
