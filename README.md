# YARD

Internal preview. Not for distribution.

YARD is a mixed-fleet control plane for work that already happens in the building:

- **Cursor** builds the app and opens the PR.
- **Grok** ships the tagged build (canary, promote, rollback).
- **A local LLM** reads logs and heartbeats. No egress. No code. No deploy.

Humans remain product owners. Scrum-master agents cap WIP. Each domain is an agile crew with an assigned runtime.

## Surface

Open `index.html`. Tokyo Night. Keyboard first.

| key | action |
|---|---|
| `1–7` | views |
| `/` | filter |
| `j` `k` | move card |
| `return` | open |
| `esc` | close |

## Views

1. overview
2. the yard
3. crews
4. cursor build
5. grok ship
6. local watch
7. signals

## What this is not

Not a waitlist. Not a model vendor. Not a replacement for Cursor, Grok, or the box that runs the local model. It is the board those three report to.

## Status

Stealth preview. Contracts and detector rules are documented in `docs/ARCHITECTURE.md`.
