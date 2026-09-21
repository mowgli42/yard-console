#!/usr/bin/env python3
"""
Screenshot generator for YARD Control Plane.
Uses headless Chromium to capture high-fidelity screenshots of all console views,
modals, and multi-project beads telemetry for README and docs.
"""

import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "docs" / "images"
INDEX_URL = f"file://{BASE_DIR}/index.html"

SCREENSHOTS = [
    {
        "file": "01_overview_main.png",
        "url": f"{INDEX_URL}?view=1",
        "desc": "Overview: Fleet Summary, Agent Roster, Active Beads Ribbon",
        "size": "1400,900"
    },
    {
        "file": "02_the_yard_board.png",
        "url": f"{INDEX_URL}?view=2",
        "desc": "The Yard: 5-Column Kanban Board with test systems",
        "size": "1400,900"
    },
    {
        "file": "03_card_detail_agent_identity.png",
        "url": f"{INDEX_URL}?view=2&card=CORE-104",
        "desc": "Card Detail: Forensic Agent Telemetry & Overrun Guard",
        "size": "1400,900"
    },
    {
        "file": "04_crews_wip.png",
        "url": f"{INDEX_URL}?view=3",
        "desc": "Crews: Multi-Project Agile Domain Teams & WIP caps",
        "size": "1400,900"
    },
    {
        "file": "05_cursor_build_fleet.png",
        "url": f"{INDEX_URL}?view=4",
        "desc": "Cursor Build: Builder fleet tracking across projects",
        "size": "1400,900"
    },
    {
        "file": "06_local_watch_telemetry.png",
        "url": f"{INDEX_URL}?view=6",
        "desc": "Local Watch: Zero-Egress Heartbeat Telemetry across projects",
        "size": "1400,900"
    },
    {
        "file": "07_baseball_card_openspec.png",
        "url": f"{INDEX_URL}?project=mowgli42/appliance-keeper&bead=inWork",
        "desc": "OpenSpec Baseball Card: Appliance-Keeper living spec & BDD scenario",
        "size": "1400,900"
    },
    {
        "file": "08_baseball_card_fluffy_spoon.png",
        "url": f"{INDEX_URL}?project=mowgli42/fluffy-spoon&bead=inWork",
        "desc": "OpenSpec Baseball Card: Fluffy-Spoon recipe engine spec & BDD scenario",
        "size": "1400,900"
    },
    {
        "file": "09_baseball_card_onepage_pm.png",
        "url": f"{INDEX_URL}?project=mowgli42/OnePage-PM&bead=inWork",
        "desc": "OpenSpec Baseball Card: OnePage-PM matrix spec & BDD scenario",
        "size": "1400,900"
    }
]

def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Capturing {len(SCREENSHOTS)} screenshots using Chromium headless...")
    
    for item in SCREENSHOTS:
        out_path = IMG_DIR / item["file"]
        cmd = [
            "/usr/bin/chromium",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--virtual-time-budget=2000",
            f"--window-size={item['size']}",
            f"--screenshot={out_path}",
            item["url"]
        ]
        print(f"  → Generating {item['file']}: {item['desc']}")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"    [error] Failed: {res.stderr}")
        else:
            size_kb = out_path.stat().st_size / 1024
            print(f"    ✓ {item['file']} ({size_kb:.1f} KB)")
        time.sleep(0.5)

    print("\nAll screenshots generated successfully.")

if __name__ == "__main__":
    main()
