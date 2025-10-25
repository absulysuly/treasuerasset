"""
============================================================
✅ AGENT VERIFIER
Purpose: check backend (Render), Supabase DB, and frontend links.
Output:  reports/verification_report.md
============================================================
"""

import os, json, requests
from pathlib import Path

# --- Configuration -------------------------------------------------------------
BACKEND_URL = "https://hamlet-complete-mvp-2.onrender.com"
SUPABASE_URL = "https://poddahszdnnpoeiesguo.supabase.co"
SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBvZGRhaHN6ZG5ucG9laWVzZ3VvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDE3NjgxNDksImV4cCI6MjAxNzM0NDE0OX0.07WXWBuqWDt4jCB2Ox5h6G50jMZFLcA_vJN2UQ5Wb9A"
REPORT_DIR = Path("E:/HamletUnified/IraqElectinMegaMVP/reports")
REPORT_DIR.mkdir(exist_ok=True)
REPORT_FILE = REPORT_DIR / "verification_report.md"

# --- Helpers ------------------------------------------------------------------
def check_backend():
    try:
        r = requests.get(BACKEND_URL, timeout=10)
        return {"status": r.status_code, "ok": r.ok}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def check_supabase():
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        r = requests.get(f"{SUPABASE_URL}/rest/v1/candidates?select=id&limit=1", headers=headers, timeout=10)
        if r.ok:
            count_check = requests.get(f"{SUPABASE_URL}/rest/v1/candidates?select=id", headers=headers, timeout=10)
            total = len(count_check.json()) if count_check.ok else "unknown"
            return {"status": r.status_code, "ok": True, "count": total}
        return {"status": r.status_code, "ok": False}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def check_frontend():
    # This just verifies that the purple frontend build exists on Vercel
    FRONTENDS = [
        "https://iraqi-election-platform.vercel.app",
        "https://copy-of-hamlet-social.vercel.app"
    ]
    result = {}
    for url in FRONTENDS:
        try:
            r = requests.get(url, timeout=10)
            result[url] = r.status_code if r.ok else "error"
        except Exception as e:
            result[url] = f"unreachable ({e})"
    return result

# --- Run checks ---------------------------------------------------------------
print("🧩 Checking Render backend ...")
backend = check_backend()
print("🧩 Checking Supabase database ...")
supabase = check_supabase()
print("🧩 Checking Vercel frontends ...")
frontends = check_frontend()

# --- Write report -------------------------------------------------------------
lines = [
    "# 🧾 Verification Report\n",
    "## Backend (Render)\n",
    f"- URL: {BACKEND_URL}\n",
    f"- Status: {backend}\n",
    "\n## Database (Supabase)\n",
    f"- URL: {SUPABASE_URL}\n",
    f"- Candidates found: {supabase.get('count','?')}\n",
    f"- Status: {supabase}\n",
    "\n## Frontends (Vercel)\n",
]
for k,v in frontends.items():
    lines.append(f"- {k}: {v}\n")

REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"\n✅ Verification complete. Report saved to {REPORT_FILE}")
