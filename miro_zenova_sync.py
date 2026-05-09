#!/usr/bin/env python3
"""Create/update a Zenova funnel frame with sticky notes in a Miro board.

Usage:
  export MIRO_ACCESS_TOKEN=...
  export MIRO_BOARD_ID=...
  python3 miro_zenova_sync.py
"""

from __future__ import annotations

import os
import sys
import requests

API_BASE = "https://api.miro.com/v2"


def getenv_or_fail(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Missing env var: {name}")
        sys.exit(1)
    return value


def api_request(method: str, path: str, token: str, payload: dict | None = None, params: dict | None = None) -> dict:
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.request(method, url, headers=headers, json=payload, params=params, timeout=30)
    if not response.ok:
        print(f"API error {response.status_code} on {method} {path}: {response.text}")
        sys.exit(1)
    return response.json() if response.text else {}


def create_frame(board_id: str, token: str) -> dict:
    payload = {
        "data": {"title": "Zenova Funnel v1", "format": "custom"},
        "position": {"origin": "center", "x": 0, "y": 0},
        "geometry": {"width": 1800, "height": 1200},
        "style": {"fillColor": "#F5F7FB"},
    }
    return api_request("POST", f"/boards/{board_id}/frames", token, payload)


def create_sticky(board_id: str, token: str, text: str, x: int, y: int, color: str = "light_yellow") -> dict:
    payload = {
        "data": {"content": text, "shape": "square"},
        "position": {"origin": "center", "x": x, "y": y},
        "style": {"fillColor": color, "textAlign": "left", "textAlignVertical": "top"},
    }
    return api_request("POST", f"/boards/{board_id}/sticky_notes", token, payload)


def main() -> None:
    token = getenv_or_fail("MIRO_ACCESS_TOKEN")
    board_id = getenv_or_fail("MIRO_BOARD_ID")

    frame = create_frame(board_id, token)
    frame_id = frame.get("id", "<unknown>")

    notes = [
        ("Headline\nDu bekommst Kunden über Empfehlungen. Aber dein Umsatz bleibt trotzdem unplanbar?", -520, -320, "light_blue"),
        ("Subline\nMach den kostenlosen Zenova Check und erkenne in wenigen Minuten, wo dein Business aktuell Anfragen verliert.", -120, -320, "light_blue"),
        ("Proof\n29 Tage Ads · 2 Calls · 1 Close · 4'600 CHF\n30 Tage Ads · 2 Calls · 1 Close · 4'200 CHF", 280, -320, "light_green"),
        ("Diagnose-Typen\n- Sichtbarkeits-Lücke\n- Positionierungs-Lücke\n- Vertrauens-Lücke\n- System-Lücke", -520, -40, "yellow"),
        ("CTA (kalt)\nTrainingsvideo zu meinem Ergebnis ansehen", -120, -40, "yellow"),
        ("CTA (warm)\nKlarheitsgespräch anfragen", 280, -40, "orange"),
        ("Kernsatz\nEmpfehlungen sind ein Bonus. Aber nicht dein Fundament.\nZufall ist kein Business.", -520, 240, "pink"),
        ("Nächste Schritte\n1) Quiz auf 6-8 Fragen\n2) Ergebnis-Seiten stärken\n3) Follow-up je Lückentyp", -120, 240, "light_green"),
    ]

    for content, x, y, color in notes:
        create_sticky(board_id, token, content, x, y, color)

    print("Done.")
    print(f"Created frame: {frame_id}")
    print(f"Created sticky notes: {len(notes)}")


if __name__ == "__main__":
    main()
