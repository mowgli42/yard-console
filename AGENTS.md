# AGENTS.md - guide for AI coding agents

YARD is a mixed-fleet control plane console. Internal preview — not for distribution.

## Preview / verify

Open `index.html` (Tokyo Night UI, keyboard first). QML widgets (`BarWidget.qml`, `Panel.qml`), model in `YardModel.js`, package manifest in `manifest.json`, CLI in `bin/`.

```bash
python3 tests/test_plugin.py   # unittest suite: manifest, yard-status CLI, YardModel, Quickshell contracts
```

Track work in `openspec/` + Beads; screenshots in `docs/images/`.

## Secrets

Do not commit private keys, *-key.pem, *.key, .env secrets, or BEGIN … PRIVATE KEY. Generate locally; gitignore keys.
