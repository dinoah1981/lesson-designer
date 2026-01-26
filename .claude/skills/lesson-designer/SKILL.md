---
name: lesson-designer
description: Design complete, classroom-ready lessons and multi-lesson sequences using Robert Marzano's New Taxonomy framework
version: 3.0.0
author: Claude
---

# Lesson Designer Skill

Design complete, classroom-ready lessons and multi-lesson sequences using Robert Marzano's New Taxonomy framework. This skill produces slide decks, student worksheets, and differentiated materials with cognitive rigor validation.

## Workflow Overview

Execute these stages sequentially:

- [ ] **Stage 0.5: Sequence Planning** (optional - for multi-lesson units)
- [ ] **Stage 1: Gather competency requirements**
- [ ] **Stage 2: Decompose into skills and knowledge**
- [ ] **Stage 2b: Teacher classification and proficiency targets**
- [ ] **Stage 3: Design lesson with Marzano taxonomy**
- [ ] **Stage 3b: Validate cognitive rigor**
- [ ] **Stage 3.5: Persona feedback & revision**
- [ ] **Stage 5: Generate materials (.pptx + .docx)**
- [ ] **Stage 5b: Generate simulation (optional)**
- [ ] **Stage 5c: Generate assessment (optional)**
- [ ] **Stage 6: Validate outputs**
- [ ] **Stage 7: Present to teacher**
- [ ] **Stage 8: Generate Sequence Assessment** (sequences only)

## State Directory Structure

Each lesson session maintains state in `.lesson-designer/sessions/{session_id}/`:

**Single Lesson Structure:**
```
.lesson-designer/sessions/{session_id}/
├── state.json                            # Current workflow stage and lesson data
├── lesson.json                           # Complete lesson plan with activities
├── 03_feedback_struggling_learner.json   # Persona feedback (Stage 3.5)
├── 03_revision_plan.json                 # Revision plan with teacher decisions (Stage 3.5)
├── 03_revision_plan.md                   # Teacher-readable revision plan (Stage 3.5)
├── slide_deck.pptx                       # Generated PowerPoint presentation
└── student_worksheet.docx                # Generated Word worksheet
```

**Multi-Lesson Sequence Structure:**
```
.lesson-designer/sessions/{sequence_id}/
├── sequence_metadata.json              # Sequence-level planning
├── lesson_01/
│   ├── 01_input.json                   # Existing lesson files
│   ├── 04_lesson_final.json
│   ├── lesson_summary.json             # Compressed summary for context
│   └── materials/
├── lesson_02/
│   └── ...
└── sequence_assessment.docx            # Summative assessment
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

### Stage 0.5: Sequence Planning (Optional)

**Purpose:** Plan coherent multi-lesson units (2-4 weeks) before generating individual lessons.

**When to use:** When teacher wants multiple lessons that build on each other. Skip for single standalone lessons.

**Process:**

1. **Gather sequence information:**
   - What competencies should students master by the end?
   - How many total lessons in the sequence?
   - What grade level and lesson duration?

2. **Create sequence session:**
   ```python
   from sequence_manager import create_sequence_session

   sequence_id = create_sequence_session(
       competencies=["Analyze primary sources", "Construct evidence-based arguments"],
       grade_level="8th grade",
       total_lessons=6,
       lesson_duration=55
   )
   ```

3. **Assign competencies to lesson ranges:**
   ```python
   from sequence_manager import assign_competency_to_lessons

   assign_competency_to_lessons(sequence_id, "comp-01", start_lesson=1, end_lesson=3)
   assign_competency_to_lessons(sequence_id, "comp-02", start_lesson=4, end_lesson=6)
   ```

4. **Plan vocabulary progression:**
   - Identify key terms for each lesson
   - Terms accumulate - lesson 3 assumes students know lesson 1-2 terms

**Output:**
- `sequence_metadata.json` with competencies, lesson ranges, vocabulary plan
- Lesson subdirectories ready for individual lesson generation

**Next:** Execute Stages 1-7 for each lesson in sequence, using context from prior lessons.

---

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

### Stage 2b: Teacher Classification and Proficiency Targets

**Purpose:** Have the teacher classify each knowledge item (needs teaching vs. already assumed) and set the target proficiency level for the skill.

**Inputs:** Competency breakdown from Stage 2 (`02_competency_breakdown.json`)

**Process:**

1. **Load the competency breakdown:**

   ```python
   import sys
   sys.path.insert(0, '.claude/skills/lesson-designer/scripts')
   from parse_competency import load_breakdown, update_breakdown_with_classifications

   breakdown = load_breakdown(session_id)
   ```

2. **Present each knowledge item and ask teacher to classify:**

   ```
   For each knowledge item, I need to know if students already know this
   or if it needs to be taught in this lesson.

   **K1: What primary sources are (definition, types)**
   Classification? [needs teaching / already assumed]

   **K2: How to identify bias in sources**
   Classification? [needs teaching / already assumed]

   **K3: What constitutes evidence vs. opinion**
   Classification? [needs teaching / already assumed]

   **K4: Historical context of the period being studied**
   Classification? [needs teaching / already assumed]

   **K5: How to cite sources properly**
   Classification? [needs teaching / already assumed]
   ```

   **Classification meanings:**
   - **needs_teaching** - Students don't know this yet; lesson will include direct instruction
   - **already_assumed** - Students should already know this; lesson will include brief retrieval practice but not direct instruction

3. **Explain the impact of classification:**

   ```
   For items marked "already assumed":
   - I'll include a brief retrieval activity to activate prior knowledge
   - But we won't spend time on direct instruction

   For items marked "needs teaching":
   - The lesson will include explicit instruction on this knowledge
   - Students will get practice and feedback
   ```

4. **Ask about target proficiency level:**

   ```
   After this lesson/sequence, what proficiency level should students reach
   with the skill "[skill statement]"?

   - **Novice:** Can perform skill with significant support/scaffolding
   - **Developing:** Can perform skill with some support
   - **Proficient:** Can perform skill independently
   - **Advanced:** Can perform skill and teach/extend it to new contexts

   Note: For a single lesson on new content, "Developing" is often realistic.
   For multi-lesson sequences or practice-focused lessons, "Proficient" may
   be achievable.
   ```

5. **Update the competency breakdown with classifications:**

   ```python
   classifications = {
       "K1": "needs_teaching",
       "K2": "needs_teaching",
       "K3": "already_assumed",
       "K4": "needs_teaching",
       "K5": "already_assumed"
   }
   target_proficiency = "developing"

   update_breakdown_with_classifications(session_id, classifications, target_proficiency)
   ```

**Updated Breakdown JSON Schema (`02_competency_breakdown.json`):**

After Stage 2b, the JSON includes classifications and proficiency target:

```json
{
  "skill": {
    "verb": "evaluate",
    "object": "historical claims",
    "full_statement": "Evaluate historical claims using primary source evidence"
  },
  "required_knowledge": [
    {
      "id": "K1",
      "item": "What primary sources are (definition, types)",
      "classification": "needs_teaching"
    },
    {
      "id": "K2",
      "item": "How to identify bias in sources",
      "classification": "needs_teaching"
    },
    {
      "id": "K3",
      "item": "What constitutes evidence vs. opinion",
      "classification": "already_assumed"
    },
    {
      "id": "K4",
      "item": "Historical context of the period being studied",
      "classification": "needs_teaching"
    },
    {
      "id": "K5",
      "item": "How to cite sources properly",
      "classification": "already_assumed"
    }
  ],
  "target_proficiency": "developing"
}
```

**Classification values:**
- `"needs_teaching"` - Requires direct instruction in this lesson
- `"already_assumed"` - Prior knowledge; retrieval practice only

**Proficiency levels:**
- `"novice"` - Performs with significant support
- `"developing"` - Performs with some support
- `"proficient"` - Performs independently
- `"advanced"` - Performs and can extend/teach

**Outputs:**
- Updated `02_competency_breakdown.json` with classifications and target proficiency
- Clear understanding of what needs instruction vs. activation

**Requirements Covered:**
- COMP-04: Classify knowledge items (needs teaching vs. already assumed)
- COMP-05: Target proficiency level captured

**Next:** Stage 3

---

### Stage 3: Design Lesson with Marzano Taxonomy

**Purpose:** Create complete lesson plan with activities mapped to Marzano levels, ensuring cognitive rigor across the lesson.

> **Sequence Mode:** If designing lesson N in a sequence, first build context:
> ```python
> from sequence_context import build_context_for_lesson
> context = build_context_for_lesson(sequence_id, lesson_num)
> # context includes prior_lessons, vocabulary_already_taught
> ```
> Use this context when designing the lesson to maintain progression coherence.

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

**Next:** Stage 3.5 (Persona Feedback & Revision) or Stage 3 (if failed, up to 3 attempts)

---

### Stage 3.5: Multi-Persona Feedback (Optional)

Run the lesson design through 4 diverse student personas to identify accessibility barriers, engagement issues, and ceiling limitations.

**Personas:**
1. **Alex (Struggling/ELL)** - Reading 2-3 years below grade level, vocabulary gaps
2. **Jordan (Unmotivated Capable)** - High ability, low engagement, needs relevance
3. **Maya (Interested Capable)** - High ability, high engagement, wants depth
4. **Marcus (High Achieving)** - Gifted learner, rapid mastery, needs challenge

**Step 1: Run Multi-Persona Evaluation**

```bash
python .claude/skills/lesson-designer/scripts/run_multi_persona.py \
    .lesson-designer/sessions/{session_id}/04_lesson_final.json \
    .lesson-designer/sessions/{session_id}/
```

Output: 4 feedback files
- `03_feedback_struggling_learner_ell.json`
- `03_feedback_unmotivated_capable.json`
- `03_feedback_interested_capable.json`
- `03_feedback_high_achieving.json`

**Step 2: Generate Synthesized Revision Plan**

```bash
python .claude/skills/lesson-designer/scripts/generate_revision_plan.py \
    "03_feedback_struggling_learner_ell.json,03_feedback_unmotivated_capable.json,03_feedback_interested_capable.json,03_feedback_high_achieving.json" \
    03_revision_plan.json \
    --lesson 04_lesson_final.json \
    --markdown 03_revision_plan.md
```

Output: Revision plan with synthesis categories:
- **Universal Improvements** - 3+ personas agree (highest priority)
- **Accessibility Critical** - Struggling learner barriers
- **Engagement Enhancements** - Motivation/interest suggestions
- **Challenge Extensions** - High-achieving needs
- **Conflicting Recommendations** - Require teacher decision

**Step 3: Teacher Review**

Present `03_revision_plan.md` to teacher for approval.

Conflict resolution strategies:
- **Tiered Support**: Scaffolded version for struggling + challenge version for advanced
- **Core + Extension**: All students do core, capable students extend
- **Optionality**: Multiple paths to same learning goal

**Step 4: Apply Revisions**

```bash
python .claude/skills/lesson-designer/scripts/generate_revision_plan.py \
    --apply \
    --lesson 04_lesson_final.json \
    --revision-plan 03_revision_plan.json \
    --output 04_lesson_revised.json
```

**Differentiation Principle:** Add, don't subtract. Never remove scaffolding to add challenge or simplify to add accessibility. Use tiering and optionality instead.

**When to Skip Stage 3.5:**

Stage 3.5 can be skipped if:
- Teacher explicitly opts out (`"skip_persona_feedback": true` in 01_input.json)
- Lesson is specifically designed for a narrow audience only

Default: Always run Stage 3.5 for inclusive lesson design.

**Requirements Covered:**
- PERS-01 (partial): Tool runs lesson through struggling learner persona
- PERS-02: Persona provides reaction describing likely response
- PERS-03: Persona provides specific pedagogical recommendations
- PERS-04: Tool proposes revisions; teacher confirms before finalizing

**Next:** Stage 5 (Generate Materials)

---

### Stage 5: Generate Materials (.pptx + .docx)

**Purpose:** Create classroom-ready files from validated lesson plan.

**Inputs:** `04_lesson_final.json` from Stage 3b

**Process:**

#### Part 1: Generate PowerPoint Slide Deck

Claude generates professional slide decks directly using python-pptx, applying design principles that create visually engaging, teacher-ready presentations.

**1. Load the validated lesson design:**

```python
import json
session_path = f".lesson-designer/sessions/{session_id}"
with open(f"{session_path}/04_lesson_final.json", 'r') as f:
    lesson = json.load(f)
```

**2. Create the presentation using python-pptx:**

Write and execute python-pptx code to create the slide deck. Apply these design principles:

**Design System (Professional Teacher-Ready Style):**

```
COLOR PALETTE:
- Header background: #2D5A87 (professional blue)
- Body text: #2C3E50 (dark charcoal)
- Accent/timer: #F4D03F (gold yellow)
- Content boxes: #FFFFFF (white) with subtle shadow
- Activity icons: Use emoji for visual interest (📚 🎯 💭 ✍️ 🔍)

LAYOUT PRINCIPLES:
- White content rectangles on colored backgrounds for readability
- Timer display in corner showing duration (e.g., "⏱️ 5 min")
- Activity type icons next to headers
- Vocabulary terms in colored boxes with definitions
- Agenda slide with checkboxes (☐) for each activity

TYPOGRAPHY:
- Titles: 40pt bold, can use italic for emphasis
- Body: 20-24pt
- Minimum 16pt for any visible text
- Use consistent font (Calibri or Arial)

SLIDE STRUCTURE:
- Slide 1: HIDDEN - Teacher lesson plan (objective, agenda, misconceptions, tips)
- Slide 2: Title slide with lesson name, grade, duration, objective
- Slide 3: Agenda with activity list and timing
- Slides 4+: One slide per activity with sparse talking points
- Final slide: Exit ticket / assessment
```

**3. Required slide structure:**

| Slide | Content | Design Notes |
|-------|---------|--------------|
| **Slide 1** | Lesson plan for teacher | **HIDDEN** - Set `slide._element.set('show', '0')` |
| **Slide 2** | Title, grade, duration | Large title, accent color bar |
| **Slide 3** | Agenda with timing | Checkbox list (☐) with durations |
| **Slides 4+** | Activity content | Icon + timer + 3-5 bullet points |
| **Final** | Assessment/exit ticket | Numbered questions |

**4. Sparse Format Philosophy:**

```
IMPORTANT: Slides are designed for teacher-led instruction, not self-study.

Each slide contains:
- 3-5 talking points (not full paragraphs)
- Maximum 15 words per point
- Activity icon and timer in header area

The full content is in presenter notes, which include:
- SAY: What to tell students
- ASK: Questions to check understanding
- DEMO: What to show or model
- WATCH FOR: Common mistakes to address

Teachers should never read slides to students. Slides are conversation scaffolding.
```

**5. Example code structure:**

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Colors
HEADER_BLUE = RgbColor(0x2D, 0x5A, 0x87)
BODY_CHARCOAL = RgbColor(0x2C, 0x3E, 0x50)
ACCENT_GOLD = RgbColor(0xF4, 0xD0, 0x3F)

# Slide 1: Hidden lesson plan
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
slide1._element.set('show', '0')  # Hide this slide
# Add lesson plan content...

# Slide 2: Title slide with design elements
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
# Add colored header shape, white content area, title text...

# Continue for each activity...

prs.save(f"{session_path}/05_slides.pptx")
```

**6. Save to session directory:**

Output: `.lesson-designer/sessions/{session_id}/05_slides.pptx`

**Requirements Covered (Part 1):**
- SLID-01: Tool generates actual .pptx files
- SLID-02: Hidden first slide with lesson plan
- SLID-03: Sparse, teacher-led format (talking points, not paragraphs)
- SLID-04: 16pt font minimum (uses 20pt+ for body, 40pt for titles)

#### Part 2: Generate Student Materials (Word Document)

Generate student worksheet/materials based on lesson type:

```bash
python .claude/skills/lesson-designer/scripts/generate_worksheet.py \
  .lesson-designer/sessions/{session_id}/04_lesson_final.json \
  .claude/skills/lesson-designer/templates/student_worksheet.docx \
  .lesson-designer/sessions/{session_id}/06_worksheet.docx
```

**Material Type Selection:**

The tool automatically selects the appropriate material format based on lesson type:

| Lesson Type        | Material Format  | Purpose                    |
|--------------------|------------------|----------------------------|
| Introducing        | Worksheet        | Reading + comprehension    |
| Practicing         | Problem Set      | Practice exercises         |
| Applying           | Worksheet        | Structured application     |
| Synthesizing       | Activity Guide   | Project instructions       |
| Novel Application  | Problem Set      | Challenge problems         |

This ensures students get materials that match the lesson's purpose.

**Assessment Integration (Requirement ASMT-01):**

EVERY lesson includes assessment of its objective. Assessment appears as one of:

- **Exit Ticket:** 2-3 questions at the end of the worksheet
- **Embedded Questions:** Assessment integrated throughout activities
- **Performance Task:** Clear success criteria for demonstration

The assessment tells teachers whether students achieved the learning objective.

**Template System:**

Student materials use Jinja2 templating via docxtpl:

```
{{ title }}              -> Lesson title
{{ grade_level }}        -> Grade level
{% for activity in activities %}
  {{ activity.name }}    -> Activity name
  {{ activity.duration }} -> Duration in minutes
{% endfor %}
{{ exit_ticket.questions }} -> Assessment questions
```

This allows teachers to customize the template (fonts, branding, layout) without touching the generation code.

**Error Handling:**

If document generation fails:
1. Check that lesson design JSON is valid (`04_lesson_final.json` exists)
2. Check that template file exists at expected path
3. Check for unrendered Jinja2 tags (indicates template syntax error)
4. Review error message for specific issue

**Phase 2 Formatting Features:**

Worksheets now include:
- **Double-spaced answer lines:** Answer lines with underscores use 2.0 line spacing multiplier for adequate writing room
- **Cognitive complexity-based spacing:** Answer space scales with Marzano level (2-6 lines based on thinking demands)
- **Discussion facilitation notes:** Discussion slides include TIME ALLOCATION, WATCH FOR, and PROMPTS TO USE sections

**Outputs:**
- `05_slides.pptx` - PowerPoint presentation for teacher
- `06_worksheet.docx` - Student materials matching lesson type

**Requirements Covered:**
- MATL-01: Generate actual .docx Word documents
- MATL-03: Material type matches lesson type
- ASMT-01: Each lesson includes assessment of its objective

**Next:** Stage 5b (optional simulation) or Stage 5c (optional assessment) or Stage 6

---

### Stage 5b: Generate Simulation (Optional)

**Purpose:** Create interactive HTML/JavaScript simulations for experiential learning activities.

**When to use:** When lesson includes activities requiring visualization, interaction, or experimentation (e.g., physics simulations, data visualizations, interactive models).

**Process:**

Generate simulation using the generate_simulation.py script:

```bash
python .claude/skills/lesson-designer/scripts/generate_simulation.py \
  --competency "Students will analyze projectile motion" \
  --simulation-type "physics" \
  --output "projectile_simulation.html"
```

**Simulation Types:**

| Type | Best For | Example |
|------|----------|---------|
| `physics` | Forces, motion, waves | Projectile motion, pendulum |
| `data` | Charts, graphs, statistics | Interactive scatter plots |
| `geometry` | Shapes, transformations | Angle exploration |
| `ecosystem` | Biology, populations | Predator-prey dynamics |
| `chemistry` | Molecules, reactions | pH simulation |

**Simulation type selection:** Keyword-based detection from competency:
- "force", "motion", "velocity" → physics
- "data", "graph", "chart" → data
- "shape", "angle", "triangle" → geometry
- "population", "species", "ecosystem" → ecosystem
- "molecule", "reaction", "pH" → chemistry

**Output format:** Self-contained HTML file with p5.js loaded from CDN (zero-install deployment for students).

**Features:**
- Interactive controls (sliders, buttons)
- Real-time visualization
- Reset functionality
- Educational annotations

**Next:** Stage 5c (optional assessment) or Stage 6

---

### Stage 5c: Generate Assessment (Optional)

**Purpose:** Create dedicated assessment materials beyond embedded exit tickets.

**When to use:** When you need formal quizzes, tests, performance tasks, or Socratic discussion guides.

**Process:**

Generate assessment using the generate_assessment.py script:

```bash
python .claude/skills/lesson-designer/scripts/generate_assessment.py \
  --lesson-file ".lesson-designer/sessions/{session_id}/04_lesson_final.json" \
  --assessment-type "quiz" \
  --output ".lesson-designer/sessions/{session_id}/quiz.docx"
```

**Assessment Types:**

| Type | Purpose | Output Files | Features |
|------|---------|--------------|----------|
| `quiz` | Quick formative check (5-10 min) | Student version + Answer key | Multiple choice, short answer, auto-generated keys |
| `test` | Comprehensive summative (30-45 min) | Student version + Answer key | Mix of question types, detailed rubric |
| `performance` | Skill demonstration | Task description + Rubric | 4-level rubric (Advanced/Proficient/Developing/Beginning) |
| `socratic` | Discussion-based assessment | Discussion guide + Participation rubric | Questions, prompts, discussion protocol, default criteria |

**Quiz/Test Features:**
- Mix of retrieval, comprehension, analysis questions
- Answer keys auto-generated alongside student version
- Clear point values
- Space for student responses

**Performance Task Features:**
- Scenario or problem statement
- Clear success criteria
- 4-level rubric (4/3/2/1 points per criterion)
- Materials list

**Socratic Discussion Features:**
- Central question(s) aligned to objective
- Follow-up prompts
- Discussion protocol (timing, roles)
- Participation rubric with default criteria:
  - Participation (contribution frequency/quality)
  - Evidence Use (supports claims with evidence)
  - Engagement with Others (builds on peer ideas)

**Default rubric structure:** Advanced (4 pts) / Proficient (3 pts) / Developing (2 pts) / Beginning (1 pt)

**Next:** Stage 6

---

### Stage 6: Validate Outputs

**Purpose:** Verify generated files meet quality requirements before presenting to teacher.

**Inputs:** Generated files from Stage 5

**Process:**

#### Step 1: Run Output Validation

Execute the validation script on the session directory:

```bash
python .claude/skills/lesson-designer/scripts/validate_outputs.py \
  .lesson-designer/sessions/{session_id}/
```

#### Step 2: Review Validation Report

The script generates `07_validation_report.txt` in the session directory. Check the report for:

**Exit Codes:**
```
Exit code 0: PASSED - All files valid, proceed to Stage 7
Exit code 1: PASSED WITH WARNINGS - Files valid but have minor issues, can proceed
Exit code 2: FAILED - Critical errors found, must fix before presenting
```

**Validation Checks Performed:**

**PowerPoint (.pptx):**
- File exists and can be opened
- Has minimum number of slides (at least 4: lesson plan + title + objectives + 1 activity)
- First slide is hidden (lesson plan for teacher) - SLID-02
- Hidden slide contains required sections (objective, agenda, misconceptions, tips)
- Font sizes meet 16pt minimum for visible text - SLID-04
- Title slide has content

**Word Document (.docx):**
- File exists and can be opened
- No unrendered Jinja2 template tags ({{ or {%})
- Has required sections (objectives, activities)
- Has assessment section - ASMT-01
- Has minimum paragraph count

#### Step 3: Handle Validation Results

**If PASSED (exit code 0):**
- Proceed directly to Stage 7

**If PASSED WITH WARNINGS (exit code 1):**
- Review warnings in the report
- Decide if warnings are acceptable
- If acceptable, proceed to Stage 7
- If not, address issues and re-validate

**If FAILED (exit code 2):**
- Review error messages in the report
- Address each error before presenting to teacher

#### Common Issues and Fixes

```
ISSUE: "First slide is not hidden"
FIX: Check generate_slides.py is using slide._element.set('show', '0')
     Re-run slide generation if needed

ISSUE: "Font size below 16pt minimum"
FIX: Template may have small fonts - update template or regenerate

ISSUE: "Unrendered Jinja2 template tags"
FIX: Check lesson design JSON has all required fields
     Ensure 04_lesson_final.json is complete and valid

ISSUE: "Missing assessment section"
FIX: Ensure lesson design includes assessment with type and questions
     Return to Stage 3 if assessment is missing from design
```

#### Error Recovery Workflow

1. **If slides validation failed:**
   - Check `04_lesson_final.json` is valid: `python -c "import json; json.load(open('.lesson-designer/sessions/{session_id}/04_lesson_final.json'))"`
   - Re-run: `python .claude/skills/lesson-designer/scripts/generate_slides.py .lesson-designer/sessions/{session_id}/04_lesson_final.json`

2. **If document validation failed:**
   - Check template exists: `ls .claude/skills/lesson-designer/templates/student_worksheet.docx`
   - Re-run: `python .claude/skills/lesson-designer/scripts/generate_worksheet.py .lesson-designer/sessions/{session_id}/04_lesson_final.json`

3. **If assessment missing:**
   - Return to Stage 3 to add assessment section to lesson design
   - Re-validate with Marzano script
   - Re-generate materials

**Outputs:**
- `07_validation_report.txt` - Detailed validation results with requirement checklist
- Validation pass/fail status determining workflow progression

**Requirements Covered:**
- SLID-02: Hidden first slide with lesson plan (verified)
- SLID-04: 16pt font minimum (verified)
- MATL-01: Generated .docx file (verified)
- ASMT-01: Formative assessment included (verified)

**Next:** Stage 7 (if passed) or Stage 5 (if failed, after fixing issues)

---

### Stage 7: Present to Teacher

**Purpose:** Deliver completed materials and summarize the lesson for teacher review.

**Inputs:** Validated files from Stage 6 (05_slides.pptx, 06_worksheet.docx)

**Process:**

#### Step 1: Summarize What Was Created

Present a clear summary of the generated materials:

```
Your lesson materials are ready!

Created for: {competency}
Grade Level: {grade_level}
Duration: {duration} minutes
Lesson Type: {lesson_type}

Files generated:
- 05_slides.pptx - Slide deck with hidden lesson plan
- 06_worksheet.docx - Student materials

Cognitive rigor: {percentage}% higher-order thinking
Assessment: {assessment_type}
```

**Example:**
```
Your lesson materials are ready!

Created for: Students will analyze primary sources to evaluate historical claims
Grade Level: 8th grade
Duration: 50 minutes
Lesson Type: Introducing

Files generated:
- 05_slides.pptx - Slide deck with hidden lesson plan (12 slides)
- 06_worksheet.docx - Student worksheet with exit ticket

Cognitive rigor: 55% higher-order thinking (analysis + knowledge utilization)
Assessment: Exit ticket (2 questions)
```

#### Step 2: Provide File Locations

Tell the teacher exactly where to find their files:

```
Files are saved in:
.lesson-designer/sessions/{session_id}/

Full paths:
- Slides: .lesson-designer/sessions/{session_id}/05_slides.pptx
- Worksheet: .lesson-designer/sessions/{session_id}/06_worksheet.docx

You can open them directly or I can help you review any section.
```

#### Step 3: Highlight Key Features

Explain the instructional design choices:

```
About your materials:

SLIDE DECK:
- First slide is HIDDEN - contains your lesson plan, objective, agenda, and tips
- Slides are sparse (talking points only) - designed for teacher-led instruction
- Full instructions are in presenter notes (click Notes pane to view)
- Presenter notes include SAY/ASK/DEMO/WATCH FOR guidance

STUDENT WORKSHEET:
- Matches your lesson type ({material_type})
- Includes {assessment_type} for formative assessment
- Activities are formatted with space for student responses
```

#### Step 4: Offer Next Steps

```
What would you like to do next?

- Review the slides (I'll show you the content)
- Review the student materials (I'll show you the content)
- Make adjustments (regenerate with changes)
- Design another lesson (start fresh)
- Refine this lesson (Phase 2 adds persona feedback)
```

#### Step 5: Handle Teacher Requests

**If teacher wants to review slides:**
- Read and display the slide content from the JSON
- Highlight the hidden lesson plan content
- Show presenter notes for key activities

**If teacher wants to review worksheet:**
- Read and display the document structure
- Show activity flow and assessment questions

**If teacher requests changes:**

For **minor changes** (typos, wording, adding a question):
1. Edit the lesson design JSON (`04_lesson_final.json`)
2. Regenerate materials (re-run Stage 5)
3. Re-validate (Stage 6)
4. Present updated materials

For **major changes** (different activities, new objectives, restructuring):
1. Return to appropriate stage:
   - Stage 1: Change competency or grade level
   - Stage 2/2b: Change skills/knowledge breakdown
   - Stage 3: Change activities or lesson type
2. Progress through subsequent stages again

**If teacher approves materials:**
```
Great! Your lesson is ready to teach.

Session ID: {session_id}
Files location: .lesson-designer/sessions/{session_id}/

TIP: The hidden first slide in your PowerPoint has your complete lesson plan.
Open the presentation in Normal view and check the first slide for:
- Objective
- Agenda with timing
- Anticipated misconceptions
- Delivery tips

Good luck with your lesson!
```

> **Sequence Mode:** After lesson approval, create summary for future context:
> ```python
> from sequence_context import create_lesson_summary, update_vocabulary_progression
> summary = create_lesson_summary(sequence_id, lesson_num, lesson_json, persona_feedback)
> update_vocabulary_progression(sequence_id, lesson_num, introduced_terms)
> ```

**Outputs:**
- Teacher-facing summary of completed materials
- Clear file locations
- Options for next steps

**Next:** Session complete (or return to earlier stage if changes requested)

---

### Stage 8: Generate Sequence Assessment (Sequences Only)

**Purpose:** Create summative assessment covering the entire lesson sequence.

**When to run:** After all lessons in sequence are complete.

**Process:**

1. **Choose assessment type:**
   - `cumulative_test` - Multi-section test with questions from all lessons
   - `performance_task` - Complex task requiring integration of all competencies
   - `portfolio_review` - Reflection and self-assessment guide

2. **Generate assessment:**
   ```python
   from generate_sequence_assessment import generate_sequence_assessment, SequenceAssessmentConfig

   config = SequenceAssessmentConfig(
       assessment_type="cumulative_test",
       title="Unit 3 Assessment: Primary Source Analysis",
       time_limit=60
   )

   assessment = generate_sequence_assessment(sequence_id, config)
   ```

3. **Review and approve:**
   - Assessment covers vocabulary from all lessons
   - Questions span Marzano levels (retrieval through knowledge utilization)
   - Performance tasks integrate multiple competencies

**Output:**
- `sequence_assessment.json` - Assessment structure
- `sequence_assessment.docx` - Printable assessment document
- `sequence_assessment_key.docx` - Answer key (for cumulative_test)

**Next:** Sequence complete

---

## Complete Workflow Checklist

Use this checklist to track progress through a lesson design session:

```
COMPLETE LESSON DESIGN WORKFLOW
================================

Session ID: ________________

STAGE 1: Gather competency requirements
  [ ] Asked 5 input questions (competency, grade, lesson count, duration, constraints)
  [ ] Validated competency is skill-focused (not topic-focused)
  [ ] Created session directory
      Output: 01_input.json

STAGE 2: Decompose into skills and knowledge
  [ ] Identified skill verb and object
  [ ] Listed required knowledge items
  [ ] Teacher reviewed and approved decomposition
      Output: 02_competency_breakdown.json (partial)

STAGE 2b: Teacher classification and proficiency targets
  [ ] Teacher classified each knowledge item (needs_teaching / already_assumed)
  [ ] Teacher selected target proficiency level
      Output: Updated 02_competency_breakdown.json

STAGE 3: Design lesson with Marzano taxonomy
  [ ] Determined lesson type
  [ ] Designed activities with Marzano levels
  [ ] Included hidden slide content
  [ ] Added vocabulary and assessment
      Output: 03_lesson_design_v1.json

STAGE 3b: Validate cognitive rigor
  [ ] Ran validate_marzano.py script
  [ ] Verified 40%+ higher-order thinking
  [ ] Addressed any errors (max 3 attempts)
  [ ] Saved final validated design
      Output: Validation passed -> 04_lesson_final.json

STAGE 3.5: Persona feedback & revision
  [ ] Ran persona_evaluator.py script
  [ ] Generated revision plan (JSON + Markdown)
  [ ] Presented revision plan to teacher
  [ ] Applied approved revisions or proceeded with original
  [ ] Logged teacher decisions
      Output: 03_feedback_struggling_learner.json, 03_revision_plan.json, 03_revision_plan.md

STAGE 5: Generate materials
  [ ] Generated PowerPoint slide deck
      Output: 05_slides.pptx
  [ ] Generated Word document
      Output: 06_worksheet.docx

STAGE 6: Validate outputs
  [ ] Ran validate_outputs.py script
  [ ] Reviewed validation report
  [ ] Addressed any errors
      Output: 07_validation_report.txt

STAGE 7: Present to teacher
  [ ] Summarized what was created
  [ ] Provided file locations
  [ ] Offered next steps
      Output: Summary and file locations

SESSION COMPLETE!

Session files location: .lesson-designer/sessions/{session_id}/
  - 01_input.json
  - 02_competency_breakdown.json
  - 03_lesson_design_v1.json (and v2, v3 if iterations)
  - 04_lesson_final.json
  - 05_slides.pptx
  - 06_worksheet.docx
  - 07_validation_report.txt
```

**Quick Reference - Script Commands:**

```bash
# Stage 3b: Validate cognitive rigor
python .claude/skills/lesson-designer/scripts/validate_marzano.py \
  .lesson-designer/sessions/{session_id}/03_lesson_design_v1.json

# Stage 3.5: Persona feedback & revision
python .claude/skills/lesson-designer/scripts/persona_evaluator.py \
  .lesson-designer/sessions/{session_id}/04_lesson_final.json \
  .claude/skills/lesson-designer/personas/struggling_learner.json \
  .lesson-designer/sessions/{session_id}/03_feedback_struggling_learner.json

python .claude/skills/lesson-designer/scripts/generate_revision_plan.py \
  .lesson-designer/sessions/{session_id}/03_feedback_struggling_learner.json \
  .lesson-designer/sessions/{session_id}/03_revision_plan.json \
  --markdown .lesson-designer/sessions/{session_id}/03_revision_plan.md

# Stage 5: Generate slides
# Claude generates slides directly using python-pptx (see design principles above)
# No script required - Claude writes and executes the code

# Stage 5 Part 2: Generate worksheet
python .claude/skills/lesson-designer/scripts/generate_worksheet.py \
  .lesson-designer/sessions/{session_id}/04_lesson_final.json \
  .lesson-designer/sessions/{session_id}/06_worksheet.docx

# Stage 5b: Generate simulation (optional)
python .claude/skills/lesson-designer/scripts/generate_simulation.py \
  --competency "Students will analyze..." \
  --simulation-type "physics" \
  --output "simulation.html"

# Stage 5c: Generate assessment (optional)
python .claude/skills/lesson-designer/scripts/generate_assessment.py \
  --lesson-file .lesson-designer/sessions/{session_id}/04_lesson_final.json \
  --assessment-type "quiz" \
  --output .lesson-designer/sessions/{session_id}/quiz.docx

# Stage 6: Validate outputs (now includes Phase 2 checks)
python .claude/skills/lesson-designer/scripts/validate_outputs.py \
  .lesson-designer/sessions/{session_id}/
```

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

**Version:** 2.0.0
**Last updated:** 2026-01-25
**Framework:** [Marzano's New Taxonomy](./MARZANO.md)
