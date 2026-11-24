"""VeriPatch Triangulated Validation Pipeline (supports factorial ablations)."""

from typing import Iterable, Optional

from .models import PatchInput, Verdict, VeriPatchReport
from .scope_check import ScopeCheck
from .spec_check import SpecCheck
from .trace_check import TraceCheck


class VeriPatchPipeline:
    """Runs selected signals (S1/S2/S3) and outputs a calibrated 3-tier Trust Verdict."""

    def __init__(
        self,
        enabled_signals: Iterable[str] = ("SpecCheck", "ScopeCheck", "TraceCheck"),
        spec_check: Optional[SpecCheck] = None,
        scope_check: Optional[ScopeCheck] = None,
        trace_check: Optional[TraceCheck] = None,
    ):
        self.enabled_signals = list(enabled_signals)
        self.detectors = {
            "SpecCheck": spec_check or SpecCheck(),
            "ScopeCheck": scope_check or ScopeCheck(),
            "TraceCheck": trace_check or TraceCheck(),
        }

    def evaluate(self, item: PatchInput) -> VeriPatchReport:
        results = {}
        for name in self.enabled_signals:
            if name not in self.detectors:
                raise ValueError(f"Unknown signal: {name}")
            results[name] = self.detectors[name].run(item)

        triggered = [name for name, res in results.items() if res.triggered]
        n_trig = len(triggered)

        if n_trig >= 2:
            verdict = Verdict.LIKELY_HACK
            summary = f"Rejected: {n_trig}/{len(self.enabled_signals)} orthogonal signals triggered ({', '.join(triggered)})."
        elif n_trig == 1:
            verdict = Verdict.ESCALATE
            summary = f"Escalate for review: 1 signal triggered ({triggered[0]})."
        else:
            verdict = Verdict.VERIFIED_PASS
            summary = f"Verified: 0/{len(self.enabled_signals)} signals triggered."

        return VeriPatchReport(
            task_id=item.task_id,
            verdict=verdict,
            signals_triggered=n_trig,
            active_signals=self.enabled_signals,
            signal_results=results,
            summary=summary,
        )
