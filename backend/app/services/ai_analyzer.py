import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=_api_key) if _api_key else None


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1]
        if t.endswith("```"):
            t = t.rsplit("\n", 1)[0]
    return t.strip()

def analyze_security(scan_result):
    if not client:
        return {
            "summary": "AI disabled (missing GROQ_API_KEY)",
            "recommendations": [],
        }

    prompt = f"""
You are a cybersecurity analyst.

Analyze this security scan + changes:

{scan_result}

RULES:
- Explain CURRENT risk
- Explain WHAT CHANGED from previous scan
- Highlight new threats
- Give mitigation steps
- Output JSON ONLY
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a strict JSON security analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    # safety parse (biar backend gak crash)
    try:
        cleaned = _strip_code_fences(content)
        return json.loads(cleaned)
    except Exception:
        # fallback: return raw text so frontend still has something to show
        return content
