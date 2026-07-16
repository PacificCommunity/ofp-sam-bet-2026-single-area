#!/usr/bin/env python3
"""Submit fitted BET and YFT single-area models and their Noumea diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
BASE_LAUNCHER = ROOT / "scripts" / "launch_single_area_full_diagnostics.py"
TASK = "ofp-sam-bet-yft-2026-single-area"
REPO = "PacificCommunity/ofp-sam-bet-yft-2026-single-area"
BRANCH = "BET-YFT-2026"
FLOW_GROUP = "bet-yft-2026-single-area"
NOUMEA_HOST = "nouofpsubmit.corp.spc.int"
MODELS = (
    ("BET", "01-SingleArea", "steps/01-SingleArea/model"),
    ("YFT", "02-YFT-SingleArea", "steps/02-YFT-SingleArea/model"),
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Submit BET and YFT fitted single-area runs with linked diagnostics."
    )
    parser.add_argument("--kflow-url", default="http://127.0.0.1:8089")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for species, selector, source_path in MODELS:
        command = [
            sys.executable,
            str(BASE_LAUNCHER),
            "--kflow-url", args.kflow_url,
            "--task", TASK,
            "--model-selector", selector,
            "--branch", BRANCH,
            "--flow-group", FLOW_GROUP,
            "--remote-host", NOUMEA_HOST,
            "--remote-user", "kyuhank",
            "--remote-base-dir", "/home/kyuhank/KflowOutput",
            "--submitter", "noumea",
            "--run-mode", "single_par",
            "--memory", "8GB",
            "--checks", "hessian", "profile", "jitter", "retro", "aspm",
            "--hessian-nsplit", "5",
            "--jitter-seeds", " ".join(str(value) for value in range(1, 31)),
            "--jitter-cv", "0.1",
            "--retro-peels", " ".join(str(value) for value in range(1, 7)),
            "--model-source-repo", REPO,
            "--model-source-ref", BRANCH,
            "--model-source-path", source_path,
        ]
        if args.dry_run:
            command.append("--dry-run")
        print(f"[{species}] submitting {selector}", flush=True)
        subprocess.run(command, cwd=ROOT, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
