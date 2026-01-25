---
phase: 01-core-lesson-generation
plan: 03
subsystem: skill-architecture
tags: [marzano-taxonomy, lesson-design, cognitive-rigor, validation, python]

# Dependency graph
requires:
  - phase: 01-01
    provides: SKILL.md skeleton and MARZANO.md framework reference
  - phase: 01-02
    provides: Competency breakdown structure (02_competency_breakdown.json)
provides:
  - Complete Stage 3 instructions for Marzano-based lesson design
  - Stage 3b cognitive rigor validation workflow
  - validate_marzano.py script enforcing 40% higher-order thinking minimum
  - design_lesson.py helper functions for lesson creation
  - JSON schema for 03_lesson_design_v1.json
affects: [01-04, 01-05, 01-06, 02-quality-validation]

# Tech tracking
tech-stack:
  added: []
  patterns: [Marzano cognitive rigor validation, lesson type distributions, activity templates]

key-files:
  created:
    - .claude/skills/lesson-designer/scripts/validate_marzano.py
    - .claude/skills/lesson-designer/scripts/design_lesson.py
  modified:
    - .claude/skills/lesson-designer/SKILL.md

key-decisions:
  - "Lesson types have distinct cognitive distributions (introducing: 30% retrieval, novel_application: 50% knowledge_utilization)"
  - "Validation script uses exit codes for workflow control (0=pass, 1=warnings, 2=fail/block)"
  - "Maximum 3 validation attempts before escalating to teacher"

patterns-established:
  - "Marzano validation: Run validation script immediately after lesson design, iterate on failure"
  - "Lesson type determines recommended cognitive distribution"
  - "Activity specification: name, duration, marzano_level, instructions, materials, student_output, assessment_method"

# Metrics
duration: 8min
completed: 2026-01-25
---

# Phase 01 Plan 03: Marzano-based Lesson Design and Validation Summary

**Stage 3 lesson design with 5 lesson types, Stage 3b cognitive rigor validation enforcing 40% higher-order thinking minimum via Python script**

## Performance

- **Duration:** 8 minutes
- **Started:** 2026-01-25T21:06:02Z
- **Completed:** 2026-01-25T21:14:15Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Implemented complete Stage 3 instructions with all 5 lesson types (introducing, practicing, applying, synthesizing, novel_application)
- Created validate_marzano.py that enforces 40% higher-order thinking minimum with exit code 2 blocking progression
- Created design_lesson.py with helper functions for lesson creation, activity templates, and recommended distributions
- Defined JSON schema for lesson design files with hidden slide content

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement Stage 3 - Marzano-based lesson design** - `94fc1dc` (feat)
2. **Task 2: Create Marzano validation script** - `fb19bdd` (feat)
3. **Task 3: Create lesson design helper functions** - `1ee0133` (feat)

## Files Created/Modified

- `.claude/skills/lesson-designer/SKILL.md` - Updated with Stage 3 (lesson design workflow) and Stage 3b (validation workflow)
- `.claude/skills/lesson-designer/scripts/validate_marzano.py` - Cognitive rigor validation script with 40% minimum enforcement
- `.claude/skills/lesson-designer/scripts/design_lesson.py` - Helper functions for lesson creation and activity templates

## Decisions Made

**Lesson type cognitive distributions:**
Each lesson type has a recommended Marzano level distribution:
- Introducing: 30% retrieval, 40% comprehension, 20% analysis, 10% knowledge utilization
- Practicing: 20% retrieval, 30% comprehension, 35% analysis, 15% knowledge utilization
- Applying: 10% retrieval, 20% comprehension, 30% analysis, 40% knowledge utilization
- Synthesizing: 10% retrieval, 20% comprehension, 35% analysis, 35% knowledge utilization
- Novel application: 5% retrieval, 15% comprehension, 30% analysis, 50% knowledge utilization

**Validation exit code semantics:**
- Exit code 0: Passed - proceed to Stage 4
- Exit code 1: Passed with warnings - can proceed but inform teacher
- Exit code 2: Failed - blocks progression, must iterate on design

**Maximum validation attempts:**
Set to 3 attempts. If still failing after 3 tries, escalate to teacher for guidance on acceptable trade-offs.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Phase 1 Plans 04-06 (File Generation):**
- Stage 3 produces `03_lesson_design_v1.json` with complete activity specifications
- Stage 3b validates and saves `04_lesson_final.json` for generation
- Hidden slide content structure defined for slide generation

**Ready for Phase 2 (Quality Validation):**
- validate_marzano.py provides foundation for additional validation scripts
- Validation report format established for consistent feedback

**Blockers/concerns:**
None identified. Marzano-based lesson design and validation is complete.

---
*Phase: 01-core-lesson-generation*
*Completed: 2026-01-25*
