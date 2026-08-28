from port_scanner import scan_common_ports
from device_detector import identify_device
from service_detector import detect_service


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


if __name__ == "__main__":
    main()