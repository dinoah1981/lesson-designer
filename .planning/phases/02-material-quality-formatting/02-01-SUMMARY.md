---
phase: 02-material-quality-formatting
plan: 01
subsystem: document-generation
completed: 2026-01-25
duration: 4min
tags: [python-docx, formatting, accessibility, cognitive-design]

requires:
  - phase: 01
    plan: 05
    what: generate_worksheet.py script foundation

provides:
  - Double-spaced student worksheets with adequate writing space
  - Cognitive complexity-based answer space allocation
  - Validation for adequate spacing

affects:
  - phase: 02
    plan: future
    how: Sets formatting standards for all document generators

tech-stack:
  added: []
  patterns:
    - Float multiplier line spacing (2.0) for proportional scaling
    - Configuration-driven content generation (WRITING_SPACE_CONFIG)
    - Validation checks for formatting quality

key-files:
  created: []
  modified:
    - .claude/skills/lesson-designer/scripts/generate_worksheet.py

decisions:
  - what: Use float multiplier (2.0) instead of WD_LINE_SPACING.DOUBLE enum
    why: Ensures spacing scales with font size changes
    impact: More accessible for vision-impaired users who may adjust fonts

  - what: Variable answer space by Marzano level (2-6 lines)
    why: Higher-order thinking requires more space for complex responses
    impact: Students get appropriate space for cognitive complexity

  - what: Exit ticket gets 4 lines per question
    why: Exit tickets are critical assessment - need adequate reflection space
    impact: Better quality exit ticket responses
---

# Phase 2 Plan 01: Enhanced Worksheet Line Spacing Summary

**One-liner:** Double-spaced worksheets with cognitive complexity-based answer space using float multiplier line spacing

## What Was Built

Enhanced the existing `generate_worksheet.py` script to provide proper double-spacing and adequate writing space for student responses. This addresses MATL-02 requirement directly.

**Key enhancements:**
1. **Double-spaced answer lines** using `line_spacing = 2.0` (float multiplier, not fixed Pt)
2. **Configuration-based writing space** that scales with cognitive complexity:
   - Retrieval: 2 lines (quick recall)
   - Comprehension: 3 lines (moderate explanations)
   - Analysis: 5 lines (detailed responses)
   - Knowledge_utilization: 6 lines (complex responses)
3. **Exit ticket gets 4 lines** per question (critical assessment)
4. **Validation checks** ensure double-spacing is applied (warns if <50% of answer lines have spacing >= 1.5)

**Files modified:**
- `.claude/skills/lesson-designer/scripts/generate_worksheet.py` (58 lines changed)

## How It Works

**Line spacing implementation:**
```python
# Uses float multiplier (2.0) not fixed Pt value
p.paragraph_format.line_spacing = 2.0  # Double-spaced
```

This ensures spacing scales proportionally with font size changes, per RESEARCH.md guidance. Critical for accessibility.

**Writing space configuration:**
```python
WRITING_SPACE_CONFIG = {
    'retrieval': 2,
    'comprehension': 3,
    'analysis': 5,
    'knowledge_utilization': 6,
    'default': 3
}

# Usage in generate_worksheet_from_lesson():
answer_line_count = WRITING_SPACE_CONFIG.get(marzano_level, WRITING_SPACE_CONFIG['default'])
add_answer_lines(doc, answer_line_count)
```

Activities automatically get appropriate answer space based on their Marzano cognitive level.

**Validation:**
The `validate_output()` function now checks:
- At least 50% of answer lines have spacing >= 1.5
- Warns if document lacks answer lines entirely

## Deviations from Plan

None - plan executed exactly as written.

## Decisions Made

### 1. Float Multiplier vs Enum for Line Spacing

**Decision:** Use `line_spacing = 2.0` instead of `line_spacing_rule = WD_LINE_SPACING.DOUBLE`

**Rationale:** Float multipliers scale proportionally with font size. If a student with vision impairment increases font to 14pt, the spacing scales automatically. Fixed enum values don't scale.

**Source:** 02-RESEARCH.md (Pattern 1, Anti-Pattern 1)

**Impact:** Worksheets are more accessible and maintain proper spacing across different font sizes.

### 2. Cognitive Complexity-Based Line Counts

**Decision:** Allocate 2-6 answer lines based on Marzano level

**Rationale:**
- Retrieval activities need minimal space (2 lines) for quick recall
- Analysis/knowledge_utilization need substantial space (5-6 lines) for complex reasoning
- Matches cognitive demands of each activity type

**Impact:** Students get appropriate space for the thinking required. No more cramped analysis responses or excessive blank space on recall questions.

### 3. Exit Ticket Space Allocation

**Decision:** 4 lines per exit ticket question (fixed, not variable by Marzano level)

**Rationale:** Exit tickets are critical formative assessment. Teachers need substantial student responses to gauge understanding, regardless of question complexity.

**Impact:** More thoughtful exit ticket responses with adequate reflection space.

## Testing & Validation

**Test execution:**
```bash
python generate_worksheet.py sample_lesson.json test_double_spaced.docx
```

**Validation results:**
- Tables: 2 (header table + content tables)
- Answer lines: 28 total
- Double-spaced lines: 28/28 (100% ratio)
- No warnings or errors

**Visual inspection:** Answer lines are visibly double-spaced with adequate room for student handwriting.

## Known Issues

None.

## Next Phase Readiness

**Phase 2 continuation:**
- Formatting standards established for document generation
- Configuration pattern (WRITING_SPACE_CONFIG) can extend to other material types
- Validation pattern established for checking formatting quality

**Future plans:**
- 02-02: Discussion activity structure and facilitation notes
- 02-03: HTML/JS simulation generation
- 02-04: Assessment lesson types (quizzes, rubrics)

No blockers for Phase 2 continuation.

## Performance Notes

**Execution time:** 4 minutes

**Breakdown:**
- Task 1 (line spacing implementation): ~2 minutes
- Task 2 (configuration + validation): ~2 minutes

**Code quality:**
- 2 atomic commits (1 per task)
- Clean separation of concerns
- Backward compatible (all parameters have defaults)

## Lessons Learned

**What went well:**
- Float multiplier approach (2.0) works perfectly for proportional scaling
- Configuration dictionary provides clear, maintainable control over behavior
- Validation catches spacing issues immediately

**What to improve:**
- Consider making WRITING_SPACE_CONFIG user-configurable in future (teacher preferences may vary)
- May need to add margin configuration for different page sizes (currently assumes 8.5x11)

**Reusable patterns:**
- Configuration-driven formatting (can apply to font sizes, margins, etc.)
- Validation checks for formatting properties
- Float multipliers for proportional values

## Links

**Phase documentation:**
- Phase overview: `.planning/phases/02-material-quality-formatting/02-PHASE.md`
- Research: `.planning/phases/02-material-quality-formatting/02-RESEARCH.md`
- This plan: `.planning/phases/02-material-quality-formatting/02-01-PLAN.md`

**Related code:**
- Modified: `.claude/skills/lesson-designer/scripts/generate_worksheet.py`
- Test fixture: `.claude/skills/lesson-designer/tests/sample_lesson.json`

**Requirements satisfied:**
- MATL-02: Worksheets use double-spaced lines with adequate space for student writing ✓
- Answer space scales with cognitive complexity ✓
- No regressions in existing worksheet generation ✓

---
*Summary generated: 2026-01-25*
*Plan executed by: Claude Opus 4.5*
