import socket


def detect_service(host, port, timeout=1):
    """Identify common services running on a specific port."""

    common_services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
    }

    service = common_services.get(port)

    if service:
        return service

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "Unknown service"
    except socket.timeout:
        return "No response"
    except socket.error:
        return "Unavailable"
