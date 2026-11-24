"""Command-line entry point for VeriPatch prototype."""

import argparse
import json
from pathlib import Path

from .models import PatchInput, TrajectoryStep
from .pipeline import VeriPatchPipeline


def load_case(path: Path) -> PatchInput:
    raw = json.loads(path.read_text(encoding="utf-8"))
    traj = [TrajectoryStep(**s) for s in raw.get("trajectory", [])]
    return PatchInput(
        task_id=raw["task_id"],
        repo=raw["repo"],
        issue_description=raw["issue_description"],
        patch_diff=raw["patch_diff"],
        trajectory=traj,
        allowed_test_edits=raw.get("allowed_test_edits", False),
        metadata=raw.get("metadata", {}),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="VeriPatch: Reference-Free Triangulated Patch Validator")
    parser.add_argument("case_json", type=Path, help="Path to JSON file describing a test-passing patch case")
    parser.add_argument(
        "--signals",
        default="SpecCheck,ScopeCheck,TraceCheck",
        help="Comma-separated signals for factorial ablation (default: SpecCheck,ScopeCheck,TraceCheck)",
    )
    args = parser.parse_args()

    item = load_case(args.case_json)
    signals = [s.strip() for s in args.signals.split(",") if s.strip()]
    report = VeriPatchPipeline(enabled_signals=signals).evaluate(item)
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    main()
