# Miro API Setup (Zenova)

## Voraussetzungen
- Miro App mit Scopes: `boards:read`, `boards:write`
- Access Token
- Board ID

## Umgebungsvariablen
```bash
export MIRO_ACCESS_TOKEN="<dein_token>"
export MIRO_BOARD_ID="<deine_board_id>"
```

## Ausführen
```bash
python3 miro_zenova_sync.py
```

Das Script erstellt ein Frame `Zenova Funnel v1` und fügt strukturierte Sticky Notes für Headline, Subline, Proof, Diagnose-Typen, CTAs und nächste Schritte ein.
