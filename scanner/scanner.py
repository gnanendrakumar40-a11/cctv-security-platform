"""
CCTV Security Platform - Scanner Module

This module performs basic authorized network service discovery.
Use only on systems and networks you own or have permission to test.
"""

import socket


def scan_port(host, port, timeout=1):
    """Check whether a specific TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
            scanner.settimeout(timeout)
            result = scanner.connect_ex((host, port))

            if result == 0:
                return True

    except socket.error:
        return False

    return False


def scan_target(host, ports):
    """Scan a list of ports on an authorized target."""
    print(f"\nScanning authorized target: {host}")

    open_ports = []

    for port in ports:
        if scan_port(host, port):
            print(f"Port {port}: OPEN")
            open_ports.append(port)
        else:
            print(f"Port {port}: CLOSED")

    return open_ports


if __name__ == "__main__":
    target = "127.0.0.1"

    # Common ports for demonstration and authorized testing
    ports_to_scan = [80, 443, 554, 8080]

    open_ports = scan_target(target, ports_to_scan)

    print("\nScan completed.")
    print("Open ports:", open_ports)
