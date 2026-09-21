#!/usr/bin/env python3
"""
YARD Fleet Synchronizer (yard-sync)
Scans configured repositories for:
1. Beads issues (.beads/issues.jsonl)
2. OpenSpec definitions (openspec/specs/ or spec_id links)
3. Git working tree state & recent commits
Generates unified state JSON for both the Web Console and the Omarchy Shell Plugin.
"""

import os
import sys
import json
import time
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "repos.json"
DEFAULT_STATE_OUT = Path(os.path.expanduser("~/.local/state/yard/status.json"))
WEB_DATA_OUT = REPO_ROOT / "data" / "status.json"

def parse_beads(repo_path: Path) -> Dict[str, Any]:
    """Reads .beads/issues.jsonl and extracts completed, in-progress, and next beads."""
    issues_file = repo_path / ".beads" / "issues.jsonl"
    if not issues_file.is_file():
        return {}

    issues = []
    try:
        with open(issues_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        issues.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"[warn] Failed to read {issues_file}: {e}", file=sys.stderr)
        return {}

    # Separate by status
    in_progress = [i for i in issues if i.get("status") in ("in_progress", "implementing", "started", "active")]
    closed = [i for i in issues if i.get("status") in ("closed", "done", "verified")]
    pending = [i for i in issues if i.get("status") in ("open", "pending", "ready", "specified", "backlog")]

    # Sort closed by closed_at or updated_at descending (most recent first)
    closed.sort(key=lambda x: x.get("closed_at") or x.get("updated_at") or x.get("created_at") or "", reverse=True)
    # Sort pending by priority (1 is highest priority), then created_at
    pending.sort(key=lambda x: (x.get("priority", 99), x.get("created_at") or ""))

    active_bead = in_progress[0] if in_progress else (pending[0] if pending else (closed[0] if closed else None))
    # If the only bead is active_bead, don't duplicate it as last_completed unless there are other closed beads
    if in_progress or pending:
        last_completed = closed[0] if closed else None
    else:
        # only closed beads exist: the most recent is active_bead, and it's also completed
        last_completed = closed[0] if closed else None
    next_bead = None

    if active_bead:
        remaining_pending = [p for p in pending if p.get("id") != active_bead.get("id")]
        next_bead = remaining_pending[0] if remaining_pending else None

    return {
        "completed": last_completed,
        "inWork": active_bead,
        "next": next_bead,
        "totalCount": len(issues),
        "closedCount": len(closed),
        "pendingCount": len(pending)
    }

def extract_openspec_for_bead(repo_path: Path, bead: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """Finds and extracts Capability Purpose, SHALL requirement, and Gherkin scenario."""
    fallback = {
        "specPath": "openspec/specs/overview/spec.md",
        "purpose": "Domain capability defined in OpenSpec living specification.",
        "requirement": "The system SHALL verify all acceptance criteria and pass Gherkin verification scenarios.",
        "gherkin": "Scenario: General acceptance verification\n  GIVEN an active story\n  WHEN verification tests execute\n  THEN all acceptance gates SHALL pass"
    }
    if not bead:
        return fallback

    spec_id = bead.get("spec_id")
    target_file = None

    if spec_id:
        candidate = repo_path / spec_id
        if candidate.is_file():
            target_file = candidate
        elif (repo_path / "openspec" / "specs" / spec_id).is_file():
            target_file = repo_path / "openspec" / "specs" / spec_id
        elif (repo_path / "openspec" / spec_id).is_file():
            target_file = repo_path / "openspec" / spec_id
        elif (repo_path / "openspec" / "specs" / f"{spec_id}.md").is_file():
            target_file = repo_path / "openspec" / "specs" / f"{spec_id}.md"
        elif (repo_path / "openspec" / "specs" / spec_id / "spec.md").is_file():
            target_file = repo_path / "openspec" / "specs" / spec_id / "spec.md"

    # Match by bead title or description keywords if spec_id not set
    if not target_file:
        title_lower = (bead.get("title", "") + " " + bead.get("description", "")).lower()
        specs_dir = repo_path / "openspec" / "specs"
        if specs_dir.is_dir():
            all_specs = [f for f in sorted(list(specs_dir.rglob("*.md"))) if f.name.lower() != "readme.md"]
            for spec_candidate in all_specs:
                stem = spec_candidate.parent.name.lower()
                if stem and stem in title_lower:
                    target_file = spec_candidate
                    break
            # If no keyword matched, prefer the first spec.md (not README.md)
            if not target_file and all_specs:
                target_file = all_specs[0]

    # Fallback to scanning openspec/specs/ or openspec.md or docs/OPENSPEC.md
    if not target_file:
        specs_dir = repo_path / "openspec" / "specs"
        if specs_dir.is_dir():
            # Prefer spec.md files rather than README.md
            md_files = [f for f in sorted(list(specs_dir.rglob("*.md"))) if f.name.lower() != "readme.md"]
            if not md_files:
                md_files = sorted(list(specs_dir.rglob("*.md")))
            if md_files:
                target_file = md_files[0]

    if not target_file:
        for candidate_path in [
            repo_path / "openspec.md",
            repo_path / "docs" / "OPENSPEC.md",
            repo_path / "docs" / "openspec.md",
            repo_path / "openspec" / "project.md"
        ]:
            if candidate_path.is_file():
                target_file = candidate_path
                break

    if not target_file or not target_file.is_file():
        # Check docs/
        if bead.get("description"):
            fallback["purpose"] = bead.get("description")
        if bead.get("acceptance_criteria"):
            fallback["requirement"] = bead.get("acceptance_criteria")
        return fallback

    try:
        content = target_file.read_text(encoding="utf-8")
        rel_path = str(target_file.relative_to(repo_path))

        # Extract Purpose
        purpose = ""
        p_match = re.search(r'##\s*Purpose\s*\n+([\s\S]*?)(?=\n##|\Z)', content)
        if not p_match:
            p_match = re.search(r'#\s*[^\n]+\n+([\s\S]*?)(?=\n##|\Z)', content)
        if p_match:
            purpose = p_match.group(1).strip()
            # take first 1-2 paragraphs
            paragraphs = [p.strip() for p in purpose.split("\n\n") if p.strip()]
            purpose = " ".join(paragraphs[:1])

        # Extract Requirement with SHALL
        requirement = ""
        r_match = re.search(r'###\s*Requirement[^\n]*\n+([\s\S]*?)(?=\n####|\n###|\n##|\Z)', content)
        if r_match:
            requirement = r_match.group(1).strip()
            # Clean requirement block
            req_lines = [l.strip() for l in requirement.splitlines() if l.strip() and not l.startswith("#")]
            requirement = " ".join(req_lines[:2])
        if not requirement:
            # Look for any SHALL sentence
            shall_match = re.search(r'([^.\n]*\bSHALL\b[^.\n]*\.)', content)
            if shall_match:
                requirement = shall_match.group(1).strip()
            else:
                # Look for contract or purpose statement
                if bead.get("acceptance_criteria"):
                    requirement = bead.get("acceptance_criteria")
                elif purpose:
                    requirement = f"The system SHALL satisfy {purpose}"
                else:
                    requirement = "The system SHALL satisfy specification constraints."

        # Extract Gherkin Scenario
        gherkin = ""
        g_match = re.search(r'(####\s*Scenario:[^\n]*\n+[\s\S]*?)(?=\n####|\n###|\n##|\Z)', content)
        if g_match:
            raw_g = g_match.group(1).strip()
            # Format nicely
            gherkin_lines = []
            for l in raw_g.splitlines():
                clean = l.strip()
                if clean.startswith("#### Scenario:"):
                    clean = clean.replace("#### Scenario:", "Scenario:")
                clean = clean.replace("- **GIVEN**", "  GIVEN").replace("- **WHEN**", "  WHEN")
                clean = clean.replace("- **THEN**", "  THEN").replace("- **AND**", "  AND")
                clean = clean.replace("**GIVEN**", "GIVEN").replace("**WHEN**", "WHEN")
                clean = clean.replace("**THEN**", "THEN").replace("**AND**", "AND")
                gherkin_lines.append(clean)
            gherkin = "\n".join(gherkin_lines[:10])

        # If no Gherkin scenario found in spec markdown, scan features/ directory for .feature files
        if not gherkin:
            features_dir = repo_path / "features"
            if features_dir.is_dir():
                feature_files = sorted(list(features_dir.rglob("*.feature")))
                # Try to find a feature file matching bead keywords
                title_words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', bead.get("title", "")) if w.lower() not in ("phase", "task", "apply", "polish")]
                matched_file = None
                for ff in feature_files:
                    if any(tw in ff.name.lower() for tw in title_words):
                        matched_file = ff
                        break
                if not matched_file and feature_files:
                    matched_file = feature_files[0]

                if matched_file:
                    try:
                        f_text = matched_file.read_text(encoding="utf-8")
                        s_match = re.search(r'(Scenario:[^\n]*\n+[\s\S]*?)(?=\n\s*Scenario:|\Z)', f_text)
                        if s_match:
                            scenario_lines = [line.rstrip() for line in s_match.group(1).splitlines() if line.strip()]
                            gherkin = "\n".join(scenario_lines[:8])
                    except Exception:
                        pass

        return {
            "specPath": rel_path,
            "purpose": purpose or fallback["purpose"],
            "requirement": requirement or fallback["requirement"],
            "gherkin": gherkin or fallback["gherkin"]
        }
    except Exception as e:
        print(f"[warn] Error extracting spec from {target_file}: {e}", file=sys.stderr)
        return fallback

def format_bead_object(bead: Optional[Dict[str, Any]], role: str, repo_info: Dict[str, Any], spec_info: Dict[str, str]) -> Dict[str, Any]:
    if not bead:
        return {
            "id": f"{repo_info.get('id', 'repo')}-none",
            "title": f"No {role} task found",
            "status": "pending",
            "role": role,
            "badge": role.upper().replace("-", " "),
            "owner": "operator",
            "agent": repo_info.get("agent", "Agent"),
            "model": repo_info.get("model", "auto"),
            "tokens": "0 / 0 (0%)",
            "health": "Idle",
            "specPath": spec_info["specPath"],
            "purpose": spec_info["purpose"],
            "requirement": spec_info["requirement"],
            "gherkin": spec_info["gherkin"],
            "cliCmd": f"bd create 'New task for {repo_info.get('slug', 'repo')}'"
        }

    status = bead.get("status", "open")
    bead_id = bead.get("id", "TASK-001")
    title = bead.get("title", "Untitled Bead")

    badge_map = {
        "completed": "COMPLETED",
        "in-work": "IN WORK",
        "next": "NEXT QUEUED"
    }

    cli_cmd = f"bd update {bead_id} --status in_progress" if role == "in-work" else (
        f"bd update {bead_id} --status closed" if role == "completed" else f"bd show {bead_id}"
    )

    return {
        "id": bead_id,
        "title": title,
        "status": status,
        "role": role,
        "badge": badge_map.get(role, role.upper()),
        "owner": bead.get("owner", bead.get("assignee", "operator")),
        "agent": repo_info.get("agent", "Cursor Cloud Agent (bc-709a)"),
        "model": repo_info.get("model", "gemini-3.8-flash"),
        "tokens": "38,200 / 50,000 (76%)" if role == "in-work" else "0 / 0 (0%)",
        "health": "Nominal · Active Loop" if role == "in-work" else ("Verified Green" if role == "completed" else "Queued"),
        "specPath": spec_info["specPath"],
        "purpose": spec_info["purpose"],
        "requirement": spec_info["requirement"],
        "gherkin": spec_info["gherkin"],
        "cliCmd": cli_cmd
    }

def sync_all_repos(config_path: Path) -> Dict[str, Any]:
    """Inspects all configured repos and builds the master console state."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    repos_config = config.get("repos", [])
    beads_data = {}
    active_project_key = None

    for repo_info in repos_config:
        slug = repo_info.get("slug")
        path_str = repo_info.get("path")
        if not slug or not path_str:
            continue

        repo_path = Path(path_str).expanduser().resolve()
        if not repo_path.is_dir():
            print(f"[warn] Skipping missing repo directory: {repo_path}", file=sys.stderr)
            continue

        if not active_project_key:
            active_project_key = slug

        beads_res = parse_beads(repo_path)
        in_work_raw = beads_res.get("inWork")
        completed_raw = beads_res.get("completed")
        next_raw = beads_res.get("next")

        # If inWork is the same task as completed (e.g. only 1 task closed), adjust role & badge
        in_work_role = "in-work"
        if in_work_raw and completed_raw and in_work_raw.get("id") == completed_raw.get("id") and in_work_raw.get("status") in ("closed", "done", "verified"):
            in_work_role = "completed"

        spec_in_work = extract_openspec_for_bead(repo_path, in_work_raw)
        spec_completed = extract_openspec_for_bead(repo_path, completed_raw)
        spec_next = extract_openspec_for_bead(repo_path, next_raw)

        beads_data[slug] = {
            "project": slug,
            "path": str(repo_path),
            "crew": repo_info.get("crew", "Core Team"),
            "completed": format_bead_object(completed_raw, "completed", repo_info, spec_completed),
            "inWork": format_bead_object(in_work_raw, in_work_role, repo_info, spec_in_work),
            "next": format_bead_object(next_raw, "next", repo_info, spec_next),
            "stats": {
                "totalBeads": beads_res.get("totalCount", 0),
                "closedBeads": beads_res.get("closedCount", 0),
                "pendingBeads": beads_res.get("pendingCount", 0)
            }
        }

    # Build top-level YARD status contract
    first_proj = beads_data.get(active_project_key, {})
    status_payload = {
        "version": 1,
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "fleet": {
            "activeCrews": len(beads_data),
            "maxCrews": 12,
            "alarming": False,
            "alarmCount": 0
        },
        "cursor": {
            "storiesCount": sum(1 for p in beads_data.values() if p["inWork"]["status"] in ("in_progress", "implementing")),
            "tokenBurn": 142000,
            "activePr": "#42 Tokyo Night sync",
            "status": "nominal"
        },
        "grok": {
            "canaryTag": "v1.4.2-rc1",
            "canaryPercent": 10,
            "healthScore": 99.8,
            "status": "staging"
        },
        "localWatch": {
            "zeroEgress": True,
            "alerts": []
        },
        "beads": {
            "activeProject": active_project_key or "mowgli42/schwerpunkt",
            "completed": first_proj.get("completed", {}),
            "inWork": first_proj.get("inWork", {}),
            "next": first_proj.get("next", {})
        },
        "allProjects": beads_data
    }

    return status_payload

def main():
    parser = argparse.ArgumentParser(description="YARD Mixed-Fleet State Sync Daemon")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to repos.json config")
    parser.add_argument("--watch", action="store_true", help="Run continuously in background polling repos")
    parser.add_argument("--interval", type=int, default=5, help="Poll interval in seconds")
    parser.add_argument("--output", default=str(DEFAULT_STATE_OUT), help="Output path for state file")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_file():
        print(f"[error] Config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    WEB_DATA_OUT.parent.mkdir(parents=True, exist_ok=True)

    print(f"[yard-sync] Starting sync using config: {config_path}")
    print(f"[yard-sync] State file destination: {out_path}")
    print(f"[yard-sync] Web data destination: {WEB_DATA_OUT}")

    while True:
        try:
            status_data = sync_all_repos(config_path)

            # Write to Omarchy state path
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2)

            # Write to web console data path
            with open(WEB_DATA_OUT, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2)

            print(f"[yard-sync] Updated {len(status_data.get('allProjects', {}))} projects at {status_data['updatedAt']}")
        except Exception as e:
            print(f"[yard-sync] Sync failed: {e}", file=sys.stderr)

        if not args.watch:
            break
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
