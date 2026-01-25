---
phase: 01-core-lesson-generation
plan: 02
subsystem: teacher-input
tags: [competency-decomposition, session-management, teacher-workflow, skill-design]

# Dependency graph
requires:
  - phase: 01-01
    provides: Skill directory structure and Marzano framework reference
provides:
  - Complete Stage 1 instructions for competency input gathering
  - Complete Stage 2 instructions for competency decomposition
  - Complete Stage 2b instructions for knowledge classification and proficiency targets
  - parse_competency.py script for session management
affects: [01-03, 01-04, 01-05, 01-06]

# Tech tracking
tech-stack:
  added: []
  patterns: [Session-based state management, UUID session IDs, JSON schema validation]

key-files:
  created:
    - .claude/skills/lesson-designer/scripts/parse_competency.py
  modified:
    - .claude/skills/lesson-designer/SKILL.md

key-decisions:
  - "Stage 2b positioned between decomposition and lesson design to capture teacher input before planning"
  - "Knowledge classification uses binary options (needs_teaching vs already_assumed) for clarity"
  - "Proficiency levels use four tiers (novice, developing, proficient, advanced) aligned with common rubric patterns"
  - "Session management uses UUID v4 for unique session identification"

patterns-established:
  - "5-question competency intake: competency, grade, lesson count, duration, constraints"
  - "Skill decomposition pattern: verb + object + full statement + required knowledge items"
  - "Knowledge classification flow: present items, explain impact, gather classifications"
  - "Session file structure: 01_input.json (Stage 1), 02_competency_breakdown.json (Stages 2/2b)"

# Metrics
duration: 6min
completed: 2026-01-25
---

# Phase 01 Plan 02: Teacher Input and Competency Decomposition Summary

**Complete teacher input workflow with competency decomposition and knowledge classification, plus session management utilities**

## Performance

- **Duration:** 6 minutes
- **Started:** 2026-01-25
- **Completed:** 2026-01-25
- **Tasks:** 3
- **Files modified:** 2 (1 created, 1 modified)

## Accomplishments

- Implemented Stage 1 with 5 input questions and skill-focused validation guidance
- Implemented Stage 2 with competency decomposition process and example breakdown
- Implemented Stage 2b with knowledge classification and proficiency target collection
- Created parse_competency.py with all session management functions
- Updated workflow to include Stage 2b in correct position (between Stage 2 and Stage 3)
- Covered all COMP-01 through COMP-05 requirements

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement Stage 1 - Competency input gathering** - `e4af4d0` (feat)
   - Added 5 input questions (competency, grade, lesson count, duration, constraints)
   - Added validation guidance for skill-focused vs topic-focused competencies
   - Included JSON schema for 01_input.json

2. **Task 2: Implement Stage 2 - Competency decomposition** - `c2fda06` (feat)
   - Added decomposition process (skill verb/object + required knowledge)
   - Created parse_competency.py with session management functions
   - Uses absolute paths for Claude environment compatibility

3. **Task 3: Implement Stage 2b - Knowledge classification and proficiency targets** - `00a1c31` (feat)
   - Added classification options (needs_teaching vs already_assumed)
   - Added proficiency levels (novice, developing, proficient, advanced)
   - Updated workflow order and removed old Stage 4 placeholder

## Files Created/Modified

- `.claude/skills/lesson-designer/SKILL.md` - Updated with complete Stage 1, 2, and 2b instructions
- `.claude/skills/lesson-designer/scripts/parse_competency.py` - New session management utilities:
  - `generate_session_id()` - UUID v4 generation
  - `create_session_directory()` - Creates `.lesson-designer/sessions/{id}/`
  - `save_input()` / `load_input()` - Stage 1 persistence
  - `save_breakdown()` / `load_breakdown()` - Stage 2 persistence
  - `update_breakdown_with_classifications()` - Stage 2b updates

## Decisions Made

**Stage 2b positioning:**
Placed knowledge classification between decomposition (Stage 2) and lesson design (Stage 3) because teacher input about what needs teaching directly affects activity design. Classification should happen before planning, not after.

**Binary classification:**
Used simple needs_teaching/already_assumed instead of a scale because teachers need to make clear instructional decisions. Items either get direct instruction or retrieval practice - no middle ground.

**Proficiency level options:**
Adopted novice/developing/proficient/advanced to align with common educational rubrics. Four tiers provide enough granularity while remaining familiar to teachers.

**Session ID format:**
Used UUID v4 for session identification instead of timestamp-based IDs. UUIDs ensure uniqueness even with rapid session creation and avoid any timestamp parsing issues.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

**Deprecation warning in Python:**
Initial implementation used `datetime.utcnow()` which is deprecated. Fixed by using `datetime.now(timezone.utc)` instead. No impact on functionality.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Phase 1 Plan 03 (Lesson Design):**
- Stage 2b produces `02_competency_breakdown.json` with classifications and proficiency target
- Stage 3 can load this data to inform activity design
- Marzano framework reference already exists from Plan 01

**Ready for subsequent plans:**
- parse_competency.py utilities available for all future stages
- Session directory structure established
- JSON schemas defined and documented

**Blockers/concerns:**
None identified. Input handling is complete and validated.

---
*Phase: 01-core-lesson-generation*
*Completed: 2026-01-25*
