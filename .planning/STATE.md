# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2025-01-25)

**Core value:** Produce classroom-ready materials that actually work for teaching — slides that support instruction, worksheets with room to write, discussions with clear structure, and differentiation built in from the start.

**Current focus:** Phase 3 - Single Persona Feedback

## Current Position

Phase: 3 of 5 in progress (Single Persona Feedback)
Plan: 1 of 3 complete
Status: In progress
Last activity: 2026-01-26 — Completed 03-01-PLAN.md: struggling learner persona and evaluator created

Progress: [████████░░] 83%

## Performance Metrics

**Velocity:**
- Total plans completed: 12
- Average duration: 5.2 min
- Total execution time: 62 minutes

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-core-lesson-generation | 6 | 33min | 5.5min |
| 02-material-quality-formatting | 5 | 26min | 5.2min |
| 03-single-persona-feedback | 1 | 3min | 3min |

**Recent Trend:**
- Last 6 plans: 01-06 (5min), 02-01 (4min), 02-02 (5min), 02-03 (4min), 02-04 (5min), 02-05 (8min), 03-01 (3min)
- Trend: Phase 3 started efficiently, faster than average due to focused persona/evaluator creation

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- **Roadmap creation (Phase 0):** Adopted research-recommended 5-phase approach (core → quality → single persona → multi-persona → sequences) to de-risk file generation and feedback loops before scaling complexity
- **Cognitive rigor threshold (01-01):** Set 40% minimum higher-order thinking (analysis + knowledge utilization) based on educational research. Enforced in Stage 3b validation
- **7-stage workflow structure (01-01):** Linear workflow separates lesson design (Stages 1-4) from file generation (Stages 5-6) to enable future enhancements without redesigning core
- **Template creation approach (01-01):** Python script generates Office files programmatically for reproducibility. Templates verified with python-pptx/python-docx before committing
- **Stage 2b positioning (01-02):** Knowledge classification happens between decomposition and lesson design because teacher input about what needs teaching directly affects activity design
- **Binary knowledge classification (01-02):** Simple needs_teaching/already_assumed options instead of a scale - teachers need clear instructional decisions
- **UUID session IDs (01-02):** UUID v4 for session identification ensures uniqueness and avoids timestamp parsing issues
- **Lesson type distributions (01-03):** Each lesson type has recommended Marzano level distribution (e.g., novel_application: 50% knowledge_utilization)
- **Validation exit codes (01-03):** Exit 0=pass, 1=warnings, 2=fail/block - controls workflow progression
- **Maximum 3 validation attempts (01-03):** After 3 failures, escalate to teacher for guidance
- **Sparse slide format (01-04):** Max 5 bullets per slide, max 15 words per bullet for teacher-led instruction
- **Font size standards (01-04):** 40pt titles, 20pt body (exceeds 16pt minimum per SLID-04)
- **Presenter notes structure (01-04):** SAY/ASK/DEMO/WATCH FOR sections for teacher guidance
- **Material type mapping (01-05):** Direct lesson-to-material mapping (introducing->worksheet, practicing->problem_set, etc.)
- **Assessment integration (01-05):** Every document includes assessment (exit_ticket, embedded, or performance) per ASMT-01
- **Stage 6 error recovery (01-06):** Specific fix instructions for common validation failures (hidden slides, font sizes, template tags)
- **Stage 7 summary template (01-06):** Standardized presentation format with cognitive rigor percentage and next steps
- **E2E test fixture (01-06):** Sample lesson at 70% higher-order thinking provides margin above 40% minimum
- **Float multiplier line spacing (02-01):** Use 2.0 multiplier instead of fixed Pt for proportional scaling with font size changes
- **Cognitive complexity-based spacing (02-01):** Answer space scales with Marzano level (2-6 lines) to match thinking demands
- **Discussion facilitation notes (02-02):** TIME ALLOCATION, WATCH FOR, and PROMPTS TO USE sections in slide notes for teacher guidance
- **p5.js CDN for simulations (02-03):** Self-contained HTML files with p5.js loaded from CDN for zero-install student deployment
- **Keyword-based simulation detection (02-03):** Predictable simulation type selection based on competency keywords (not LLM classification)
- **4-level rubric structure (02-04):** Advanced/Proficient/Developing/Beginning (4/3/2/1 points) aligns with common educational standards
- **Auto-generate answer keys (02-04):** Quiz/test answer keys generated automatically alongside student version to save teacher time
- **Default Socratic criteria (02-04):** Participation, Evidence Use, Engagement with Others - research-backed criteria when not specified
- **Persona-based evaluation (03-01):** Parameterized PersonaEvaluator class loads persona JSON with characteristics and decision rules for automated accessibility feedback
- **Decision rules with severity thresholds (03-01):** High/medium/low severity levels based on explicit thresholds (e.g., 3+ undefined terms = high, 1-2 = medium)
- **Structured feedback format (03-01):** Each concern includes element, issue, severity, impact, evidence, and recommendation (change + rationale + implementation)
- **5-criteria accessibility framework (03-01):** vocabulary_accessibility, instruction_clarity, scaffolding_adequacy, pacing_appropriateness, engagement_accessibility
- **1-5 accessibility rating (03-01):** Quantitative rating based on concern count and severity (5 = highly accessible, 1 = major barriers)

### Pending Todos

None

### Blockers/Concerns

**Phase 1 complete (pending verification):**
- ✓ Library availability: Verified python-pptx, python-docx, and docxtpl are available (installed in 01-01)
- ✓ Marzano framework reference: Created MARZANO.md (610 lines) - well within token limits
- ✓ Teacher input workflow: Stages 1, 2, 2b complete with session management
- ✓ Lesson design workflow: Stage 3 and 3b complete with validation script
- ✓ PowerPoint generation: Stage 5 Part 1 complete with generate_slides.py (01-04)
- ✓ Word generation: Stage 5 Part 2 complete with generate_worksheet.py (01-05)
- ✓ Output validation: Combined validate_outputs.py for both PPTX and DOCX (01-05)
- ✓ Workflow documentation: Complete SKILL.md with all stages documented (01-06)
- ✓ Integration testing: test_e2e.py exercises complete workflow (01-06)
- ✓ Human verification: Slides approved after v4 with professional design system

**Phase 2 complete (5 of 5 plans, verified):**
- ✓ Worksheet formatting enhanced (02-01): double-spacing and cognitive complexity-based answer space
- ✓ Discussion facilitation notes added (02-02): timing, teacher prompts, discussion protocol
- ✓ Simulation generator created (02-03): HTML/JS interactive simulations for experiential learning
- ✓ Assessment generator created (02-04): quizzes, tests, performance tasks, Socratic discussions with rubrics
- ✓ Validation and documentation updated (02-05): Phase 2 checks, SKILL.md v2.0.0, human verification
- ✓ Formatting finalized: Helvetica font, 80-character answer lines, proper name line widths
- Verification: 14/14 must-haves passed

**Phase 3 in progress (1 of 3 plans complete):**
- ✓ Persona foundation (03-01): Alex struggling learner persona with 5 evaluation criteria, PersonaEvaluator class producing structured feedback
- Next: Revision plan generator (03-02) to aggregate feedback into teacher-approved changes
- Remaining: Workflow integration (03-03) to insert Stage 3.5 persona evaluation into existing lesson generation workflow

**Phase 5 readiness:**
- Context management: Multi-lesson sequences require empirical testing of context compression strategies (flagged in research)

## Session Continuity

Last session: 2026-01-26 (Phase 3 started)
Stopped at: Completed 03-01-PLAN.md
Resume file: None
Next action: Execute 03-02-PLAN.md (Revision Plan Generator)

---
*State initialized: 2025-01-25*
*Last updated: 2026-01-26 — Phase 3 Plan 01 complete*
