import socket
import requests
from datetime import datetime

COMMON_PORTS = [21,22,25,53,80,443,3306,5432,6379,8080]

def check_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        return s.connect_ex((ip, port)) == 0
    except:
        return False


def scan_domain(domain: str):

    result = {
        "domain": domain,
        "ip": None,
        "open_ports": [],
        "findings": [],
        "risk_score": 0,
        "severity": "low",
        "scanned_at": str(datetime.utcnow())
    }

    try:
        ip = socket.gethostbyname(domain)
        result["ip"] = ip
    except:
        result["severity"] = "critical"
        result["findings"].append("DNS resolution failed")
        return result

    # PORT SCAN
    for port in COMMON_PORTS:
        if check_port(ip, port):
            result["open_ports"].append(port)
            result["risk_score"] += 10

    # FINDINGS ENGINE
    if 80 in result["open_ports"]:
        result["findings"].append("HTTP service exposed")
        result["risk_score"] += 15

    if 443 in result["open_ports"]:
        result["findings"].append("HTTPS service exposed")
        result["risk_score"] += 10

    if 22 in result["open_ports"]:
        result["findings"].append("SSH exposed to public network")
        result["risk_score"] += 25

    if not result["findings"]:
        result["findings"].append("No critical exposure detected")
        result["risk_score"] += 5

    # SEVERITY ENGINE
    if result["risk_score"] >= 70:
        result["severity"] = "high"
    elif result["risk_score"] >= 40:
        result["severity"] = "medium"
    else:
        result["severity"] = "low"

    result["attack_surface"] = {
        "open_ports": result["open_ports"],
        "exposed_services": len(result["open_ports"])
    }

    return result