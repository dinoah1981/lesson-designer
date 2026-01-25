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

**Purpose:** Collect all information needed to design a competency-focused lesson.

> **Scope Note:** This tool designs lessons for one competency at a time. Multi-lesson sequences across different competencies are planned for a future update.

**Process:**

1. **Ask the teacher these 5 questions:**

   ```
   1. What competency do you want students to master?
      (The skill they will demonstrate - state it as what students will DO)

   2. What grade level are the students?
      (e.g., "7th grade", "AP", "College freshman")

   3. How many lessons do you want to dedicate to this competency?
      (default: 1 if not specified)

   4. How long is each lesson period?
      (e.g., 50 min, 60 min, 90 min)

   5. Are there any constraints I should know about?
      (available materials, time of year, student background, etc.)
   ```

2. **Validate the competency statement:**

   Competencies must be **skill-focused** (what students will DO), not **topic-focused** (what they will learn about).

   **Good examples (skill-focused):**
   - "Students will analyze primary sources to evaluate historical claims"
   - "Students will apply the quadratic formula to solve real-world problems"
   - "Students will construct arguments using evidence from multiple texts"

   **Bad examples (topic-focused) - help teacher reframe:**
   - "The Civil War" → Ask: "What skill do you want students to demonstrate with Civil War content?"
   - "Photosynthesis" → Ask: "What should students be able to DO with their knowledge of photosynthesis?"
   - "Fractions" → Ask: "What fraction operations should students master?"

   **Reframing prompt when needed:**
   > "I see you've given me a topic. To create the best lesson, I need to know what skill students should demonstrate. For example, with [topic], should they be able to [analyze/compare/create/evaluate/apply] something specific?"

3. **Create session directory:**

   ```python
   import sys
   sys.path.insert(0, '.claude/skills/lesson-designer/scripts')
   from parse_competency import generate_session_id, create_session_directory, save_input

   session_id = generate_session_id()
   create_session_directory(session_id)
   ```

4. **Save input to `01_input.json`:**

   ```python
   input_data = {
       "session_id": session_id,
       "competency": "Students will analyze primary sources to evaluate historical claims",
       "grade_level": "8th grade",
       "lesson_count": 2,
       "lesson_duration": 55,
       "constraints": "Students have limited access to technology; need paper-based activities"
   }
   save_input(session_id, input_data)
   ```

**Input JSON Schema (`01_input.json`):**

```json
{
  "session_id": "string (UUID)",
  "competency": "string (skill statement - what students will DO)",
  "grade_level": "string (e.g., '7th grade', 'AP', 'College')",
  "lesson_count": "integer (1 or more, default 1)",
  "lesson_duration": "integer (minutes per lesson period)",
  "constraints": "string or null (any limiting factors)",
  "created_at": "string (ISO 8601 timestamp)"
}
```

**Example Conversation:**

```
Teacher: I want to teach about the Civil War for my 8th graders.

Claude: Great topic! To create the best lesson, I need to know what skill
students should demonstrate. With the Civil War, should they be able to:
- Analyze primary sources from the era?
- Compare perspectives of different groups?
- Evaluate the causes and effects?
- Something else?

Teacher: I want them to analyze primary sources to understand different
perspectives on the war.

Claude: Perfect. So the competency is: "Students will analyze primary sources
to identify and compare different perspectives on the Civil War."

Let me gather a few more details:
- How many lessons do you want to dedicate to this? (I'll design for 1 unless you say more)
- How long is each class period?
- Any constraints I should know about - available materials, what they already know, etc.?

Teacher: Let's do 2 lessons, 55 minutes each. They have access to Chromebooks
but the school has a limited printing budget.

Claude: Got it! Here's what I have:

- **Competency:** Students will analyze primary sources to identify and compare
  different perspectives on the Civil War
- **Grade Level:** 8th grade
- **Lessons:** 2 lessons at 55 minutes each
- **Constraints:** Chromebook access available; limited printing budget

Creating your lesson session now...

[Creates session and saves 01_input.json]

Moving to Stage 2: I'll now decompose this competency into the specific skills
and knowledge students need...
```

**Outputs:**
- Session directory created at `.lesson-designer/sessions/{session_id}/`
- `01_input.json` saved with validated competency requirements

**Requirements Covered:**
- COMP-01: Single competency supported (series acknowledged as future)
- COMP-02: Lesson count and duration captured

**Next:** Stage 2

---

### Stage 2: Decompose into Skills and Knowledge

**Purpose:** Break down the competency into teachable components - the skill students will demonstrate and the knowledge required to perform it.

**Inputs:** Competency requirements from Stage 1 (`01_input.json`)

**Process:**

1. **Load input from Stage 1:**

   ```python
   import sys
   sys.path.insert(0, '.claude/skills/lesson-designer/scripts')
   from parse_competency import load_input, save_breakdown

   input_data = load_input(session_id)
   competency = input_data['competency']
   ```

2. **Decompose the competency into skill + knowledge:**

   Every competency has two parts:
   - **The Skill** - What students will DO (verb + object)
   - **Required Knowledge** - What students need to KNOW to perform the skill

   **Decomposition process:**

   a. Identify the main verb (the skill action): analyze, evaluate, construct, compare, apply, etc.

   b. Identify the object (what the verb acts on): primary sources, arguments, equations, etc.

   c. List all factual knowledge required to perform the skill successfully

   **Example decomposition:**

   ```
   Competency: "Students will analyze primary sources to evaluate historical claims"

   Skill:
   - Verb: evaluate
   - Object: historical claims
   - Full statement: "Evaluate historical claims using primary source evidence"

   Required Knowledge:
   K1: What primary sources are (definition, types)
   K2: How to identify bias in sources
   K3: What constitutes evidence vs. opinion
   K4: Historical context of the period being studied
   K5: How to cite sources properly
   ```

3. **Present decomposition to teacher for review:**

   ```
   I've broken down the competency like this:

   **The Skill:**
   Evaluate historical claims using primary source evidence

   **Required Knowledge (what students need to know):**
   1. What primary sources are (definition, types)
   2. How to identify bias in sources
   3. What constitutes evidence vs. opinion
   4. Historical context of the period being studied
   5. How to cite sources properly

   Does this look right? Would you add or remove anything?
   ```

   Wait for teacher confirmation or adjustments before proceeding.

4. **Save decomposition to `02_competency_breakdown.json`:**

   ```python
   breakdown_data = {
       "skill": {
           "verb": "evaluate",
           "object": "historical claims",
           "full_statement": "Evaluate historical claims using primary source evidence"
       },
       "required_knowledge": [
           {"id": "K1", "item": "What primary sources are (definition, types)", "classification": None},
           {"id": "K2", "item": "How to identify bias in sources", "classification": None},
           {"id": "K3", "item": "What constitutes evidence vs. opinion", "classification": None},
           {"id": "K4", "item": "Historical context of the period being studied", "classification": None},
           {"id": "K5", "item": "How to cite sources properly", "classification": None}
       ]
   }
   save_breakdown(session_id, breakdown_data)
   ```

**Breakdown JSON Schema (`02_competency_breakdown.json`):**

```json
{
  "skill": {
    "verb": "string (action verb - analyze, evaluate, construct, etc.)",
    "object": "string (what the verb acts on)",
    "full_statement": "string (complete skill statement)"
  },
  "required_knowledge": [
    {
      "id": "string (K1, K2, etc.)",
      "item": "string (what students need to know)",
      "classification": "string or null (set in Stage 2b)"
    }
  ]
}
```

**Utility Script:** See [scripts/parse_competency.py](./scripts/parse_competency.py) for session management functions:
- `generate_session_id()` - Creates UUID for session
- `create_session_directory(session_id)` - Creates session folder
- `save_input(session_id, input_data)` - Saves Stage 1 input
- `load_input(session_id)` - Loads Stage 1 input
- `save_breakdown(session_id, breakdown_data)` - Saves Stage 2 breakdown
- `load_breakdown(session_id)` - Loads Stage 2 breakdown

**Outputs:**
- `02_competency_breakdown.json` saved in session directory
- Teacher-approved decomposition of skill + required knowledge

**Requirements Covered:**
- COMP-03: Decompose competency into skill + knowledge

**Next:** Stage 2b

---

### Stage 3: Design Lesson with Marzano Taxonomy

**Purpose:** Create complete lesson plan with activities mapped to Marzano levels, ensuring cognitive rigor across the lesson.

**Inputs:**
- Competency breakdown from Stage 2 (`02_competency_breakdown.json`)
- [MARZANO.md](./MARZANO.md) framework reference

**Process:**

#### Step 1: Load Competency Breakdown

Read the skills and knowledge from `02_competency_breakdown.json` saved in Stage 2.

#### Step 2: Determine Lesson Type

Based on teacher input and context, identify which lesson type applies:

| Lesson Type | When to Use | Cognitive Focus |
|-------------|-------------|-----------------|
| **Introducing new knowledge/skills** | First lesson on a topic | More retrieval + comprehension |
| **Practicing skills** | Reinforcing introduced content | Balance of all levels |
| **Applying knowledge** | Using knowledge in structured problems | Heavy analysis + application |
| **Synthesizing** | Combining multiple concepts | Analysis + knowledge utilization |
| **Novel application** | Applying to new/unfamiliar contexts | Mostly knowledge utilization |

**Confirmation prompt:** "Based on what you've told me, this seems like an [introducing/practicing/etc.] lesson. Is that right?"

#### Step 3: Design Activities Following Marzano Progression

See [MARZANO.md](./MARZANO.md) for detailed guidance on each cognitive level.

**For "Introducing new knowledge" lessons:**
- Opening retrieval (5-10 min): Connect to prior knowledge
- Comprehension (15-20 min): Direct instruction with checks for understanding
- Analysis (10-15 min): Students examine/compare/contrast new content
- Application (10-15 min): Initial practice with scaffolding
- Assessment (5 min): Exit ticket or embedded check

**For "Practicing skills" lessons:**
- Retrieval (5 min): Quick review of key concepts/procedures
- Comprehension (10 min): Explain steps and reasoning
- Analysis (15-20 min): Error analysis and pattern recognition
- Knowledge utilization (10-15 min): Apply to varied contexts
- Assessment (5 min): Demonstration or exit ticket

**For "Applying knowledge" lessons:**
- Retrieval (5 min): Quick review of key concepts
- Comprehension check (5 min): Verify readiness
- Analysis (15-20 min): Structured problem-solving
- Knowledge utilization (20-25 min): Open-ended application
- Assessment (5 min): Reflection or exit ticket

**For "Synthesizing" lessons:**
- Retrieval (5 min): Activate prior knowledge from multiple topics
- Comprehension (10 min): Connect ideas across concepts
- Analysis (15-20 min): Examine relationships across concepts
- Knowledge utilization (15-20 min): Create something integrating multiple concepts
- Assessment (5 min): Synthesis demonstration

**For "Novel application" lessons:**
- Retrieval (5 min): Minimal fact recall
- Comprehension (5-10 min): Understand problem context
- Analysis (15-20 min): Break down complex/unfamiliar problem
- Knowledge utilization (25-30 min): Innovative problem solving
- Assessment (5 min): Process reflection

#### Step 4: Specify Each Activity

For each activity in the lesson, include:

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Action-oriented activity name | Yes |
| `duration` | Time in minutes | Yes |
| `marzano_level` | One of: `retrieval`, `comprehension`, `analysis`, `knowledge_utilization` | Yes |
| `instructions` | Numbered steps for students | Yes |
| `materials` | List of required materials/resources | Yes |
| `student_output` | What students produce (tangible work product) | Yes |
| `assessment_method` | How teacher knows it worked | Yes |
| `differentiation` | Support/extension options | Recommended |

#### Step 5: Include Hidden First Slide Content

Design content for the teacher-only hidden first slide:

- **Objective:** Single clear statement of what students will be able to do
- **Agenda:** Activity list with timing
- **Anticipated misconceptions:** 2-3 common student errors to watch for
- **Delivery tips:** 2-3 instructional suggestions

#### Step 6: Save Lesson Design

Save to `.lesson-designer/sessions/{session_id}/03_lesson_design_v1.json`:

```json
{
  "title": "string",
  "grade_level": "string",
  "duration": "integer (minutes)",
  "lesson_type": "introducing|practicing|applying|synthesizing|novel_application",
  "objective": "string (single clear statement)",
  "activities": [
    {
      "name": "string",
      "duration": "integer",
      "marzano_level": "retrieval|comprehension|analysis|knowledge_utilization",
      "instructions": ["string"],
      "materials": ["string"],
      "student_output": "string",
      "assessment_method": "string",
      "differentiation": {
        "support": ["string"],
        "extension": ["string"]
      }
    }
  ],
  "hidden_slide_content": {
    "objective": "string",
    "agenda": [{"activity": "string", "duration": "integer"}],
    "misconceptions": ["string"],
    "delivery_tips": ["string"]
  },
  "vocabulary": [{"word": "string", "definition": "string"}],
  "assessment": {
    "type": "exit_ticket|embedded|performance",
    "description": "string",
    "questions": ["string"]
  }
}
```

**Outputs:** `03_lesson_design_v1.json` with complete lesson structure

**Requirements Covered:**
- MARZ-01: Lessons structured according to Marzano taxonomy (retrieval through knowledge utilization)
- MARZ-02: Tasks aligned to lesson type (introducing, practicing, applying, synthesizing, novel application)

**Next:** Stage 3b (Validate cognitive rigor)

---

### Stage 3b: Validate Cognitive Rigor

**Purpose:** Ensure lesson meets minimum higher-order thinking thresholds before proceeding.

**Inputs:** `03_lesson_design_v1.json` from Stage 3

**Process:**

#### Step 1: Run Validation Script

After saving lesson design, IMMEDIATELY run validation:

```bash
python .claude/skills/lesson-designer/scripts/validate_marzano.py .lesson-designer/sessions/{session_id}/03_lesson_design_v1.json
```

#### Step 2: Interpret Results

**Exit code 0 (PASSED):**
- Proceed to Stage 4
- Save final validated design as `04_lesson_final.json`

**Exit code 1 (PASSED WITH WARNINGS):**
- Review warnings and consider addressing them
- Can proceed if warnings are acceptable
- Inform teacher of any warnings

**Exit code 2 (FAILED - BLOCKS PROGRESSION):**
- Review the error messages
- The most common issue is insufficient higher-order thinking

#### Step 3: Address Validation Failures

If validation fails, return to Stage 3 and:

1. **Convert retrieval activities to comprehension:**
   - Change "List the steps" to "Explain why each step is needed"
   - Change "Define vocabulary" to "Create analogies for concepts"

2. **Convert comprehension activities to analysis:**
   - Change "Summarize the content" to "Compare and contrast with..."
   - Change "Explain the process" to "Analyze what would happen if..."

3. **Add knowledge utilization activities:**
   - Design challenges: "Create a solution for..."
   - Investigation tasks: "Investigate and propose..."
   - Real-world application: "Apply this concept to solve..."

4. **Regenerate lesson design** as `03_lesson_design_v2.json`

5. **Re-run validation**

#### Step 4: Maximum Attempts

**Maximum 3 validation attempts.** If still failing after 3 tries:
- Present the issues to the teacher for guidance
- Ask which cognitive trade-offs are acceptable
- Proceed with teacher's explicit approval

#### Example Validation Workflow

```
[Claude runs validation]

VALIDATION REPORT
=================

Cognitive Distribution:
  Retrieval: 20.0%
  Comprehension: 25.0%
  Analysis: 30.0%
  Knowledge Utilization: 25.0%

Higher-Order Thinking: 55.0% (minimum 40%) - PASS

Errors:
  (none)

Warnings:
  - Activity 4 drops 2 cognitive levels from Activity 3

RESULT: PASSED WITH WARNINGS

[Claude proceeds to Stage 4, noting warning for teacher]
```

**Outputs:** Validation report and final lesson design (`04_lesson_final.json`)

**Requirements Covered:**
- MARZ-03: Cognitive rigor enforced with minimum 40% higher-order thinking

**Next:** Stage 4 (if passed) or Stage 3 (if failed, up to 3 attempts)

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
