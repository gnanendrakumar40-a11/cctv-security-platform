from port_scanner import scan_common_ports
from device_detector import detect_device


def main():
    print("CCTV Security Platform - Scanner")
    print("-" * 40)

    target = input("Enter authorized target IP or hostname: ").strip()

    if not target:
        print("No target provided.")
        return

    print(f"\nDetecting device at {target}...")

    device = detect_device(target)

    print(f"Device: {device}")

    print(f"\nScanning configured ports on {target}...\n")

    results = scan_common_ports(target)

    for result in results:
        port = result["port"]
        status = result["status"]

        print(f"Port {port}: {status}")


if __name__ == "__main__":
    main()
