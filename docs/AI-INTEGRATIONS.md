# YARD AI Tools Integration Matrix & Extension Points

YARD serves as the central control plane for mixed-fleet agentic engineering. Rather than competing with specialized tools, YARD defines contracts, telemetry taps, and gating mechanisms that orchestrate external AI systems.

---

## 1. Primary Fleet Runtime Profiles

| AI Tool / Runtime | Primary YARD Role | Protocols / Ingestion | Permitted Actions | Forbidden Actions |
|---|---|---|---|---|
| **Cursor** (Cloud / Local) | **Code Construction & Test Generation** | GitHub App Webhooks, Cursor Agent CLI / MCP Server, Git Branch metadata | Implement stories, create unit/integration tests, generate PR descriptions, update domain documentation | Mutate production clusters, access prod secrets, read raw live log firehoses |
| **Grok (xAI)** | **Release, Verification & Deployment** | xAI API, GitHub Actions dispatch, Webhook triggers | Tag release artifacts, trigger canaries, evaluate canary metrics, execute promote or rollback | Reopen product brief, invent new environment secrets, swallow unparsed raw logs |
| **Local LLMs** (vLLM, Ollama, llama.cpp, Qwen 2.5 / DeepSeek R1 14B) | **On-Premise Watch & Anomaly Detection** | Unix Domain Sockets, Local REST (`/v1/chat/completions`), Journald streaming | Classify journald logs, parse agent heartbeats, calculate token curve slopes, raise board cards | Write source code, execute deployments, egress data off-box, access customer payloads |
| **Claude Code** (Anthropic) | **Alternative Builder / Refactoring Crew** | CLI transcripts (`~/.claude/projects`), OAuth usage API, MCP servers | Architectural refactoring, multi-file code editing, local test execution | Direct deployment without Grok gatekeeper review |
| **OpenCode / Codex** | **Specialized Subagent / Script Generator** | Codex app-server RPC, native session JSONL records | Generate migration scripts, repetitive fixture generation | Unbounded autonomous network loops |
| **Antigravity CLI (`agy`) / Gemini** | **Fast Exploration & Code Review** | Google GenAI SDK, local CLI stdio JSON | Quick exploration, semantic diff review, AST validation | Production credential handling |

---

## 2. MCP (Model Context Protocol) Integration Points

YARD acts as both an **MCP Server** (exposing board state to agents) and an **MCP Client/Gateway** (bridging external tools into the control plane).

### 2.1 YARD as MCP Server (`yard-mcp-server`)
Exposes tools to Cursor, Claude, or Grok sessions:
- `yard_get_active_story(crew_id)`: Fetches the current story, acceptance criteria, and domain pack.
- `yard_report_progress(story_id, tokens_spent, step_name)`: Emits heartbeat and token telemetry to the local watcher.
- `yard_check_wip(crew_id)`: Verifies if the crew has capacity to pick up an additional task.
- `yard_submit_pr(story_id, pr_url, diff_summary)`: Registers a completed PR and transitions story to `verification`.

### 2.2 YARD as MCP Bridge to Local Services
Bridges local monitoring infrastructure to the YARD detector engine:
- **Systemd Journald MCP:** Feeds local container and system logs into the local LLM classifier.
- **Git State MCP:** Inspects branch diffs for goal drift evaluation against the active sprint brief.
- **Process & Resource MCP:** Tracks CPU, memory, and token velocity of running agent processes.

---

## 3. Telemetry Ingestion Architecture

```
┌────────────────────────────────────────────────────────┐
│                   AI TOOLS & AGENTS                    │
│   Cursor Cloud Agent   Claude Code     Grok Release   │
└───────────┬───────────────────┬──────────────┬─────────┘
            │                   │              │
            ▼                   ▼              ▼
   [Git & PR Webhooks]  [Session Logs]   [Canary Hooks]
            │                   │              │
            └─────────────┬─────┴──────────────┘
                          ▼
             ┌─────────────────────────┐
             │  YARD Ingestion Engine  │
             │  (Heartbeat & Tokens)   │
             │  Local Socket / REST    │
             └────────────┬────────────┘
                          │
                          ▼
             ┌─────────────────────────┐
             │   Local LLM Classifier  │
             │   (Ollama / llama.cpp)  │
             │   *Strict Zero Egress*  │
             └────────────┬────────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
  ┌─────────────────────┐   ┌───────────────────────────┐
  │  YARD Board Card    │   │  Omarchy Desktop Alert    │
  │  (Signals & Yard)   │   │  (Bar Badge & OSD Toast)  │
  └─────────────────────┘   └───────────────────────────┘
```

---

## 4. Detector Contracts for AI Tooling

### Detector 1: Token Burn & Velocity Ceiling
- **Trigger:** Token burn rate exceeds $2\times$ the story class baseline (e.g. >100k tokens for a small refactor) or velocity exceeds 5,000 tokens/min without a git commit.
- **Action:** Advisory flag (Yellow). At $4\times$, issue process freeze / hard stop (Red).

### Detector 2: Identical Tool Signature Loops
- **Trigger:** An agent repeats identical tool invocation parameters $\ge 3$ times (e.g. repeated failing search queries or failing test runs without code edits).
- **Action:** Anomaly card created on view 7 (`signals`).

### Detector 3: Semantic Goal Drift
- **Trigger:** Vector cosine similarity between story `DOMAIN.md` intent and commit diff embedding drops below `0.60`.
- **Action:** Goal drift warning raised; requires human PO acknowledgment before Grok can canary.

### Detector 4: Zombie / Stale Heartbeat
- **Trigger:** Agent process alive but no progress packet received for $>2\times$ average step interval.
- **Action:** Bar badge lights up with urgent indicator; card marked `stale`.
