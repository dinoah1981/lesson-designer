---
phase: 03-single-persona-feedback
plan: 02
subsystem: lesson-design-workflow
tags: [persona-feedback, revision-planning, python, json, markdown]

# Dependency graph
requires:
  - phase: 03-01
    provides: "Persona definition and evaluator for struggling learner"
provides:
  - "Revision plan generator transforming persona feedback into actionable changes"
  - "apply_revisions() function for automated lesson JSON modification"
  - "Stage 3.5 workflow documentation in SKILL.md"
affects: [03-03, phase-04-multi-persona]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Element-specific handlers for applying revisions (_apply_vocabulary_change, _apply_scaffolding_change, etc.)"
    - "Severity-based prioritization (high → critical_changes, medium → optional_improvements)"
    - "Implementation objects with action-specific fields for automation"

key-files:
  created:
    - ".claude/skills/lesson-designer/scripts/generate_revision_plan.py"
  modified:
    - ".claude/skills/lesson-designer/SKILL.md"

key-decisions:
  - "Revision plan JSON includes implementation objects parseable by apply_revisions() for full automation"
  - "Element-specific handlers (_apply_vocabulary_change, etc.) allow targeted lesson JSON modifications"
  - "Severity-based categorization (critical/optional/low-priority) guides teacher approval workflow"
  - "Markdown output provides teacher-readable format with approve/reject checkboxes"

patterns-established:
  - "Implementation object pattern: each change includes action-specific fields enabling automation"
  - "Element-based routing: change.element determines which handler function processes the revision"
  - "Status tracking: changes track 'pending'/'approved'/'rejected' for multi-step workflows"

# Metrics
duration: 5min
completed: 2026-01-26
---

# Phase 03 Plan 02: Revision Plan Generator Summary

**Revision plan generator with apply_revisions() automating lesson JSON modifications from persona feedback**

## Performance

- **Duration:** 5 min
- **Started:** 2026-01-26T07:05:52Z
- **Completed:** 2026-01-26T07:10:55Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Created generate_revision_plan.py with full revision automation pipeline
- Implemented apply_revisions() with element-specific handlers for vocabulary, scaffolding, pacing, and instructions
- Documented Stage 3.5: Persona Feedback & Revision workflow in SKILL.md
- Established implementation object pattern enabling automated lesson modifications

## Task Commits

Each task was committed atomically:

1. **Task 1: Create revision plan generator script** - `8cc0a0f` (feat)
2. **Task 2: Add Stage 3.5 to SKILL.md workflow** - `8787925` (docs)

## Files Created/Modified

- `.claude/skills/lesson-designer/scripts/generate_revision_plan.py` - Transforms persona feedback into revision plan JSON/Markdown and applies approved changes to lesson JSON
- `.claude/skills/lesson-designer/SKILL.md` - Added Stage 3.5 workflow documentation, updated checklists and quick reference

## Decisions Made

1. **Implementation object architecture:** Each change in the revision plan includes an `implementation` object with element-specific fields. This enables apply_revisions() to parse and execute changes automatically without manual intervention.

2. **Element-specific handlers:** Created dedicated functions (_apply_vocabulary_change, _apply_scaffolding_change, _apply_pacing_change, _apply_instructions_change) to handle the unique JSON modifications for each element type. Generic changes fall through to _apply_generic_change for manual review.

3. **Severity-based categorization:** Concerns are categorized as critical_changes (high severity), optional_improvements (medium severity), or requires_teacher_decision (low severity) to guide teacher approval workflow.

4. **Teacher-readable Markdown:** render_revision_markdown() generates formatted output with approve/reject checkboxes, making it easy for teachers to review and make decisions without editing JSON.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## Next Phase Readiness

- Revision plan generator ready for Stage 3.5 integration testing (Plan 03-03)
- apply_revisions() architecture supports Phase 4 multi-persona aggregation (change IDs enable deduplication)
- Implementation object pattern extensible for new element types in Phase 4

**Ready for:** Plan 03-03 (Stage 3.5 integration testing)

---
*Phase: 03-single-persona-feedback*
*Completed: 2026-01-26*
