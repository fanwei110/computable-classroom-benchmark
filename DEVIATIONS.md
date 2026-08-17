# Disclosed Deviations from the Preregistration

Per the freeze rules (PREREGISTRATION.md §2), every post-registration change
is recorded here with its reason and timing. Deviations #1–#7 were made
**before any formal generation was collected**; the judging harness, the
tolerances, the codebook, and the reference answers are unchanged since the
initial commit (1184058f). Items #8–#11 are post-hoc addenda (journal
revision): #8 adds analysis-only reporting; #9 adds supplementary robustness
experiments on a representative model; #10 reports a human validation of the
error coding; #11 adds a factorial-completion experiment that unbundles the
structure factor (reviewer-requested). None changes any main-study
generation, judging, or correctness result.

## 8. Journal-revision analysis addendum (2026-06-14, analysis-only)

For the journal version, `analysis/journal_revision_stats.py` recomputes —
from the already-collected `runs/results_formal.csv` and
`coding/auto/final_coded.csv`, with no new generations and no change to any
judging or coding rule — the following additional reported quantities:
mechanical (κ-immune) lower bounds per error class; per-coder proportion
intervals; correctness conditional on executable code; the visible-vs-silent
failure split; latency-truncation cost at 45 s / 60 s; and a cluster-bootstrap
CI on the C3−C1 difference for T3. These were added to address peer-review
concerns and are the single source of truth for the journal manuscript's
numbers. The Fig.2 population is confirmed at N = 306.

## 9. Supplementary robustness experiments on DeepSeek (2026-07-02, post-hoc)

To address peer-review concerns that (a) the "structure" factor is a deployable
bundle and (b) provider-default decoding might be a lucky setting, two
supplementary experiments were run AFTER the main study on a representative
widely-deployed model — DeepSeek `deepseek-chat` via the official DeepSeek API
(same vendor as M2 but NOT the same model as M2 = deepseek-v4-pro; used only as
a representative robustness check, not to recalibrate the main study's absolute
levels) — over 6 representative tasks (one per knowledge point) × 5 repetitions:

- **Template ablation** (`exp_runner.py --exp ablation`): leave-one-out / minimal
  variants of the C4 template (C1 / contract-only / minus-scaffold /
  minus-convention / full-C4) to decompose the structure bundle. The gain is
  dominated by task-statement regularization (+53.3 pp), with the step scaffold
  moderate (+16.7) and the convention line small (+3.3) — reproducing the main
  finding (structure ≫ convention) within a single model.
- **Temperature sensitivity** (`--exp temperature`): C1 & C4 at T ∈ {0, 0.5, 1.0};
  C4 (80–83%) ≫ C1 (27–30%) at every temperature.

These use the FROZEN judge and add no change to any main-study data, judging, or
coding rule. Results in `runs/exp_stats.txt`; per-cell data in
`runs/exp_results.csv`; raw generations under `runs/raw/exp/`. Reported in §V.E.
The DeepSeek API key was passed via environment variable only and is never stored
in the repository.

## 10. Human validation of the error coding (2026-07-02, post-hoc)

Two annotators independently blind-coded the released batch-1 sheets. The two
formal sheets each contain 286 rows: **266 C1 items** and **20 C4 items**, as
identified by the public metadata in `coding/auto/final_coded.csv`. Calibration
drills are stored separately in `coding/calibration/drill_sheet.xlsx` and are not
part of either formal sheet. The manuscript estimand is reproduced by joining
on `blind_id` and filtering `condition == "C1"`, rather than by dropping an
assumed block of sheet rows. On those 266 C1 items, Cohen's kappa is 0.028,
Gwet's AC1 is 0.324, and raw agreement is 45.1%. As a broader batch-1 sensitivity
check, all 286 formal rows give kappa 0.030 and raw agreement 45.5%.

The conventional-versus-conceptual (CV/CN) distinction consequently has low
inter-coder reliability. The manuscript therefore makes no claim about which
of those two classes predominates and limits interpretation to directly measured
outcomes and mechanically defined categories. No main-study correctness result
is affected. Reproduction: `analysis/human_coding_stats.py --condition C1`;
output: `runs/human_coding_stats.txt`.

The separate calibration drill remains available for coder training and audit,
but it is not an analysis row in either released formal coding sheet.
This correction changes no generation, judging rule, or correctness outcome.

## 1. Prompt language: English → Chinese (2026-06-11)

The locked deployment config fixes prompt_language = zh-CN (classroom
practice). The C2/C4 prompts frozen at registration were English; running
C1/C3 in Chinese against English C2/C4 would confound the structure factor
with language. The C2/C4 sets were therefore re-issued in Chinese
(prompts/C2_zh, C4_zh), mirroring the English originals section for section
and step for step; the zero-leak screen was re-run on the Chinese set
(18/18 clean, 23 forbidden patterns). English originals retained for the
record. No generation had been collected at the time of the change.

## 2. M1 model substitution: GPT-5.5 → Mistral Large 2512 (2026-06-11)

The PI-locked config named openai/gpt-5.5 as M1. The connectivity probe
from the actual deployment network returned HTTP 403 ("not available in
your region") for **all** OpenAI, Anthropic, and Google models on
OpenRouter. M1 was replaced by the strongest international frontier model
actually reachable from the deployment environment
(mistralai/mistral-large-2512; probe 2026-06-11). M2/M3 unchanged. This
substitution itself illustrates the model-procurement constraint of Chinese
university deployments discussed in the paper.

## 3. C1/C3 improvised phrasings: LLM-simulated personas, not external
##    instructors (2026-06-11)

The registered design called for phrasings authored by two instructors not
involved in the benchmark's design. External collection was not completed;
the phrasings actually used were generated by a fourth LLM (not among the
three evaluated models) role-playing two instructor personas, from
zero-convention task essences, and are frozen verbatim in
prompts/C1_source/ with this provenance stated in their headers.

Consequences, handled as follows:
- The paper (§IV.C) describes the phrasings as LLM-simulated and treats
  their ecological validity as an explicit limitation (§VI). The claim
  "authored by independent instructors" is **removed**, not weakened.
- Each phrasing passed the same convention-leak screen as C2 (word-level
  pattern list; one variant swap logged in
  prompts/C1_source/variant_selection.md).
- One phrasing (KP5_T3, persona A, V1) had been sent to M2 and M3 once
  each during the 6-generation pipeline dry-run (tag=pilot) before this
  freeze. Pilot generations are excluded from all formal results; the
  exposure is disclosed here.

## 4. Pilot dry-run before formal data (2026-06-11)

A 6-generation end-to-end pipeline dry-run (tag=pilot; 2 tasks, M2/M3,
C1/C3/C4) was executed to validate the runner, logging, and judging
pipeline. Pilot data are archived separately (runs/raw/pilot/) and excluded
from all formal analyses. No judging rule was changed as a result of the
pilot.

## 5. Harness executor: import → script execution; extraction aligned to
##    the registered rule (2026-06-11, after 9 of 2,160 formal generations)

The first formal smoke batch (9 generations) exposed two format-neutrality
gaps in the *infrastructure* (not in any judging rule):
(a) the executor imported the generated file as a module, so a fully
    contract-compliant script that assigns `result` under
    `if __name__ == "__main__":` never populated `result`. The executor now
    runs the file as a script (runpy, run_name="__main__"), exactly as a
    classroom would. The adversarial suite was extended with sample c21
    covering this idiom; the full suite passes 41/41 under the new executor.
(b) the code-extraction implementation matched ANY fenced block, while the
    registered rule (runs/schema.md) says "first fenced python block"; a
    display block placed before the code therefore shadowed it. The
    implementation now prefers python-tagged blocks that define `result`.
Tolerances, tiers, the T3 rules, and the codebook are untouched.

## 6. max_tokens 8192 → 32768; first 9 formal generations discarded and
##    re-run (2026-06-11)

M2/M3 are reasoning models whose thinking tokens count toward the
completion limit; under max_tokens=8192 three of the first nine formal
generations returned EMPTY content with finish_reason=length - an
infrastructure truncation, not a model-capability observation. The cap
(whose stated purpose was preventing truncation) was raised to 32768.
For uniformity of settings across all 2,160 generations, the nine
generations produced under the old cap were discarded (archived verbatim
in runs/raw/formal_discarded_8k/) and their cells re-generated under the
amended config.

## 7. Error coding: deterministic mechanical classifier + heterogeneous AI
##    double-coding, no human raters (2026-06-12)

The registered protocol called for two human raters double-coding all
failures (codebook.md §5). Under submission time constraints the authors
opted for a fully automated protocol, disclosed as follows:
(a) a deterministic *mechanical classifier* (analysis/mechanical_coder.py,
    released) implements the codebook's preregistered mechanical criterion
    literally - recomputing every enumerated candidate convention with the
    reference implementations and accepting a class only when one swap
    explains all failed keys within the task tolerances; it resolves 343 of
    686 items (50%) deterministically;
(b) two LLM coders that are architecturally distinct from each other and
    from the three evaluated models independently code all 686 items from
    the same blinded item files prepared for human coders, under the frozen
    manual. Originally Qwen3-235B-A22B-2507 + Kimi K2.6; Kimi proved
    operationally unstable (minutes-long thinking, intermittent empty
    completions, silent process crashes after 197 of 686 items) and was
    replaced by Llama-4-Maverick BEFORE any reconciliation was computed;
    Kimi's 197 completed votes are archived as supplementary third votes
    (coding/auto/ai_coder_K.jsonl). Inter-coder agreement (κ) and agreement
    with the mechanical layer are reported; Q/L disagreements not settled
    by the mechanical layer are adjudicated by a third non-evaluated model
    (MiniMax-M3, replacing Llama in the adjudicator role after Llama became
    a coder);
(c) boundary exemplar 13 (code that hardcodes a hand-rounded constant
    instead of computing; submitted values within 0.2% of reference) was
    ruled **CN with subtag `hardcoded_constant`** per the letter of the
    frozen codebook ("a choice with no textbook standing is not a
    convention"), by the analyst, BEFORE the AI coding ran; its share is
    reported separately in the paper so readers can reallocate it;
(d) the paper (§IV.D) is rewritten to describe this protocol truthfully -
    the "two human raters" claim is removed, and the absence of human
    validation is stated as a limitation;
(e) visualization adequacy (§IV.B) is likewise rated by two non-evaluated
    vision models (Qwen2.5-VL-72B, Llama-4-Maverick) on the rebuilt
    per-run figure archive (632/720 reproducible; 57 generations never
    executed, 21 produced no code, 10 set no figure path - all counted
    inadequate). Rules pre-stated: adequate iff BOTH raters pass all four
    rubric items; rater disagreements count as inadequate. Nine generations
    produced interactive HTML figures the vision raters cannot score; they
    are excluded from the adequacy denominator and disclosed. Because
    adequacy prevalence is extreme (~90%), Cohen's κ collapses (0.09, the
    κ paradox); the paper reports raw agreement (83.5%) and Gwet's AC1
    (0.80) alongside it.

## 11. Factorial-completion experiment: unbundling the structure factor (2026-08-04/05, post-hoc, reviewer-requested)

Peer review of the journal submission noted that the preregistered structure
factor is a bundle (C1 -> C2 changes both the task wording and the scaffold)
and requested conditions that vary each ingredient separately. Two new cells
were therefore collected post hoc, completing a wording x scaffold factorial
in the no-convention row:

- **C1wS** (improvised wording, + scaffold): the VERBATIM frozen C1 phrasing
  (persona variants A/B alternated in replay, five uses each; the formal runs
  submitted A and B as separate five-repetition blocks) embedded in the C2_zh
  regularized task block; the C1 phrasing's own output-contract paragraph is
  stripped because the scaffold supplies the identical contract block.
- **Creg** (regularized wording, no scaffold): the C2_zh regularized task
  statement + the code-quality line + the output contract, with no role
  framing, no concept block, and no step scaffold. Built from the C2_zh
  material (not C4_zh) because the C4 task block for KP3_T1 contains one
  convention-bearing sentence; the C2 block is the clean no-convention
  regularized statement.

Scale: 18 tasks x 3 models x 10 repetitions per new cell = 1,080 additional
generations (runner: `rev_runner.py`; tags `runs/raw/rev_full_M{1,2,3}`;
collected 2026-08-04/05 in a 180-generation pilot batch plus per-model
completion batches, under the same requested OpenRouter model identifiers as
the formal run; 3 transport-level API failures were re-run to completion).
Generation, judging, and aggregation reuse the FROZEN harness, prompts,
judge, and correctness definitions unchanged. Analysis:
`analysis/rev_crossing_stats.py` -> `runs/rev_crossing_stats.txt`
(cluster-bootstrap CIs; GEE wording x scaffold decomposition).

Status: post-hoc, disclosed, supplementary. The preregistered inference
identifies only the deployed bundle (C2 - C1); the completed factorial is
reported in the paper as disclosed supplementary evidence (Section V.B,
Table IV) and does not alter any preregistered hypothesis, judging rule, or
main-study number.

### 11a. Adjacent-window replay of the pre-registered cells (2026-08-06)

Peer review of the first submission asked either for conditions that vary the
scaffold and the wording separately, or for the claim to be demoted to a
bundled template effect. The two new cells above (Creg, C1wS) were collected
in August 2026, whereas the pre-registered C1 and C2 were collected in June
2026. Comparing them directly would have aligned a collection date with the
design: the two pre-registered cells occupy the diagonal of the wording x
scaffold factorial and the two new cells occupy the off-diagonal, so a batch
indicator is collinear with the interaction contrast and splits the simple
effects.

We therefore replayed C1 and C2 on August 6, immediately after the new-cell
collections of August 4-5 (`--conditions batch`, tags
`runs/raw/rev_batch_M{1,2,3}`; 18 tasks x 3 models x 10 repetitions each =
1,080 further generations). The replayed prompts are BYTE-IDENTICAL to the
frozen formal material: C1rep reads `prompts/C1_final/<task>_<variant>.md`
and C2rep reads `prompts/C2_zh/<task>.md`, with no reconstruction; generation,
judging, and aggregation reuse the frozen harness unchanged. Table IV compares
cells acquired within the short August 4-6 period while disclosing the two
adjacent windows; Table II retains the June preregistered estimates unchanged.

Total post-hoc generations for this experiment: 2,160 (1,080 new cells +
1,080 replays), matching the size of the pre-registered study.

### 11b. Measured model drift between the two windows

The replay doubles as a drift measurement, reported in Section V.B:

- C1: 34.3% (June) vs 33.9% (August replay), difference -0.4 pp
  [-2.8, +2.2]; the interval includes zero.
- C2: 63.9% (June) vs 69.8% (August replay), difference +5.9 pp
  [+1.5, +10.7]; the replay rate is higher and the interval excludes zero.

Per-call response metadata documents a plausible source of the C2 shift but
does not identify a causal mechanism. The requested identifier
`deepseek/deepseek-v4-pro` returned the dated snapshot
`deepseek/deepseek-v4-pro-20260423` in June and an undated alias in August,
and the set of serving providers changed. By contrast, the version-stamped
`mistralai/mistral-large-2512` was stable to within +/-1.1 pp on both cells.
A requested aggregator identifier is not an immutable model snapshot. The
released logs therefore record provider and returned model per call; Table IV
discloses the adjacent dates and reports a provider-adjusted GEE sensitivity.

Operational note: the M3 lane was interrupted at 327/360 generations by a
console-encoding failure in the surrounding shell (not in the runner or the
judge); the run was resumed with the runner's resume logic, which skips
completed run_ids, and completed at 360/360. No generation was judged twice
and none was discarded.
