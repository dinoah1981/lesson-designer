# Lesson Designer

## What This Is

A Claude skill that helps teachers design pedagogically sound lessons using Marzano's framework. Teachers define competencies, and the tool produces complete, ready-to-use materials — slide decks (.pptx), student materials (.docx), and assessments — that work for diverse learners. It supports single lessons or multi-lesson sequences, and runs designs through simulated student personas to catch issues before teaching.

## Core Value

Produce classroom-ready materials that actually work for teaching — slides that support instruction (not replace it), worksheets with room to write, discussions with clear structure, and differentiation built in from the start.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Competency-Based Planning**
- [ ] Ask whether planning for one competency or a series
- [ ] Confirm number of lessons per competency
- [ ] Accept lesson length (50 min, 60 min, etc.)
- [ ] Design materials for all periods needed

**Skill & Knowledge Decomposition**
- [ ] Prompt teacher to identify the skill involved in a competency
- [ ] Suggest essential factual knowledge required for the skill
- [ ] Allow teacher to classify each knowledge item: needs teaching, already assumed, or adjust
- [ ] Define target skill proficiency level after lesson/sequence

**Marzano Framework Integration**
- [ ] Scaffold lesson design using Marzano's taxonomy
- [ ] Align tasks to lesson type: introducing skills/knowledge, practicing, applying, synthesizing, novel application
- [ ] Ensure competencies target skills (not pure knowledge regurgitation)

**Student Persona Feedback Loop**
- [ ] Run initial lesson design through 4 student personas
- [ ] Persona 1: Struggling student (literacy challenges or ELL)
- [ ] Persona 2: Capable but unmotivated/disinterested student
- [ ] Persona 3: Capable and genuinely interested student
- [ ] Persona 4: High-achieving student who may not be challenged
- [ ] Each persona provides: likely reaction + specific pedagogical recommendations
- [ ] Propose revisions based on feedback
- [ ] Allow teacher to confirm revisions before finalizing

**Lesson Materials — Slide Deck**
- [ ] Generate actual .pptx files
- [ ] Hidden first slide with: lesson plan, objective, agenda with timing, anticipated misconceptions, delivery tips
- [ ] Slides are sparse teaching supports (not self-study materials)
- [ ] 16pt font minimum
- [ ] Content supports teacher-led instruction, not detailed text for students to read alone

**Lesson Materials — Student Materials**
- [ ] Generate actual .docx files
- [ ] Worksheet/handouts with proper formatting (double-spaced lines for writing)
- [ ] Support various material types: worksheets, readings, problem sets, simulation materials, activity descriptions
- [ ] Small HTML/JS computer programs for simulations when appropriate

**Discussion & Collaboration Structure**
- [ ] Include explicit pair/group discussion timing
- [ ] Provide structure for how discussions should run
- [ ] Guidance for teacher facilitation

**Formative Assessment**
- [ ] Each lesson assesses its objective
- [ ] Assessment embedded in student work or as exit ticket
- [ ] Teacher knows if students learned

**Summative Assessment Lessons**
- [ ] Design dedicated assessment lessons when needed
- [ ] Support: quizzes, tests, graded Socratic discussions, performance tasks
- [ ] Include rubrics for performance tasks

**Context Awareness**
- [ ] Read existing unit materials to understand previous lessons
- [ ] Maintain coherence across lesson sequences

### Out of Scope

- Mobile app or web app — this is a Claude skill, not standalone software
- Non-academic subjects (PE, art, music, vocational) — academic subjects only
- Distribution to other teachers — future consideration after tool is solid
- Learning management system integration — out of scope for v1

## Context

**Background:**
- Teacher has existing Claude skill that produces slide decks and worksheets for single lessons
- Current skill works for economics, geography, and government courses
- Pain points with current tool:
  - Slides are too detailed (written for self-study, not teacher-led instruction)
  - Worksheets have single-spaced lines (not enough room to write)
  - No structure or timing for pair/group discussions
- What works well:
  - Solid, often interactive lesson ideas
  - Appropriate font sizes (16pt+)
  - Can read existing unit context from file locations

**Pedagogical Foundation:**
- Robert Marzano's framework for lesson and task design
- Lesson types: introducing new skills, introducing knowledge, practicing skills, applying knowledge, synthesizing knowledge and skills, applying in novel contexts
- Distinction between skills (what students do) and knowledge (what students need to know to do it)

**Student Personas for Feedback:**
1. Struggling learner (literacy challenges or limited English)
2. Solid academic skills but unmotivated/disinterested
3. Solid academic skills and genuinely interested
4. High-achieving with strong content knowledge (may not be challenged)

## Constraints

- **Platform**: Claude skill (prompt-based tool, not standalone application)
- **Output format**: Must produce actual .pptx and .docx files, not markdown
- **Subject scope**: Any academic subject (not limited to social studies)
- **User scope**: Personal use initially; future expansion to other teachers is deferred

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Competency-based (not topic-based) | Focuses on what students should be able to DO, not just what they learn about | — Pending |
| Four student personas | Covers access (struggling), motivation (disengaged), engagement (interested), ceiling (advanced) | — Pending |
| Marzano framework | Established pedagogical foundation with clear lesson type taxonomy | — Pending |
| Actual file output (.pptx, .docx) | Teachers need ready-to-use materials, not markdown to convert | — Pending |
| Persona feedback as revision loop | Quality gate that actively shapes design, not just informational | — Pending |

---
*Last updated: 2025-01-25 after initialization*
