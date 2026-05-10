# Ray-Guard

**AI-Powered Attack Surface Monitoring & Security Intelligence Platform**

Ray-Guard is a modern cybersecurity platform built to help organizations monitor exposed assets, detect infrastructure changes, assess risk, and generate AI-assisted security recommendations in real time.

Designed for speed, simplicity, and extensibility.

---

## Overview

Ray-Guard continuously monitors internet-facing targets such as:

* Domains
* Websites
* Public services
* Open ports
* Surface changes
* Security posture indicators

It combines traditional reconnaissance with AI-generated insights to help security teams move faster.

---

## Core Features

### Attack Surface Monitoring

* Domain scanning
* IP resolution
* Open port detection
* HTTP / HTTPS exposure checks
* Risk scoring engine
* Historical scan comparison

### AI Security Analysis

Integrated with Groq API to generate:

* Executive summaries
* Risk explanations
* Security recommendations
* Threat context
* Educational notes

### Alerting System

Detects changes such as:

* New ports opened
* Risk score increase
* Surface expansion
* Suspicious exposure changes

### Dashboard

Modern responsive UI with:

* Target management
* Live scan results
* KPI cards
* Alert center
* AI report panel

---

## Tech Stack

### Backend

* FastAPI
* Python 3
* SQLAlchemy
* PostgreSQL
* APScheduler

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### AI Layer

* Groq API

---

## Project Structure

```text
ray-guard/
│── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── scanners/
│   │   ├── services/
│   │   └── schemas/
│
│── index.html
│── requirements.txt
│── README.md
```

---

## Installation

## 1. Clone Project

```bash
git clone <your-repo-url>
cd ray-guard
```

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Setup PostgreSQL

Create database:

```sql
CREATE DATABASE rayguard;
```

## 5. Configure Environment

Create `.env`

```env
DATABASE_URL=postgresql://postgres:password@localhost/rayguard
GROQ_API_KEY=your_api_key_here
```

---

## Run Backend

```bash
uvicorn backend.app.main:app --reload
```

Backend available at:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Run Frontend

```bash
python3 -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

---

## API Endpoints

## Targets

```http
GET    /targets/
POST   /targets/
DELETE /targets/{id}
```

## Scanner

```http
GET /scan/{target_id}
```

## Alerts

```http
GET /alerts/
```

---

## Example Scan Output

```json
{
  "domain": "example.com",
  "ip": "93.184.216.34",
  "open_ports": [80,443],
  "risk_score": 42,
  "severity": "low",
  "ai_analysis": {
    "summary": "Minimal public exposure detected.",
    "recommendations": [
      "Maintain patching cycle",
      "Use WAF"
    ]
  }
}
```

---

## Roadmap

Planned future modules:

* Subdomain discovery
* DNS intelligence
* TLS certificate auditing
* WAF detection
* CVE mapping
* ASN intelligence
* WHOIS enrichment
* Scheduled recurring scans
* Multi-user authentication
* PDF reporting
* Slack / Email alerts
* SIEM integrations

---

## Security Notice

Ray-Guard is designed for **authorized security monitoring only**.

Use only on:

* Assets you own
* Assets you manage
* Environments where you have permission

Unauthorized scanning may violate laws or policies.

---

## Why Ray-Guard?

Most ASM tools are expensive, bloated, or closed.

Ray-Guard aims to be:

* Lightweight
* Fast
* Transparent
* AI-assisted
* Developer-friendly
* Open to customization

---

## Branding

**Ray-Guard**
Protect the surface before attackers reach it.

---

## Author

Built by independent builders focused on security innovation.

---

## License

MIT License

---
