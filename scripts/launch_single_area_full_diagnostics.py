#!/usr/bin/env python3
"""Submit a single-area base run with full diagnostics to Kflow (Noumea target).

Flow:
  1) Submit the single-area base model job (BET by default).
  2) Submit diagnostics against that job:
     - hessian (10-way split)
     - jitter (10 seeds; CV 0.1 by default)
     - selftest (10 replicates)
     - profile (default BET chain)
     - aspm
     - retro (6 peels)

This script does not replace the existing Kflow task registration; it only
submits jobs.  Diagnostics are submitted through
`ofp-sam-bet-2026-checks/scripts/submit_kflow_checks.py` with direct, overlay
merging enabled (default behaviour in that helper).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKS_ROOT = ROOT.parent / "ofp-sam-bet-2026-checks"
CHECKS_LAUNCH = CHECKS_ROOT / "scripts" / "submit_kflow_checks.py"
DEFAULT_MODEL = "BET"
DEFAULT_CHECK_PREFIX = "ofp-sam-bet-2026-check"
DEFAULT_TASK = "ofp-sam-bet-yft-2026-single-area"
DEFAULT_FLOW_GROUP = "bet-yft-2026-single-area"
DEFAULT_CHECKS = ["hessian", "profile", "jitter", "retro", "aspm"]
DEFAULT_HESSIAN_NSPLIT = "5"
DEFAULT_JITTER_SEEDS = " ".join(str(value) for value in range(1, 31))
DEFAULT_JITTER_CV = "0.1"
DEFAULT_SELFTEST_REPS = " ".join(str(i) for i in range(1, 11))
DEFAULT_RETRO_PEELS = " ".join(str(i) for i in range(1, 7))
DEFAULT_SUVA_HOST = "nouofpsubmit.corp.spc.int"
DEFAULT_SUVA_USER = "kyuhank"
DEFAULT_SUVA_BASE_DIR = "/home/kyuhank/KflowOutput"
DEFAULT_REF = "BET-YFT-2026"


def kflow_yaml_value(key: str, default: str = "") -> str:
    path = ROOT / "kflow.yaml"
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return default
    return match.group(1).strip().strip('"').strip("'")


def runtime_repo_packages_default() -> str:
    return os.environ.get(
        "KFLOW_REPO_RUNTIME_PACKAGES",
        kflow_yaml_value("KFLOW_REPO_RUNTIME_PACKAGES", ""),
    )


def runtime_packages_default() -> str:
    return os.environ.get(
        "KFLOW_RUNTIME_PACKAGES",
        kflow_yaml_value("KFLOW_RUNTIME_PACKAGES", "none"),
    )


def split_values(raw: str) -> list[str]:
    return [part for part in re.split(r"[\s,]+", str(raw or "").strip()) if part]


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def current_branch() -> str:
    branch = run_git("branch", "--show-current")
    if not branch:
        raise SystemExit("A checked-out branch is required for submission.")
    return branch


def api_json(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}: {detail}") from exc
    return json.loads(raw.decode("utf-8")) if raw else {}


def submit_job(base_url: str, token: str, task: str, payload: dict[str, Any]) -> dict[str, Any]:
    return api_json("POST", f"{base_url}/api/job/{task}", token, payload)


def extract_job_ref(response: dict[str, Any]) -> str:
    job = response.get("job", response)
    if not isinstance(job, dict):
        raise RuntimeError(f"Unexpected job response from Kflow: {response}")
    ref = job.get("job_number") or job.get("number") or job.get("code") or job.get("id")
    if not ref or str(ref).strip() in {"", "?"}:
        raise RuntimeError(f"Kflow response has no job reference: {job}")
    return str(ref).strip().lstrip("#")


def run_checks(
    base_url: str,
    token: str,
    base_job: str,
    model: str,
    branch: str,
    args: argparse.Namespace,
    manifest: dict[str, Any],
) -> None:
    if not CHECKS_LAUNCH.is_file():
        raise RuntimeError(
            f"Missing check launcher at {CHECKS_LAUNCH!s}; expected ofp-sam-bet-2026-checks checkout."
        )

    env = os.environ.copy()
    env.update(
        {
            "HESSIAN_NSPLIT": args.hessian_nsplit,
            "JITTER_SEEDS": args.jitter_seeds,
            "JITTER_CV": args.jitter_cv,
            "JITTER_METHOD": os.environ.get("JITTER_METHOD", "phase1_doitall"),
            "JITTER_USE_DOITALL": os.environ.get("JITTER_USE_DOITALL", "true"),
            "SELFTEST_REPS": args.selftest_reps,
            "RETRO_PEELS": args.retro_peels,
            "RETRO_USE_DOITALL": os.environ.get("RETRO_USE_DOITALL", "true"),
            "RETRO_START_STRATEGY": os.environ.get(
                "RETRO_START_STRATEGY", "auto"
            ),
            "FLOW_GROUP": args.flow_group,
            "MODEL_SOURCE_REPO": args.model_source_repo,
            "MODEL_SOURCE_REF": args.model_source_ref,
            "MODEL_SOURCE_PATH": args.model_source_path,
            "KFLOW_SUBMITTER": args.submitter,
            "KFLOW_REMOTE_HOST": args.remote_host,
            "KFLOW_REMOTE_USER": args.remote_user,
            "KFLOW_REMOTE_BASE_DIR": args.remote_base_dir,
            "ATTACH_OUTPUT_MODE": "delta",
            "KFLOW_AUTO_MERGE": "true",
            "KFLOW_AUTO_ATTACH": "true",
            "KFLOW_RUNTIME_UPDATE": os.environ.get("KFLOW_RUNTIME_UPDATE", "always"),
            "TUNA_FLOW_RUNTIME_UPDATE": os.environ.get("TUNA_FLOW_RUNTIME_UPDATE", "always"),
            "KFLOW_REPO_RUNTIME_UPDATE": os.environ.get("KFLOW_REPO_RUNTIME_UPDATE", "auto"),
            "KFLOW_RUNTIME_PACKAGES": os.environ.get(
                "KFLOW_RUNTIME_PACKAGES",
                runtime_packages_default(),
            ),
            "KFLOW_REPO_RUNTIME_PACKAGES": runtime_repo_packages_default(),
            "KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES": "true",
            "KFLOW_RUNTIME_GITHUB_AUTH": "true",
            "KFLOW_FORWARD_GITHUB_TOKEN_TO_RUNTIME": "true",
            "CHECK_COMPACT_OUTPUTS": "true",
            "CHECK_BUILD_REPORT_FIGURES": "false",
            "CHECK_ENRICH_PAYLOADS": "true",
            "CHECK_RENDER_REVIEW_HTML": "false",
        }
    )
    if args.check_profile_values:
        env["PROFILE_VALUES"] = args.check_profile_values
    if args.check_profile_preset:
        env["PROFILE_PRESET"] = args.check_profile_preset
    if args.check_profile_center:
        env["PROFILE_CENTER"] = args.check_profile_center

    cmd = [
        "python3",
        str(CHECKS_LAUNCH),
        "--kflow-url",
        args.kflow_url,
        "--task-prefix",
        args.check_task_prefix,
        "--checks",
        " ".join(args.checks),
        "--models",
        model,
        "--input-jobs",
        base_job,
        "--flow-group",
        args.flow_group,
        "--model-source-ref",
        branch,
        "--parallel-units",
        "true",
        "--auto-merge",
        "true",
        "--auto-attach",
        "true",
    ]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.dry_run:
        print("[checks] DRY-RUN command:")
        print(" ".join(cmd))
        manifest["checks"] = {"dry_run": True}
    else:
        result = subprocess.run(
            cmd,
            text=True,
            check=False,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode:
            raise RuntimeError(result.stdout.strip() or "check submission failed")
        if result.stdout:
            print(result.stdout.strip())
        manifest["checks"] = {"dry_run": False}


def submit_single_area_fit(
    base_url: str,
    token: str,
    branch: str,
    args: argparse.Namespace,
) -> str:
    model_source = "PacificCommunity/ofp-sam-bet-yft-2026-single-area"
    env = {
        "STEP_SELECT": args.model_selector,
        "RUN_MODE": args.run_mode,
        "FLOW_GROUP": args.flow_group,
        "JOB_TITLE": f"{args.model_selector} full-diagnostics rerun ({args.phase10_11})",
        "JOB_DESCRIPTION": "Run the fitted single-area PAR once, then attach the requested diagnostics.",
        "MODEL_LABEL": f"{args.model_selector} fitted model",
        "JOB_KEY": f"{args.model_selector.lower()}-fitted-final-par",
        "TRIGGER_NEXT": "false",
        "BET_FINAL_CONVERGENCE": args.phase10_11,
        "BET_PHASE10_11_CONVERGENCE": args.phase10_11,
        "KFLOW_RUNTIME_UPDATE": os.environ.get("KFLOW_RUNTIME_UPDATE", "always"),
        "TUNA_FLOW_RUNTIME_UPDATE": os.environ.get("TUNA_FLOW_RUNTIME_UPDATE", "always"),
        "KFLOW_REPO_RUNTIME_UPDATE": os.environ.get("KFLOW_REPO_RUNTIME_UPDATE", "auto"),
        "KFLOW_RUNTIME_PACKAGES": runtime_packages_default(),
        "KFLOW_REPO_RUNTIME_PACKAGES": runtime_repo_packages_default(),
        "KFLOW_RUNTIME_GITHUB_AUTH": "true",
        "KFLOW_FORWARD_GITHUB_TOKEN_TO_RUNTIME": "true",
        "KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES": "true",
        "STEPWISE_PUBLISH_REQUIRED": "false",
        "MFCL_LIVE_LOG": os.environ.get("MFCL_LIVE_LOG", "true"),
    }
    if args.frq:
        env["FRQ"] = args.frq
    payload: dict[str, Any] = {
        "repo": model_source,
        "branch": branch,
        "env": env,
        "metadata": {
            "stage": "single-area",
            "flow_group": args.flow_group,
            "model_selector": args.model_selector,
            "run_mode": args.run_mode,
        },
        "triggers": {},
        "memory": args.memory,
            "disk": "10GB",
    }
    if args.remote_host:
        payload["remote_host"] = args.remote_host
    if args.remote_user:
        payload["remote_user"] = args.remote_user
    if args.remote_base_dir:
        payload["remote_base_dir"] = args.remote_base_dir

    if args.dry_run:
        print("[fit] DRY-RUN payload:")
        print(json.dumps({"task": args.task, "payload": payload}, indent=2, sort_keys=True))
        return "DRY"

    response = submit_job(base_url, token, args.task, payload)
    job_ref = extract_job_ref(response)
    print(f"submitted fit job: {job_ref}")
    return job_ref


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kflow-url", default=os.environ.get("KFLOW_URL", "http://127.0.0.1:8089"))
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--model-selector", default=DEFAULT_MODEL)
    parser.add_argument("--frq", default="")
    parser.add_argument(
        "--input-job",
        default="",
        help="Reuse a completed fitted base job instead of submitting another base fit.",
    )
    parser.add_argument("--branch", default="")
    parser.add_argument("--flow-group", default=DEFAULT_FLOW_GROUP)
    parser.add_argument("--remote-host", default=os.environ.get("KFLOW_REMOTE_HOST", DEFAULT_SUVA_HOST))
    parser.add_argument("--remote-user", default=os.environ.get("KFLOW_REMOTE_USER", DEFAULT_SUVA_USER))
    parser.add_argument("--remote-base-dir", default=os.environ.get("KFLOW_REMOTE_BASE_DIR", DEFAULT_SUVA_BASE_DIR))
    parser.add_argument("--submitter", default=os.environ.get("KFLOW_SUBMITTER", DEFAULT_SUVA_HOST))
    parser.add_argument("--run-mode", default="single_par", help="single_par (default base fit) | doitall | job_par | ...")
    parser.add_argument("--phase10-11", default="-4", help="Legacy alias for the final doitall convergence setting.")
    parser.add_argument("--memory", default="8GB")
    parser.add_argument("--checks", nargs="+", default=DEFAULT_CHECKS)
    parser.add_argument("--check-task-prefix", default=DEFAULT_CHECK_PREFIX)
    parser.add_argument("--hessian-nsplit", default=DEFAULT_HESSIAN_NSPLIT)
    parser.add_argument("--jitter-seeds", default=DEFAULT_JITTER_SEEDS)
    parser.add_argument("--jitter-cv", default=DEFAULT_JITTER_CV)
    parser.add_argument("--selftest-reps", default=DEFAULT_SELFTEST_REPS)
    parser.add_argument("--retro-peels", default=DEFAULT_RETRO_PEELS)
    parser.add_argument("--model-source-repo", default="PacificCommunity/ofp-sam-bet-yft-2026-single-area")
    parser.add_argument("--model-source-ref", default="")
    parser.add_argument("--model-source-path", default="steps/BET")
    parser.add_argument("--check-profile-values", default="")
    parser.add_argument("--check-profile-preset", default="")
    parser.add_argument("--check-profile-center", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not split_values(" ".join(args.checks)):
        raise SystemExit("At least one check type is required.")
    args.checks = [value.lower() for value in split_values(" ".join(args.checks))]
    args.submitter = args.submitter or args.remote_host
    token = os.environ.get("KFLOW_API_TOKEN", "")
    if not args.dry_run and not token:
        raise SystemExit("Set KFLOW_API_TOKEN before submitting Kflow jobs.")
    args.branch = args.branch or current_branch()
    if not args.branch:
        raise SystemExit("A branch is required.")
    base_url = args.kflow_url.rstrip("/")
    manifest_path = ROOT / "work" / "single-area-full-diagnostics-launch.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "workflow": "single-area-full-diagnostics",
        "task": args.task,
        "branch": args.branch,
        "model_selector": args.model_selector,
        "run_mode": args.run_mode,
        "flow_group": args.flow_group,
        "checks": {"requested": args.checks},
        "submitter": {
            "host": args.submitter,
            "remote_host": args.remote_host,
            "remote_user": args.remote_user,
            "remote_base_dir": args.remote_base_dir,
        },
    }

    fit_job = args.input_job.strip().lstrip("#")
    if fit_job:
        print(f"reusing completed fit job: {fit_job}")
    else:
        fit_job = submit_single_area_fit(base_url, token, args.branch, args)
    manifest["fit_job"] = fit_job

    run_checks(
        base_url,
        token,
        fit_job,
        args.model_selector,
        args.model_source_ref or args.branch,
        args,
        manifest,
    )

    manifest["args"] = vars(args)
    manifest["status"] = "submitted" if not args.dry_run else "dry-run"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"manifest written: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
