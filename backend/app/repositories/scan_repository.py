from backend.app.models.scan_result import ScanResult

def save_scan(db, result):
    row = ScanResult(
        domain=result["domain"],
        ip=result["ip"],
        ports=",".join(map(str, result["open_ports"])),
        risk=result["risk_score"]
    )
    db.add(row)
    db.commit()
    return row


def get_previous_scan(db, domain):
    return db.query(ScanResult)        .filter(ScanResult.domain == domain)        .order_by(ScanResult.id.desc())        .offset(1)        .first()
