import socket
from config import COMMON_PORTS, SCAN_TIMEOUT


def scan_port(target, port):
    """Check whether a TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(SCAN_TIMEOUT)
            result = sock.connect_ex((target, port))

            if result == 0:
                return {
                    "port": port,
                    "status": "open"
                }

    except socket.gaierror:
        return {
            "port": port,
            "status": "invalid_target"
        }
    except socket.error:
        return {
            "port": port,
            "status": "error"
        }

    return {
        "port": port,
        "status": "closed"
    }


def scan_common_ports(target):
    """Scan the configured common ports."""
    results = []

    for port in COMMON_PORTS:
        results.append(scan_port(target, port))

    return results
