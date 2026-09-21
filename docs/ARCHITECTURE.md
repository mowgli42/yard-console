# YARD architecture

Internal. Do not circulate.

## Runtime split

| runtime | allowed | forbidden |
|---|---|---|
| cursor | implement story, tests, PR text, domain pack | prod credentials, cluster mutate, raw log firehose |
| grok | tag, canary, promote, rollback, operator note from diff | reopen product brief, invent secrets, swallow the log stream |
| local llm | classify journald / CI logs / token curves / heartbeats | write code, ship, egress, see customer payloads |

A story is done when the product owner accepts and watch is quiet.

## Crews

Each domain is an agile team.

- Product owner: named human. Goal, glossary, accept.
- Scrum master: agent. WIP cap, impediments, cycle time.
- Developers: runtime-assigned agents.
- Counterpart: ship crew on the tag, watch crew on the live session.

WIP is capped per crew, not by a global "in progress" column.

## Knowledge

Each crew carries a pack:

- `DOMAIN.md` — in / out of scope, escalation
- glossary — ubiquitous language, never mixed across crews
- golden eval set — must stay green before grok may promote
- budget file — expected tokens and wall-clock by story type

Cursor sees root rules + its crew pack. Grok sees the tag contract. Local watch sees detector rules only.

## Detectors (local)

- timeout by story type
- cloud token 2× flag / 4× hard stop
- zero-error + high tokens
- repeated tool signature ≥ 3
- goal drift < 0.60 vs the sprint item
- no artifact while the clock runs
- heartbeat stale at 2× mean step

Local watch raises a card. It does not apply the fix.

## Pipeline

```
cursor PR
  → lint + cheap eval subset
  → merge
  → image tag (sha + prompt hash + eval snapshot)
grok
  → canary
  → promote or rollback
local
  → live loop / heartbeat / retry-storm pass
  → card on the yard board
```

## Why three runtimes

Coding agents are the wrong process to push production and the wrong process to read raw logs. Shipping agents should not reopen the brief. Log triage should not leave the box or spend cloud tokens on noise. YARD is the contract that keeps those jobs apart.
