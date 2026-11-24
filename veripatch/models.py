"""Core data structures for VeriPatch."""

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Verdict(str, Enum):
    VERIFIED_PASS = "VERIFIED_PASS"
    ESCALATE = "ESCALATE"
    LIKELY_HACK = "LIKELY_HACK"


@dataclass
class TrajectoryStep:
    step_id: int
    action: str  # e.g., "read_file", "run_command", "edit_file"
    target: str  # file path or command string
    output_snippet: str = ""


@dataclass
class PatchInput:
    task_id: str
    repo: str
    issue_description: str
    patch_diff: str
    trajectory: List[TrajectoryStep] = field(default_factory=list)
    allowed_test_edits: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignalFinding:
    rule_id: str
    severity: str  # "info", "warn", "high"
    message: str
    evidence: str = ""


@dataclass
class SignalResult:
    signal_name: str  # "SpecCheck", "ScopeCheck", "TraceCheck"
    triggered: bool
    score: float  # 0.0 (clean) to 1.0 (strong suspicion)
    findings: List[SignalFinding] = field(default_factory=list)
    latency_ms: float = 0.0


@dataclass
class VeriPatchReport:
    task_id: str
    verdict: Verdict
    signals_triggered: int
    active_signals: List[str]
    signal_results: Dict[str, SignalResult]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "verdict": self.verdict.value,
            "signals_triggered": self.signals_triggered,
            "active_signals": self.active_signals,
            "summary": self.summary,
            "signal_results": {
                k: {
                    "signal_name": v.signal_name,
                    "triggered": v.triggered,
                    "score": round(v.score, 4),
                    "latency_ms": round(v.latency_ms, 2),
                    "findings": [asdict(f) for f in v.findings],
                }
                for k, v in self.signal_results.items()
            },
        }
