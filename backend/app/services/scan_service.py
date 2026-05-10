from backend.app.scanners.domain_scanner import scan_domain
from backend.app.services.ai_analyzer import analyze_security
from backend.app.services.memory_engine import detect_changes
from backend.app.repositories.scan_repository import save_scan, get_previous_scan
from backend.app.repositories.alert_repository import create_alert
from backend.app.core.logger import logger

def run_full_scan(db, *, target_id: int | None, domain: str):

    logger.info(f"Starting scan for {domain}")

    result = scan_domain(domain)

    previous = get_previous_scan(db, domain)

    changes = detect_changes(previous, result)

    # Alerts for changes (newly opened ports, etc.)
    for port in changes.get("new_ports", []):
        create_alert(
            db,
            target_id=target_id,
            domain=domain,
            message=f"⚠️ New port opened: {port}",
        )

    ai_output = analyze_security({
        "scan": result,
        "changes": changes
    })

    result["changes"] = changes
    result["ai_analysis"] = ai_output

    save_scan(db, result)

    logger.info(f"Finished scan for {domain}")

    return result
