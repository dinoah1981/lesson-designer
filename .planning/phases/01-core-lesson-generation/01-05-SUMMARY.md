---
phase: 01-core-lesson-generation
plan: 05
subsystem: skill-architecture
tags: [docxtpl, word-generation, jinja2, formative-assessment, material-types]

# Dependency graph
requires:
  - phase: 01-01
    provides: SKILL.md skeleton and student_worksheet.docx template
  - phase: 01-03
    provides: Lesson design JSON schema with assessment field
provides:
  - Word document generation from lesson design JSON
  - Material type selection based on lesson type
  - Formative assessment integration (exit ticket, embedded, performance)
  - Combined PPTX and DOCX validation script
affects: [01-06, 02-quality-validation]

# Tech tracking
tech-stack:
  added: []
  patterns: [docxtpl Jinja2 templating, material type mapping, assessment integration]

key-files:
  created:
    - .claude/skills/lesson-designer/scripts/generate_worksheet.py
    - .claude/skills/lesson-designer/scripts/validate_outputs.py
  modified:
    - .claude/skills/lesson-designer/SKILL.md

key-decisions:
  - "Material type maps directly to lesson type (introducing->worksheet, practicing->problem_set, etc.)"
  - "Every document includes assessment: exit_ticket, embedded, or performance task"
  - "validate_outputs.py validates both PPTX and DOCX in single script"

patterns-established:
  - "Material type selection: MATERIAL_TYPE_MAP dictionary for lesson-to-material mapping"
  - "Assessment context: has_exit_ticket, has_embedded_assessment, has_performance_task flags"
  - "Output validation: Combined validation with exit codes (0=pass, 1=warnings, 2=fail)"

# Metrics
duration: 6min
completed: 2026-01-25
---

# Phase 01 Plan 05: Word Document Generation for Student Materials Summary

**docxtpl-based Word generation with material type selection and formative assessment integration, plus combined validation script for both PowerPoint and Word outputs**

## Performance

- **Duration:** 6 minutes
- **Started:** 2026-01-25T21:19:57Z
- **Completed:** 2026-01-25T21:25:58Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Created generate_worksheet.py that produces Word documents from lesson design JSON using docxtpl
- Implemented material type selection that maps lesson types to appropriate formats (worksheet, problem_set, activity_guide)
- Ensured every document includes formative assessment (exit_ticket, embedded, or performance task) per ASMT-01
- Updated SKILL.md Stage 5 with complete document generation instructions and material type table
- Created validate_outputs.py that validates both PowerPoint and Word files with requirement checking

## Task Commits

Each task was committed atomically:

1. **Task 1: Create Word document generation script** - `9f2deb6` (feat)
2. **Task 2: Update SKILL.md with document generation instructions** - `c5ae9ce` (docs)
3. **Task 3: Create output validation script** - `8ce1726` (feat)

## Files Created/Modified

- `.claude/skills/lesson-designer/scripts/generate_worksheet.py` - Main generation script with:
  - `select_material_type()` - Maps lesson type to material format
  - `prepare_template_context()` - Builds Jinja2 context dictionary
  - `format_activities_for_worksheet()` - Formats activities per material type
  - `add_assessment_section()` - Adds appropriate assessment (exit ticket, embedded, performance)
  - `render_template()` - Uses docxtpl to render Word document
  - `validate_output()` - Checks for unrendered tags and required content

- `.claude/skills/lesson-designer/scripts/validate_outputs.py` - Combined validation script with:
  - `validate_pptx()` - Checks hidden slide, minimum slides, font sizes
  - `validate_docx()` - Checks for Jinja2 tags, assessment section, content
  - `generate_validation_report()` - Creates 07_validation_report.txt
  - Exit codes: 0=pass, 1=warnings, 2=fail

- `.claude/skills/lesson-designer/SKILL.md` - Updated Stage 5 with:
  - Complete Word document generation instructions
  - Material type selection table
  - Assessment integration documentation (ASMT-01)
  - Template system explanation
  - Phase 2 formatting enhancement notes

## Decisions Made

**Material type mapping:**
Direct mapping from lesson type to material format:
- introducing -> worksheet (reading + comprehension)
- practicing -> problem_set (practice exercises)
- applying -> worksheet (structured application)
- synthesizing -> activity_guide (project guide)
- novel_application -> problem_set (challenge problems)

**Assessment integration pattern:**
Three assessment types with distinct template handling:
- exit_ticket: Adds exit_ticket dict with title, instructions, questions
- embedded: Sets has_embedded_assessment flag, note about checking work
- performance: Adds performance_task dict with description and success criteria
Default to exit_ticket if unspecified to ensure ASMT-01 compliance.

**Combined validation approach:**
Single validate_outputs.py handles both file types instead of separate scripts. Generates comprehensive report at 07_validation_report.txt with:
- File-by-file status
- Error/warning categorization
- Requirements checklist (SLID-02, SLID-04, MATL-01, ASMT-01, TMPL-01)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Phase 1 Plan 06 (Finalization):**
- generate_worksheet.py creates 06_worksheet.docx from 04_lesson_final.json
- validate_outputs.py validates both 05_slides.pptx and 06_worksheet.docx
- SKILL.md Stage 5 documents both slide and worksheet generation
- Stage 6 documents validation workflow

**Ready for Phase 2 (Quality Validation):**
- Validation framework established with validate_outputs.py
- Requirements checking pattern can be extended
- Exit code semantics match validate_marzano.py

**Blockers/concerns:**
None identified. Word document generation and validation is complete.

---
*Phase: 01-core-lesson-generation*
*Completed: 2026-01-25*
