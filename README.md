# reward-hacking-swe
SWE Fall 2026 Team research project on Reward Hacking

Below is the recommended **single best research question**, our **novel approach**, and two ready-to-use deliverables I created in `docs/`.

---

### 1. Selecting ONE Best Research Question

| Original RQ | Assessment vs. 2025–2026 SOTA & 4-Week Timeline | Decision |
|---|---|---|
| **RQ1:** How do evaluation weaknesses affect scores? | **Crowded / already quantified** by SWE-Bench+, UTBoost (ACL 2025), PatchDiff (ICSE 2026), and SWE-Bench Pro Verified (2026). High risk of looking like a replication. | Use as **Motivation** only |
| **RQ2:** How can sandbox exploitation be prevented? | **Necessary but insufficient.** Hardening (Pro Verified, RHB, RewardHackingAgents) stops tampering/leakage, *not* semantic shortcuts on weak tests. | Adopt as **Precondition** |
| **RQ3 (Sharpened):** Independent validation of test-passing patches | **Clear unsolved gap + high publishability + 4-week feasible.** Existing validators (Invalidator in TSE, UTBoost in ACL, PatchDiff in ICSE) require the **gold patch** as an oracle—useless on new benchmarks or real PRs. | **SELECT AS CORE RQ** |

> **Recommended Single Core RQ:**  
> ***Once environment hardening eliminates explicit sandbox cheating, how effectively can reference-free (gold-patch-free) triangulated validation detect semantic reward hacking and test-overfitted patches among test-passing coding-agent submissions—without rejecting genuinely correct fixes?***

---

### 2. Novel Idea: `VeriPatch` (Reference-Free Triangulated Validation)

Instead of relying on a gold patch, white-box model weights (`HackTrace`), or heavy formal proofs (`SWE-Proof`), **`VeriPatch`** audits any test-passing patch using **three orthogonal, black-box signals**:
1. **`SpecCheck` (Dynamic / Semantic):** An independent LLM test generator—strictly **blinded** to the agent's patch and benchmark tests—synthesizes boundary, edge-case, and metamorphic tests from the issue description + pre-patch repo only.
2. **`ScopeCheck` (Static + Full-Repo Regression):** Deterministic AST/diff checks (test-file edits, broad `try/except` swallowing, magic literals) + running unmodified sibling tests across the repo (capturing the 7.8% broader-test failures reported by PatchDiff).
3. **`TraceCheck` (Trajectory-to-Diff Provenance):** Cross-checks the agent's tool-call log against the final diff to flag *"test-peeking → literal mirroring"* and blind oracle-fishing.

These combine into a practical **3-Tier Trust Verdict** (`VERIFIED PASS`, `ESCALATE / REVIEW`, `LIKELY HACK`), evaluated not only on **False-Pass Recall & Precision** but also on **Collateral Damage (False-Fail Rate on genuinely correct patches)** and **\$/latency overhead**.

---

### 3. Deliverables Created in Your Workspace

1. **Full Research Plan, SOTA Survey & Paper Blueprint:**  
   [Research_Plan_and_Paper_Blueprint.md](file:///d:/Minar/Study/Special%20Topics%20In%20Software%20Engineering/reward-hacking-swe/docs/Research_Plan_and_Paper_Blueprint.md)
   - RQ selection matrix & justification for the professor.
   - 4-pillar SOTA literature survey covering **IEEE TSE**, **ACM TOSEM**, **ICSE**, **FSE**, **ASE**, **ACL**, **ICML**, **ICLR**, **NeurIPS**, and 2026 frontier preprints, plus a positioning matrix.
   - **4-week feasible experimental design** (reusing 120–150 publicly labeled passing patches from SWE-bench Verified / UTBoost / PatchDiff + 20–30 synthetic semantic hacks + a 30-task fresh hardened Pro Verified slice, with blinded 2-rater adjudication and Cohen's $\kappa$).
   - **8–10 page IEEE/ACM paper outline**, **4-week role division** (Nov 23 → Dec 21) for Heng Vicheka, Le Tri Lam, and Matiur Rahman Minar, and **Professor Q&A talking points**.

2. **Interactive Final Presentation Draft (`.pptx`):**  
   [Final_Presentation_Draft.pptx](file:///d:/Minar/Study/Special%20Topics%20In%20Software%20Engineering/reward-hacking-swe/docs/Final_Presentation_Draft.pptx)
   - **12 widescreen (16:9) slides** styled in your team's burgundy & warm-cream academic theme, validated with zero XML errors, and **embedded Speaker Notes** on every slide.
   - Includes an **interactive Slide 2 (*"Spot the Hack!"* 30-second audience poll)**, a **4-step worked walkthrough (Slide 8)** showing `VeriPatch` catching that exact hack, the SOTA comparison matrix, architecture diagram, experimental design, paper blueprint, and 4-week roadmap.

---

### Recommended Next Steps
- **Open [Final_Presentation_Draft.pptx](file:///d:/Minar/Study/Special%20Topics%20In%20Software%20Engineering/reward-hacking-swe/docs/Final_Presentation_Draft.pptx)** in PowerPoint to review the layout and speaker notes; tell me if you want any slides tweaked, expanded, or adapted for your **Week 12 Midterm Progress Presentation** (Nov 30–Dec 7).
- Once your professor approves the narrowed RQ, we can start scaffolding the **`VeriPatch` prototype** (`SpecCheck`, `ScopeCheck`, `TraceCheck`) and the **IEEE/ACM LaTeX paper template** directly in this repository.