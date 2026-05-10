from backend.app.models.scan_result import ScanResult

def get_previous_scan(db, domain):
    return db.query(ScanResult)        .filter(ScanResult.domain == domain)        .order_by(ScanResult.id.desc())        .offset(1)        .first()


def detect_changes(previous, current):
    if not previous:
        return {
            "new_ports": [],
            "removed_ports": [],
            "risk_delta": 0
        }

    prev_ports = set(previous.ports.split(",")) if previous.ports else set()
    curr_ports = set(map(str, current["open_ports"]))

    return {
        "new_ports": list(curr_ports - prev_ports),
        "removed_ports": list(prev_ports - curr_ports),
        "risk_delta": current["risk_score"] - previous.risk
    }
