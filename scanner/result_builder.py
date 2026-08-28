import json


def build_result(target, device, scan_results, findings):
    """Build a structured scan result."""

    ports = []

    for result in scan_results:
        port_data = {
            "port": result["port"],
            "status": result["status"]
        }

        if result["status"] == "open":
            # Service is added by scanner.py before this function is called.
            port_data["service"] = result.get("service", "Unknown")

        ports.append(port_data)

    return {
        "target": target,
        "device": device,
        "ports": ports,
        "findings": findings
    }


def save_result(result, filename="scan_result.json"):
    """Save scan result as a JSON file."""

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    return filename