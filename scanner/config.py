# Scanner configuration

SCAN_TIMEOUT = 5

COMMON_PORTS = [
    21,
    22,
    23,
    80,
    443,
    554,
    8000,
    8080
]

MAX_THREADS = 10
import ipaddress

# Authorized target scopes (Loopback, Local subnet testbeds)
AUTHORIZED_TARGETS = [
    "127.0.0.1",
    "localhost",
    "192.168.1.0/24",
    "10.0.0.0/24"
]

# Known CCTV/DVR service port mapping
STANDARD_CCTV_PORTS = {
    80: "HTTP Web Management",
    554: "RTSP Video Streaming",
    8000: "Hikvision Device Service",
    8080: "HTTP Alternate Interface",
    8081: "Embedded Web Portal",
    37777: "Dahua Management Interface"
}

def is_target_authorized(target_ip: str) -> bool:
    """
    Validates whether a target IP address falls within the approved testing scope.
    """
    if target_ip in ["127.0.0.1", "localhost"]:
        return True
    
    try:
        ip = ipaddress.ip_address(target_ip)
        for authorized in AUTHORIZED_TARGETS:
            if "/" in authorized:
                if ip in ipaddress.ip_network(authorized):
                    return True
            elif target_ip == authorized:
                return True
    except ValueError:
        return False
    
    return False
