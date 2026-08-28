from port_scanner import scan_common_ports
from device_detector import identify_device
from service_detector import detect_service
from vulnerability_checker import check_vulnerabilities
from result_builder import build_result, save_result
from security_checks import run_security_checks
from risk_scoring import calculate_risk


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
            result["service"] = service
            print(f"Port {port}: {status} - {service}")
        else:
            print(f"Port {port}: {status}")

    findings = check_vulnerabilities(results)

    security_findings = run_security_checks(results)
    findings.extend(security_findings)

    risk = calculate_risk(findings)

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

    print(f"Risk score: {risk['risk_score']}")
    print(f"Risk level: {risk['risk_level']}")

    report = build_result(
        target=target,
        device=device,
        scan_results=results,
        findings=findings
    )

    report["risk_score"] = risk["risk_score"]
    report["risk_level"] = risk["risk_level"]

    filename = save_result(report)

    print(f"Structured result saved to: {filename}")


if __name__ == "__main__":
    main()