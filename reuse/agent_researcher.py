"""
============================================================
🔍 AGENT RESEARCHER
Purpose: Scan your local repositories and collect reusable
         assets for the Iraq Election Mega MVP.
============================================================
"""

import os
import json
from pathlib import Path

# --- Configuration
ROOT_DIR = Path("E:/HamletUnified")
TARGET_DIR = ROOT_DIR / "IraqElectinMegaMVP"
REPORTS_DIR = TARGET_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

REPOSITORIES = [
    "hamlet-complete-mvp",
    "asset-completeredrive",
    "Copy-of-Hamlet-social",
]

SCAN_TARGETS = ["components", "api", "services", "schemas", "data", "pages"]

reuse_manifest = {
    "frontend_components": [],
    "backend_services": [],
    "data_assets": [],
    "schemas": [],
}

print("🔍 Scanning repositories for reusable assets...\n")

for repo in REPOSITORIES:
    repo_path = ROOT_DIR / repo
    if not repo_path.exists():
        print(f"⚠️ Repo not found: {repo}")
        continue

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            lower = file.lower()
            full_path = os.path.join(root, file)
            # Categorize files by purpose
            if "component" in root.lower() or lower.endswith(".tsx"):
                reuse_manifest["frontend_components"].append(full_path)
            elif "api" in root.lower() or lower.endswith(".py") or lower.endswith(".ts"):
                reuse_manifest["backend_services"].append(full_path)
            elif "schema" in root.lower() or lower.endswith(".prisma") or lower.endswith(".sql"):
                reuse_manifest["schemas"].append(full_path)
            elif "data" in root.lower() or lower.endswith(".csv") or lower.endswith(".json"):
                reuse_manifest["data_assets"].append(full_path)

print("\n✅ Scan complete!")

# --- Save manifest
manifest_path = REPORTS_DIR / "reuse_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(reuse_manifest, f, indent=2)

summary = {
    "frontend_components": len(reuse_manifest["frontend_components"]),
    "backend_services": len(reuse_manifest["backend_services"]),
    "data_assets": len(reuse_manifest["data_assets"]),
    "schemas": len(reuse_manifest["schemas"]),
}
summary_path = REPORTS_DIR / "research_summary.json"
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"""
🧾 Summary:
  - Frontend components: {summary['frontend_components']}
  - Backend services:    {summary['backend_services']}
  - Data assets:          {summary['data_assets']}
  - Schemas:              {summary['schemas']}

📄 Reports saved to:
  {manifest_path}
  {summary_path}
""")
