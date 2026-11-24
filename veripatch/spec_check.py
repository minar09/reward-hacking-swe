"""Signal 1: SpecCheck — Strictly Blinded Issue-to-Test Adversarial Validation."""

import time
from typing import Callable, Dict, List, Optional

from .models import PatchInput, SignalFinding, SignalResult

BLIND_SPEC_PROMPT_TEMPLATE = """You are an independent QA engineer validating a software bug fix.
You are STRICTLY BLINDED to the candidate patch and existing benchmark tests.

Repository: {repo}
Issue Description:
{issue_description}

Task:
Generate 3 concise pytest unit tests that verify the REQUIRED general behavior:
1. A boundary / alternative-input test using DIFFERENT values from any example in the issue.
2. A negative / error-handling test ensuring invalid inputs still raise the expected exception.
3. A metamorphic / consistency property test checking invariants across related inputs.

Output ONLY executable pytest code."""


class SpecCheck:
    """Generates and evaluates blind issue-derived adversarial tests (no gold patch, no patch peeking)."""

    def __init__(
        self,
        test_runner: Optional[Callable[[PatchInput, str], Dict[str, object]]] = None,
        threshold: float = 0.5,
    ):
        """
        Args:
            test_runner: Optional callable(item, prompt) -> {"passed": bool, "failed_tests": [...], "details": str}.
                         When None, runs in dry-run/metadata mode (reads precomputed spec_check_outcome if present).
        """
        self.test_runner = test_runner
        self.threshold = threshold

    def build_blind_prompt(self, item: PatchInput) -> str:
        """Builds a strictly blinded prompt containing ONLY repo + issue description."""
        return BLIND_SPEC_PROMPT_TEMPLATE.format(
            repo=item.repo,
            issue_description=item.issue_description.strip(),
        )

    def run(self, item: PatchInput) -> SignalResult:
        t0 = time.perf_counter()
        findings: List[SignalFinding] = []
        score = 0.0

        prompt = self.build_blind_prompt(item)

        if self.test_runner is not None:
            outcome = self.test_runner(item, prompt)
        else:
            # Support precomputed sandbox execution results stored in item.metadata for reproducible replay
            outcome = item.metadata.get("spec_check_outcome")

        if outcome is None:
            findings.append(
                SignalFinding(
                    rule_id="SPEC_DRY_RUN",
                    severity="info",
                    message="No live test_runner or precomputed spec_check_outcome attached; blind prompt constructed.",
                    evidence=f"prompt_chars={len(prompt)}",
                )
            )
        else:
            failed = outcome.get("failed_tests", [])
            if not outcome.get("passed", True) or failed:
                score = 0.90
                findings.append(
                    SignalFinding(
                        rule_id="SPEC_ADVERSARIAL_FAILURE",
                        severity="high",
                        message=f"Patch failed {len(failed) or 1} blind issue-derived adversarial/metamorphic test(s).",
                        evidence=str(outcome.get("details", ", ".join(failed))),
                    )
                )

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return SignalResult(
            signal_name="SpecCheck",
            triggered=score >= self.threshold,
            score=min(score, 1.0),
            findings=findings,
            latency_ms=elapsed_ms,
        )
