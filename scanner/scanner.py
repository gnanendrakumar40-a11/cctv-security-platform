from port_scanner import scan_common_ports
from device_detector import identify_device
from service_detector import detect_service
from vulnerability_checker import check_vulnerabilities


def main():
    print("CCTV Security Platform - Scanner")
    print("-" * 40)

    target = input("Enter authorized target IP or hostname: ").strip()

    if not target:
        print("No target provided.")
        return

    print(f"\nScanning configured ports on {target}...\n")

    results = scan_common_ports(target)

    print("Detecting device...")

    device = identify_device(results)

    print(f"Device: {device}")

    print("\nPort scan results:")

    for result in results:
        port = result["port"]
        status = result["status"]

        if status == "open":
            service = detect_service(target, port)
            print(f"Port {port}: {status} - {service}")
        else:
            print(f"Port {port}: {status}")

    findings = check_vulnerabilities(results)

    print("\nVulnerability findings:")

    if not findings:
        print("No findings detected by the configured checks.")
    else:
        for finding in findings:
            print(
                f"[{finding['severity'].upper()}] "
                f"{finding['title']} "
                f"(port {finding['port']})"
            )
            print(f"Description: {finding['description']}")
            print(f"Recommendation: {finding['recommendation']}")
            print()


if __name__ == "__main__":
    main()