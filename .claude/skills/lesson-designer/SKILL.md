---
name: lesson-designer
description: Designs classroom-ready lessons using Marzano's New Taxonomy framework, producing slide decks and student worksheets with cognitive rigor validation
version: 1.0.0
author: Claude
---

# Lesson Designer Skill

Design complete, classroom-ready lessons using Robert Marzano's New Taxonomy framework. This skill produces slide decks, student worksheets, and differentiated materials with cognitive rigor validation.

## Workflow Overview

Execute these stages sequentially:

- [ ] **Stage 1: Gather competency requirements**
- [ ] **Stage 2: Decompose into skills and knowledge**
- [ ] **Stage 3: Design lesson with Marzano taxonomy**
- [ ] **Stage 3b: Validate cognitive rigor**
- [ ] **Stage 4: Teacher classification and proficiency targets**
- [ ] **Stage 5: Generate materials (.pptx + .docx)**
- [ ] **Stage 6: Validate outputs**
- [ ] **Stage 7: Present to teacher**

## State Directory Structure

Each lesson session maintains state in `.lesson-designer/sessions/{session_id}/`:

```
.lesson-designer/sessions/{session_id}/
├── state.json              # Current workflow stage and lesson data
├── lesson.json             # Complete lesson plan with activities
├── slide_deck.pptx         # Generated PowerPoint presentation
└── student_worksheet.docx  # Generated Word worksheet
```

Session IDs use format: `YYYYMMDD-HHMMSS-{topic_slug}`

## Framework Reference

**Marzano's New Taxonomy** provides the pedagogical foundation for all lesson designs. See [MARZANO.md](./MARZANO.md) for complete framework documentation including:

- Four cognitive levels (retrieval, comprehension, analysis, knowledge utilization)
- Cognitive rigor requirements (minimum 40% higher-order thinking)
- Activity design templates by level
- JSON schema for lesson validation

## Templates

Base templates for material generation:

- [templates/slide_deck.pptx](./templates/slide_deck.pptx) - PowerPoint template with branded layouts
- [templates/student_worksheet.docx](./templates/student_worksheet.docx) - Word template with Jinja2 placeholders

## Stage Details

### Stage 1: Gather Competency Requirements

**Purpose:** Understand what students need to learn.

**Inputs:** Teacher provides grade level, subject, competency/standard, lesson duration

**Process:**
1. Ask clarifying questions about context
2. Identify prerequisite knowledge
3. Determine lesson scope boundaries
4. Record in state.json

**Outputs:** Structured competency requirements

**Next:** Stage 2

---

### Stage 2: Decompose into Skills and Knowledge

**Purpose:** Break down competency into teachable components.

**Inputs:** Competency requirements from Stage 1

**Process:**
1. Identify specific skills (procedural knowledge)
2. Identify specific knowledge (declarative knowledge)
3. Sequence learning elements
4. Identify potential misconceptions

**Outputs:** Skills and knowledge breakdown

**Next:** Stage 3

---

### Stage 3: Design Lesson with Marzano Taxonomy

**Purpose:** Create complete lesson plan with activities mapped to Marzano levels.

**Inputs:** Skills and knowledge from Stage 2, MARZANO.md framework

**Process:**
1. Design opening/hook activity
2. Create main instructional activities
3. Design practice activities
4. Create closing/assessment activity
5. Map each activity to Marzano cognitive level
6. Assign duration and materials
7. Structure as JSON following schema

**Outputs:** Complete lesson.json with activities

**Next:** Stage 3b

---

### Stage 3b: Validate Cognitive Rigor

**Purpose:** Ensure lesson meets minimum higher-order thinking thresholds.

**Inputs:** lesson.json from Stage 3

**Process:**
1. Calculate percentage of time at each Marzano level
2. Check against thresholds:
   - Minimum 40% higher-order (analysis + knowledge utilization)
   - Maximum 30% retrieval-only
3. If validation fails, return to Stage 3 with specific adjustments
4. If validation passes, proceed

**Outputs:** Validation report

**Next:** Stage 4 (if passed) or Stage 3 (if failed)

---

### Stage 4: Teacher Classification and Proficiency Targets

**Purpose:** Adapt lesson for teacher's experience and set proficiency targets.

**Process:** (To be implemented in Phase 1, Plan 03)

**Outputs:** Teacher-adapted lesson with proficiency targets

**Next:** Stage 5

---

### Stage 5: Generate Materials (.pptx + .docx)

**Purpose:** Create classroom-ready files from lesson plan.

**Process:** (To be implemented in Phase 1, Plan 04-06)

**Outputs:** slide_deck.pptx and student_worksheet.docx

**Next:** Stage 6

---

### Stage 6: Validate Outputs

**Purpose:** Verify generated files meet quality requirements.

**Process:** (To be implemented in Phase 2)

**Outputs:** Validation report

**Next:** Stage 7

---

### Stage 7: Present to Teacher

**Purpose:** Deliver materials and explain lesson structure.

**Process:**
1. Summarize lesson objectives and flow
2. Provide file paths
3. Highlight key instructional moments
4. Explain differentiation opportunities

**Outputs:** Teacher-facing summary

**Next:** Session complete

---

## Usage Example

```
Teacher: I need a 45-minute lesson on photosynthesis for 7th grade.

Claude: I'll use the lesson-designer skill to create this.

[Stage 1] Let me gather some details:
- What specific standard or competency are you targeting?
- What have students already learned about plants?
- What materials/resources are available?

[... workflow continues through all stages ...]

[Stage 7] Lesson complete! Here are your materials:
- slide_deck.pptx: 12 slides with visual diagrams
- student_worksheet.docx: 2-page worksheet with guided practice

The lesson includes 45% higher-order thinking activities...
```

---

**Version:** 1.0.0
**Last updated:** 2026-01-25
**Framework:** [Marzano's New Taxonomy](./MARZANO.md)
