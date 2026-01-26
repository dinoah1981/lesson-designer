# Roadmap: Lesson Designer

## Overview

This roadmap delivers a Marzano-based lesson planning skill that transforms teacher competencies into classroom-ready materials. We start with end-to-end value (competency to materials) in Phase 1, add quality refinements in Phase 2, introduce feedback loops in Phases 3-4 (starting with one persona before scaling to four), and expand to multi-lesson sequences in Phase 5. Each phase delivers observable, verifiable capabilities that build toward production-ready materials.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Core Lesson Generation** - Single competency to complete materials
- [x] **Phase 2: Material Quality & Formatting** - Worksheets, discussions, assessment variety
- [x] **Phase 3: Single Persona Feedback** - Struggling learner feedback loop
- [x] **Phase 4: Multi-Persona Validation** - Full 4-persona feedback system
- [x] **Phase 5: Multi-Lesson Sequences** - Context awareness & sequence planning

## Phase Details

### Phase 1: Core Lesson Generation
**Goal**: Teacher provides single competency and receives classroom-ready slide deck (.pptx), student materials (.docx), and lesson plan that address known pain points (sparse slides, proper formatting, embedded assessment).

**Depends on**: Nothing (first phase)

**Requirements**: COMP-01, COMP-02, COMP-03, COMP-04, COMP-05, MARZ-01, MARZ-02, MARZ-03, SLID-01, SLID-02, SLID-03, SLID-04, MATL-01, MATL-03, ASMT-01

**Success Criteria** (what must be TRUE):
  1. Teacher can input single competency with lesson count and duration, and receive decomposition into skills and knowledge
  2. Teacher can classify knowledge items as "needs teaching" or "already assumed" and define target proficiency
  3. Generated slides (.pptx) use sparse, teacher-led format (16pt minimum, talking points not paragraphs) with hidden first slide containing lesson plan
  4. Generated student materials (.docx) match lesson type (worksheets, readings, problem sets) and support Marzano taxonomy levels
  5. Each lesson includes formative assessment embedded in student work or as exit ticket
  6. All materials align to Marzano taxonomy with enforced cognitive rigor (not just recall)

**Plans**: 6 plans

Plans:
- [x] 01-01-PLAN.md — Skill structure, Marzano framework, and templates
- [x] 01-02-PLAN.md — Teacher input and competency decomposition
- [x] 01-03-PLAN.md — Marzano-based lesson design and validation
- [x] 01-04-PLAN.md — PowerPoint generation with sparse format
- [x] 01-05-PLAN.md — Word document generation with assessment
- [x] 01-06-PLAN.md — Integration and verification checkpoint

### Phase 2: Material Quality & Formatting
**Goal**: Materials are physically usable and pedagogically complete with proper formatting, discussion structure, and diverse assessment types.

**Depends on**: Phase 1

**Requirements**: MATL-02, MATL-04, DISC-01, DISC-02, DISC-03, ASMT-02, ASMT-03, ASMT-04

**Success Criteria** (what must be TRUE):
  1. Worksheets use double-spaced lines with adequate space for student writing
  2. Discussion activities include explicit time allocations (e.g., 10-15 min), opening/prompts/closing structure, and teacher facilitation guidance
  3. Tool can generate HTML/JS simulation programs when appropriate for the competency
  4. Tool can generate dedicated assessment lessons including quizzes, tests, graded Socratic discussions with guides, and performance tasks with rubrics
  5. All material types (worksheets, readings, problem sets, simulations, activity descriptions) are properly formatted for their purpose

**Plans**: 5 plans in 2 waves

Plans:
- [x] 02-01-PLAN.md — Worksheet double-spacing and writing space configuration
- [x] 02-02-PLAN.md — Discussion slide structure with time allocations and facilitation notes
- [x] 02-03-PLAN.md — HTML/JS simulation generator with p5.js
- [x] 02-04-PLAN.md — Assessment generator for quizzes, tests, Socratic guides, and performance tasks
- [x] 02-05-PLAN.md — Validation updates and integration checkpoint

### Phase 3: Single Persona Feedback
**Goal**: Lesson designs are validated through struggling learner persona before finalization, with teacher-approved revisions.

**Depends on**: Phase 2

**Requirements**: PERS-01 (partial - 1 persona only), PERS-02, PERS-03, PERS-04

**Success Criteria** (what must be TRUE):
  1. Tool runs lesson design through struggling learner persona (literacy challenges or ELL)
  2. Persona provides reaction describing likely response to the lesson
  3. Persona provides specific pedagogical recommendations to improve lesson for their needs
  4. Tool proposes revisions based on feedback; teacher confirms before finalizing
  5. Feedback loop architecture is proven and ready to scale to additional personas

**Plans**: 3 plans in 3 waves

Plans:
- [x] 03-01-PLAN.md — Persona definition and parameterized evaluator script
- [x] 03-02-PLAN.md — Revision plan generator and workflow integration
- [x] 03-03-PLAN.md — End-to-end verification with teacher approval checkpoint

### Phase 4: Multi-Persona Validation
**Goal**: Comprehensive pedagogical validation through 4 diverse student personas covering access, motivation, engagement, and ceiling issues.

**Depends on**: Phase 3

**Requirements**: PERS-01 (complete - all 4 personas)

**Success Criteria** (what must be TRUE):
  1. Tool runs lesson designs through all 4 student personas: struggling/ELL, unmotivated capable, interested capable, high-achieving
  2. Each persona provides independent reaction and pedagogical recommendations
  3. Tool synthesizes feedback from all personas, handling conflicting recommendations
  4. Teacher receives aggregated revision proposal addressing needs across all learner types
  5. Lessons are differentiated to work for diverse learners before teaching

**Plans**: 3 plans in 2 waves

Plans:
- [x] 04-01-PLAN.md — Create 3 new persona definitions (Jordan, Maya, Marcus)
- [x] 04-02-PLAN.md — Create run_multi_persona.py orchestrator
- [x] 04-03-PLAN.md — Add conflict detection/synthesis + SKILL.md + verification

### Phase 5: Multi-Lesson Sequences
**Goal**: Teachers can plan coherent 2-4 week units with lesson interdependencies, skill progression, and context awareness across the sequence.

**Depends on**: Phase 4

**Requirements**: SEQN-01, SEQN-02, SEQN-03, SEQN-04

**Success Criteria** (what must be TRUE):
  1. Teacher can plan multiple lessons for a competency or series of competencies
  2. Lessons within a sequence build on each other with logical progression
  3. Tool maintains context awareness across lessons (knows what came before when designing next lesson)
  4. Tool can generate sequence-level assessments covering multiple lessons
  5. Context management prevents quality degradation from Lesson 1 to Lesson 10 (compression, essence summaries, terminology tracking)

**Plans**: 4 plans in 3 waves

Plans:
- [x] 05-01-PLAN.md — Sequence session management and metadata schema
- [x] 05-02-PLAN.md — Context assembly and vocabulary continuity tracking
- [x] 05-03-PLAN.md — Sequence-level assessment generation
- [x] 05-04-PLAN.md — SKILL.md update and end-to-end integration

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Lesson Generation | 6/6 | Complete | 2026-01-25 |
| 2. Material Quality & Formatting | 5/5 | Complete | 2026-01-25 |
| 3. Single Persona Feedback | 3/3 | Complete | 2026-01-26 |
| 4. Multi-Persona Validation | 3/3 | Complete | 2026-01-26 |
| 5. Multi-Lesson Sequences | 4/4 | Complete | 2026-01-26 |

---
*Roadmap created: 2025-01-25*
*Last updated: 2026-01-26 — Phase 5 complete (all 5 phases done)*
