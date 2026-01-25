---
phase: 02-material-quality-formatting
plan: 03
subsystem: material-generation
tags: [p5.js, jinja2, simulations, html, javascript, interactive-learning]

# Dependency graph
requires:
  - phase: 01-core-lesson-generation
    provides: Lesson design schema and file generation patterns
provides:
  - HTML/JS simulation generator for interactive visualizations
  - p5.js simulation template with educational design
  - Three pre-built simulations (supply/demand, velocity, predator-prey)
affects: [Stage 5 - File Generation, MATL-04 requirement]

# Tech tracking
tech-stack:
  added: [p5.js (via CDN), jinja2 template engine]
  patterns: [Keyword-based simulation detection, Self-contained HTML generation, Educational p5.js sketches]

key-files:
  created:
    - .claude/skills/lesson-designer/templates/simulation_template.html
    - .claude/skills/lesson-designer/scripts/generate_simulation.py
  modified: []

key-decisions:
  - "Use p5.js loaded from CDN for zero-install deployment"
  - "Self-contained HTML files (no separate .js files) for easy distribution"
  - "Exit code 0 for non-matching competencies (not an error condition)"
  - "Keyword-based detection rather than ML/LLM classification for predictability"
  - "Three initial simulation types covering economics, physics, and biology"

patterns-established:
  - "Simulation template pattern: Jinja2 HTML template with embedded p5.js sketch"
  - "Detection pattern: Keyword matching in competency text for simulation type"
  - "Graceful degradation: Informational message when no simulation matches"
  - "Educational simulation design: Learning objective prominent, keyboard controls listed, instructions clear"

# Metrics
duration: 4min
completed: 2026-01-25
---

# Phase 02 Plan 03: Interactive Simulation Generator Summary

**p5.js-based HTML simulation generator with three pre-built educational simulations (supply/demand, velocity, predator-prey) and self-contained single-file output**

## Performance

- **Duration:** 4 min
- **Started:** 2026-01-25T23:33:35Z
- **Completed:** 2026-01-25T23:37:56Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Created Jinja2 HTML template with p5.js CDN integration and educational design system
- Built simulation generator with keyword detection for economics, physics, and biology topics
- Generated self-contained HTML files with embedded JavaScript (no multi-file deployment)
- Graceful handling of non-matching competencies with exit code 0

## Task Commits

Each task was committed atomically:

1. **Task 1: Create simulation HTML template** - `ef38682` (feat)
2. **Task 2: Create simulation generator script** - `10422bd` (feat)

## Files Created/Modified
- `.claude/skills/lesson-designer/templates/simulation_template.html` - Jinja2 template with p5.js CDN, learning objective section, keyboard controls list, and design system colors (#2D5A87 blue, #F4D03F gold)
- `.claude/skills/lesson-designer/scripts/generate_simulation.py` - CLI generator with keyword detection, three pre-built p5.js sketches (supply_demand, velocity, ecosystem), and graceful non-match handling

## Decisions Made

**p5.js via CDN (not npm package):**
- Rationale: Self-contained HTML files are easier to distribute to students. No build step required. CDN provides caching and reliability.
- Alternative considered: Local p5.js bundle would work offline but require multi-file distribution

**Keyword detection (not LLM classification):**
- Rationale: Predictable, fast, and transparent. Teachers can see which keywords trigger which simulations. No API calls or model uncertainty.
- Alternative considered: LLM could classify competencies into simulation types, but adds complexity and latency

**Exit code 0 for non-matches:**
- Rationale: "No simulation needed" is not an error condition. Allows pipeline to continue without treating missing simulation as failure.
- Alternative considered: Exit 1 would require special handling in workflow scripts

**Three initial simulation types:**
- Rationale: Cover major subject areas (economics, physics, biology). Proven educational topics that benefit from visualization. Can expand based on usage patterns.
- Alternative considered: Could start with just one, but three demonstrates pattern generalizability

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## Next Phase Readiness

**Material generation infrastructure complete:**
- Worksheets (01-05): Line spacing and compact formatting ✓
- Slides (01-04): Teacher notes and sparse content ✓
- Discussions (02-02): Facilitation notes with time allocations ✓
- Simulations (02-03): Interactive HTML/JS programs ✓

**Ready for Phase 3 (Single Persona Feedback):**
- File generators can produce all material types
- Quality standards established (formatting, accessibility, pedagogy)
- Validation infrastructure exists for all output types

**Simulation expansion path:**
- Current: 3 simulations (economics, physics, biology)
- Future: Chemistry (molecular models), Math (function graphing), Geography (climate patterns)
- Pattern established for adding new simulation types to SIMULATION_TEMPLATES dict

---
*Phase: 02-material-quality-formatting*
*Completed: 2026-01-25*
