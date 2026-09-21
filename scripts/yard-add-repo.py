#!/usr/bin/env python3
"""
Add Repository to YARD Fleet (yard-add-repo)
Usage:
  ./scripts/yard-add-repo.py /path/to/repo --crew "Crew Name" --agent "Cursor Cloud" --model "gemini-3.8-flash"
  ./scripts/yard-add-repo.py --new /path/to/new-repo --init-beads --init-openspec
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = REPO_ROOT / "config" / "repos.json"

def detect_git_slug(repo_path: Path) -> str:
    """Extracts git origin remote slug if available, else directory name."""
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_path), "config", "--get", "remote.origin.url"],
            capture_output=True, text=True, check=True
        )
        url = res.stdout.strip()
        if "github.com:" in url:
            return url.split("github.com:")[1].replace(".git", "")
        elif "github.com/" in url:
            return url.split("github.com/")[1].replace(".git", "")
    except Exception:
        pass
    return f"local/{repo_path.name}"

def init_beads(repo_path: Path, slug: str):
    """Initializes a .beads directory with sample starter bead."""
    beads_dir = repo_path / ".beads"
    beads_dir.mkdir(parents=True, exist_ok=True)
    issues_file = beads_dir / "issues.jsonl"
    config_file = beads_dir / "config.yaml"

    if not config_file.exists():
        config_file.write_text(f"# Beads config for {slug}\nissue-prefix: {repo_path.name}\nno-db: true\n", encoding="utf-8")

    if not issues_file.exists() or issues_file.stat().st_size == 0:
        sample_bead = {
            "_type": "issue",
            "id": f"{repo_path.name}-001",
            "title": f"Initial repository baseline & OpenSpec verification for {slug}",
            "description": "Baseline repository setup and verification of OpenSpec living specifications.",
            "acceptance_criteria": "Project builds, unit tests pass, and initial capability requirements are specified.",
            "status": "in_progress",
            "priority": 1,
            "issue_type": "task",
            "owner": os.getenv("USER", "operator"),
            "created_at": "2026-09-21T10:00:00Z"
        }
        with open(issues_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(sample_bead) + "\n")
        print(f"[init] Created starter bead in {issues_file}")

def init_openspec(repo_path: Path, slug: str):
    """Initializes openspec/ directory with project index and starter capability spec."""
    openspec_dir = repo_path / "openspec"
    specs_dir = openspec_dir / "specs" / "core-capability"
    specs_dir.mkdir(parents=True, exist_ok=True)

    project_md = openspec_dir / "project.md"
    if not project_md.exists():
        project_md.write_text(f"""# {repo_path.name} — Project Context & Specification Index

## Purpose
Domain implementation for {slug}.

## Specifications Index
| Capability | Spec Path | Description |
|---|---|---|
| Core Capability | `openspec/specs/core-capability/spec.md` | Primary domain requirements and verification gates. |
""", encoding="utf-8")

    spec_md = specs_dir / "spec.md"
    if not spec_md.exists():
        spec_md.write_text(f"""# Core Capability Specification for {repo_path.name}

## Purpose
Define the primary capability contract and verification criteria for {slug}.

## Requirements

### Requirement: Domain Verification Contract
The service SHALL execute core domain logic and emit deterministic output without unhandled errors.

#### Scenario: Clean execution baseline
- **GIVEN** a nominal environment configuration
- **WHEN** the primary service starts
- **THEN** it SHALL report healthy status
- **AND** emit zero fatal errors
""", encoding="utf-8")
        print(f"[init] Created starter OpenSpec spec in {spec_md}")

def main():
    parser = argparse.ArgumentParser(description="Add an existing or new repository to YARD Fleet")
    parser.add_argument("repo_path", help="Absolute or relative path to the repository directory")
    parser.add_argument("--slug", help="GitHub or repository slug (e.g. owner/repo-name)")
    parser.add_argument("--crew", default="Core Engineering", help="Crew name assigned to this domain")
    parser.add_argument("--runtime", default="Cursor", choices=["Cursor", "Grok", "Local LLM"], help="Primary runtime")
    parser.add_argument("--agent", default="Cursor Cloud Agent (bc-709a)", help="Assigned agent identification")
    parser.add_argument("--model", default="gemini-3.8-flash", help="Underlying foundation model")
    parser.add_argument("--new", action="store_true", help="Initialize directory as a new git repository if not existing")
    parser.add_argument("--init-beads", action="store_true", help="Initialize .beads directory if missing")
    parser.add_argument("--init-openspec", action="store_true", help="Initialize openspec/ directory if missing")

    args = parser.parse_args()
    target_path = Path(args.repo_path).expanduser().resolve()

    if args.new and not target_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(target_path), "init"], check=True)
        print(f"[ok] Initialized new git repository at {target_path}")

    if not target_path.is_dir():
        print(f"[error] Repository path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)

    slug = args.slug or detect_git_slug(target_path)

    if args.init_beads or not (target_path / ".beads").exists():
        init_beads(target_path, slug)

    if args.init_openspec or not (target_path / "openspec").exists():
        init_openspec(target_path, slug)

    # Read current config
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {"repos": [], "pollIntervalSec": 5}

    repos = config.get("repos", [])
    # Check if already registered
    existing = next((r for r in repos if r.get("path") == str(target_path) or r.get("slug") == slug), None)
    if existing:
        existing.update({
            "slug": slug,
            "path": str(target_path),
            "crew": args.crew,
            "runtime": args.runtime,
            "agent": args.agent,
            "model": args.model
        })
        print(f"[ok] Updated existing registration for {slug}")
    else:
        repos.append({
            "id": target_path.name,
            "slug": slug,
            "path": str(target_path),
            "crew": args.crew,
            "runtime": args.runtime,
            "agent": args.agent,
            "model": args.model
        })
        print(f"[ok] Added {slug} to YARD fleet registry")

    config["repos"] = repos
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Run immediate sync
    sync_script = SCRIPT_DIR / "yard-sync.py"
    if sync_script.is_file():
        subprocess.run([sys.executable, str(sync_script)], check=True)

    print("\n[success] Repository successfully linked to YARD!")
    print(f"  • Slug:    {slug}")
    print(f"  • Path:    {target_path}")
    print(f"  • Crew:    {args.crew}")
    print(f"  • Runtime: {args.runtime} ({args.model})")

if __name__ == "__main__":
    main()
