# Requirements: Lesson Designer

**Defined:** 2025-01-25
**Core Value:** Produce classroom-ready materials that actually work for teaching — slides that support instruction, worksheets with room to write, discussions with clear structure, and differentiation built in from the start.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Competency Planning

- [ ] **COMP-01**: Teacher can choose to plan for a single competency or a series of competencies
- [ ] **COMP-02**: Teacher can specify number of lessons per competency and lesson length (50 min, 60 min, etc.)
- [ ] **COMP-03**: Tool decomposes each competency into the skill involved and the required factual knowledge
- [ ] **COMP-04**: Teacher can classify each knowledge item as "needs teaching" or "already assumed"
- [ ] **COMP-05**: Teacher can define target proficiency level after the lesson/sequence

### Marzano Framework

- [ ] **MARZ-01**: Lessons are structured according to Marzano's taxonomy (retrieval → comprehension → analysis → knowledge utilization)
- [ ] **MARZ-02**: Tasks are aligned to lesson type (introducing skills/knowledge, practicing, applying, synthesizing, novel application)
- [ ] **MARZ-03**: Tool enforces cognitive rigor with minimum higher-order thinking activities (not just recall/regurgitation)

### Student Persona Feedback

- [ ] **PERS-01**: Tool runs lesson designs through 4 student personas (struggling/ELL, unmotivated capable, interested capable, high-achieving)
- [ ] **PERS-02**: Each persona provides a reaction describing how they would likely respond to the lesson
- [ ] **PERS-03**: Each persona provides specific pedagogical recommendations to improve the lesson for their needs
- [ ] **PERS-04**: Tool proposes revisions based on persona feedback; teacher confirms before finalizing

### Slide Deck Generation

- [ ] **SLID-01**: Tool generates actual .pptx PowerPoint files
- [ ] **SLID-02**: Each deck includes a hidden first slide with lesson plan (objective, agenda with timing, anticipated misconceptions, delivery tips)
- [ ] **SLID-03**: Slides use sparse, teacher-led format (talking points and visual prompts, not dense self-study text)
- [ ] **SLID-04**: All slide text uses 16pt font minimum for classroom readability

### Student Materials

- [ ] **MATL-01**: Tool generates actual .docx Word documents for student materials
- [ ] **MATL-02**: Worksheets use double-spaced lines with adequate space for student writing
- [ ] **MATL-03**: Tool produces appropriate material type for the lesson (worksheets, readings, problem sets, activity descriptions, simulation materials)
- [ ] **MATL-04**: Tool can generate HTML/JS simulation programs when appropriate for the competency

### Discussion & Collaboration

- [ ] **DISC-01**: Discussion activities include explicit time allocations for pair/group work
- [ ] **DISC-02**: Discussion activities include structure (opening, prompts, closing)
- [ ] **DISC-03**: Discussion activities include teacher facilitation guidance

### Assessment

- [ ] **ASMT-01**: Each lesson includes assessment of its objective (embedded in student work or as exit ticket)
- [ ] **ASMT-02**: Tool can generate dedicated assessment lessons (quizzes, tests)
- [ ] **ASMT-03**: Tool can generate graded Socratic discussion guides
- [ ] **ASMT-04**: Tool can generate performance tasks with rubrics

### Multi-Lesson Sequences

- [ ] **SEQN-01**: Teacher can plan multiple lessons for a competency or series of competencies
- [ ] **SEQN-02**: Lessons within a sequence build on each other with logical progression
- [ ] **SEQN-03**: Tool maintains context awareness across lessons (knows what came before when designing next lesson)
- [ ] **SEQN-04**: Tool can generate sequence-level assessments covering multiple lessons

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Standards Alignment

- **STND-01**: Lessons automatically align to Common Core standards
- **STND-02**: Lessons can align to state-specific standards
- **STND-03**: Standards alignment is visible in lesson plan

### Advanced Differentiation

- **DIFF-01**: Tool generates tiered versions of activities (basic, proficient, advanced)
- **DIFF-02**: Tool generates scaffolded supports for struggling learners
- **DIFF-03**: Tool generates extension activities for advanced learners

### Visual Content

- **VISL-01**: Tool generates or suggests relevant images/diagrams
- **VISL-02**: Tool creates data visualizations when appropriate

### Distribution

- **DIST-01**: Skill can be shared with other teachers
- **DIST-02**: Templates can be customized per teacher/school

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Learning Management System (LMS) features | Scope creep; integrate with existing LMS platforms instead |
| Pre-built lesson library | Teachers want customization, not canned lessons |
| Mobile app | Claude skill runs in Claude interface; no separate app needed |
| Real-time collaboration | Basic sharing sufficient for v1; Claude skill doesn't support real-time editing |
| Generic AI generation without framework | The whole point is Marzano-guided design, not generic output |
| Non-academic subjects (PE, art, music) | Scoped to academic subjects only for v1 |
| Overly detailed slides | This is an anti-feature; the known pain point we're solving |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| COMP-01 | Phase 1 | Complete |
| COMP-02 | Phase 1 | Complete |
| COMP-03 | Phase 1 | Complete |
| COMP-04 | Phase 1 | Complete |
| COMP-05 | Phase 1 | Complete |
| MARZ-01 | Phase 1 | Complete |
| MARZ-02 | Phase 1 | Complete |
| MARZ-03 | Phase 1 | Complete |
| PERS-01 | Phase 3, Phase 4 | Partial (1/4 personas) |
| PERS-02 | Phase 3 | Complete |
| PERS-03 | Phase 3 | Complete |
| PERS-04 | Phase 3 | Complete |
| SLID-01 | Phase 1 | Complete |
| SLID-02 | Phase 1 | Complete |
| SLID-03 | Phase 1 | Complete |
| SLID-04 | Phase 1 | Complete |
| MATL-01 | Phase 1 | Complete |
| MATL-02 | Phase 2 | Complete |
| MATL-03 | Phase 1 | Complete |
| MATL-04 | Phase 2 | Complete |
| DISC-01 | Phase 2 | Complete |
| DISC-02 | Phase 2 | Complete |
| DISC-03 | Phase 2 | Complete |
| ASMT-01 | Phase 1 | Complete |
| ASMT-02 | Phase 2 | Complete |
| ASMT-03 | Phase 2 | Complete |
| ASMT-04 | Phase 2 | Complete |
| SEQN-01 | Phase 5 | Pending |
| SEQN-02 | Phase 5 | Pending |
| SEQN-03 | Phase 5 | Pending |
| SEQN-04 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 31 total
- Mapped to phases: 31 (100% coverage)
- Unmapped: 0

**Notes:**
- PERS-01 is partially implemented in Phase 3 (1 persona) and completed in Phase 4 (all 4 personas)
- All other requirements map to exactly one phase

---
*Requirements defined: 2025-01-25*
*Last updated: 2026-01-26 — Phase 3 requirements complete (PERS-02, PERS-03, PERS-04), PERS-01 partial*
