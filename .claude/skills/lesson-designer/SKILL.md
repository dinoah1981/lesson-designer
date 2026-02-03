---
name: lesson-designer
description: Design complete, classroom-ready lessons using Marzano's framework with persona feedback. Produces slide decks, worksheets, and all supporting materials.
version: 4.0.0
author: Claude
---

# Lesson Designer Skill

Design pedagogically sound lessons using Marzano's New Taxonomy, validate through student personas, and generate complete classroom-ready materials.

## Workflow Overview

```
Stage 1: Gather Requirements     → Competency, grade, lesson count, duration
Stage 2: Decompose & Classify    → Skills, knowledge, teacher classifications
Stage 3: Design Lesson           → Activities with Marzano levels
Stage 4: Persona Feedback        → 4 personas evaluate, teacher selects revisions
Stage 5: Generate Materials      → Claude creates all materials directly
Stage 6: Download                → Teacher downloads files
```

## Framework Reference

See [MARZANO.md](./MARZANO.md) for the complete pedagogical framework including:
- Four cognitive levels (retrieval, comprehension, analysis, knowledge utilization)
- Minimum 40% higher-order thinking requirement
- Activity design guidance by level

## Stage Details

### Stage 1: Gather Requirements

Collect:
1. **Competency** - What students will be able to DO (skill-focused, not topic-focused)
2. **Grade level** - e.g., "7th grade", "AP", "College"
3. **Lesson count** - How many lessons for this competency
4. **Duration** - Minutes per lesson period
5. **Constraints** - Available materials, student background, etc.

**Validation:** Competencies must be skill-focused. Help teacher reframe topic-focused statements:
- "The Civil War" → "What skill should students demonstrate with Civil War content?"
- "Photosynthesis" → "What should students DO with their knowledge of photosynthesis?"

### Stage 2: Decompose & Classify

**Decompose** the competency into:
- **Skills** - What students will DO (verbs: analyze, evaluate, construct, compare)
- **Knowledge** - What students need to KNOW to perform the skills

**ELA Distinction:** Reading a text = KNOWLEDGE (exposure). Analyzing it = SKILL.

**Teacher classifies** each knowledge item:
- `needs_teaching` - Direct instruction required
- `already_assumed` - Brief retrieval practice only

**Set target proficiency:** novice → developing → proficient → advanced

### Stage 3: Design Lesson with Marzano

Design activities following Marzano's taxonomy:

| Lesson Type | Structure |
|-------------|-----------|
| Introducing | Retrieval (5-10 min) → Comprehension (15-20 min) → Analysis (10-15 min) → Application (10-15 min) → Assessment |
| Practicing | Retrieval (5 min) → Comprehension (10 min) → Analysis (15-20 min) → Knowledge Utilization (10-15 min) → Assessment |
| Applying | Retrieval (5 min) → Analysis (15-20 min) → Knowledge Utilization (20-25 min) → Assessment |
| Synthesizing | Retrieval (5 min) → Comprehension (10 min) → Analysis (15-20 min) → Knowledge Utilization (15-20 min) → Assessment |

**Each activity includes:**
- Name, duration, Marzano level
- Student-facing instructions
- Materials needed (be specific - these will be generated)
- Student output / deliverable
- Differentiation options

**Cognitive rigor requirement:** Minimum 40% higher-order thinking (analysis + knowledge utilization)

### Stage 4: Persona Feedback & Revision

Run lesson through 4 student personas:

| Persona | Focus | Key Questions |
|---------|-------|---------------|
| **Alex** (Struggling/ELL) | Access barriers | Vocabulary gaps? Reading level? Scaffolding? |
| **Jordan** (Unmotivated capable) | Relevance & autonomy | Why should I care? Any choice? |
| **Maya** (Interested capable) | Depth & inquiry | Can I go deeper? Interesting questions? |
| **Marcus** (High achieving) | Challenge ceiling | Am I just waiting? Real challenge? |

Each persona provides:
- Overall rating (1-5)
- Reaction (how they'd experience the lesson)
- Specific concerns with severity
- Recommendations

**Teacher reviews** feedback and selects which concerns to address. Conflicting recommendations are resolved through:
- Tiered support (scaffolded + challenge versions)
- Core + extension (all do core, capable extend)
- Student choice (multiple paths to same goal)

### Stage 5: Generate Materials

**This is where Claude generates everything directly**, using the finalized lesson plan and incorporated feedback.

#### 5.1 Slide Deck (PPTX)

**Slide 1 (HIDDEN):** Teacher lesson plan
```
Objective: [Student-friendly daily objective]
1. Do Now (X mins): [Activity + notes]
2. [Activity 2] (X mins): [Description + materials]
...
Materials needed: [List]
Anticipated misconceptions: [List]
```

**Slide 2:** Objective in Context
- Day's objective
- Connection to unit/prior learning

**Remaining slides:** One per activity
- Clean, sparse design (talking points, not paragraphs)
- 3-5 bullet points max per slide
- Timer/duration indicator
- Activity icon

**Formatting:**
- Helvetica or similar clean font
- Minimum 16pt (body 20pt+, titles 40pt)
- No text cutoff at edges
- Presenter notes with SAY/ASK/WATCH FOR guidance

#### 5.2 Student Worksheet (DOCX)

Structure varies by lesson type but always includes:
- Header with title, name/date fields
- Activity sections with appropriate response formats
- Exit ticket / formative assessment

**Key principle:** Worksheet sections must match what the activity actually asks students to do:
- If activity uses a graphic organizer → include the graphic organizer
- If activity needs data tables → include the data tables
- If activity has specific questions → include those questions

**Formatting:**
- Helvetica font throughout
- Double-spaced answer lines
- Adequate writing space (scales with cognitive complexity)

#### 5.3 Supplementary Materials (DOCX)

**Generate all materials referenced in activities.** If an activity mentions materials, create them:

| Material Type | When to Generate | Content |
|---------------|------------------|---------|
| Station cards | Station rotation activities | Instructions, data/content, 1-2 analysis questions per station |
| Data sheets | Investigation activities | Raw data, statistics, primary source excerpts |
| Graphic organizers | Compare/contrast, analysis | Structured visual template with labels |
| Vocabulary cards | Vocabulary activities | Term, definition, visual space, example space |
| Discussion guides | Socratic, group discussion | Central questions, follow-up prompts, facilitation notes |
| Role cards | Simulations, debates | Role description, goals, talking points |
| Rubrics | Performance tasks | Criteria with 4-level descriptors |

**Discovery Principle for Discussion/Station Materials:**
- DO NOT give away answers - provide raw information students must analyze
- Limit to 1-2 thought-provoking questions per card
- Questions should require synthesis, not fact-finding
- Avoid leading language - let students draw conclusions
- Think of each card as a mini case study or data set

**Good card structure:**
1. Topic/region title
2. Context paragraph (scene-setting, not answer-giving)
3. 3-5 data points, statistics, or examples (raw material for thinking)
4. 1-2 discussion questions requiring analysis
5. Space for students to record key takeaway

#### 5.4 Differentiated Versions (Optional)

If teacher selected persona concerns:

**Modified version (for Alex concerns):**
- Same objectives
- Added scaffolds: word banks, sentence starters, visual supports
- Simplified language where appropriate
- Chunked instructions

**Extension version (for Marcus concerns):**
- Same objectives
- Added depth: complex questions, research prompts
- Ceiling removal: open-ended challenges
- Independent inquiry options

### Stage 6: Download

Present all generated materials:
- Slide deck (.pptx)
- Student worksheet (.docx)
- Supplementary materials (.docx) - one file or bundled
- Modified worksheet (.docx) if generated
- Extension worksheet (.docx) if generated

Show lesson summary with:
- Competency, grade, duration
- Cognitive rigor percentage
- Assessment type
- Persona feedback summary

---

## Material Generation Guidelines

When generating materials, follow these principles:

### Slides

1. **Sparse is better** - Slides support teacher-led instruction, not self-study
2. **No text overflow** - Content must fit within slide boundaries
3. **Visual hierarchy** - Clear distinction between headers and content
4. **Consistent styling** - Same fonts, colors, spacing throughout
5. **Hidden first slide** - Complete lesson plan for teacher reference

### Worksheets

1. **Match the activity** - If activity says "complete graphic organizer," include that organizer
2. **Adequate space** - More complex thinking = more writing space
3. **Clear sections** - Visual separation between activities
4. **Assessment included** - Every worksheet ends with formative assessment

### Supplementary Materials

1. **Self-contained** - Each document works without additional explanation
2. **Student-facing clarity** - Grade-appropriate language
3. **Teacher notes where needed** - Setup instructions, timing, facilitation tips
4. **Discovery-oriented** - Provide evidence, not conclusions

### Differentiation

1. **Add, don't subtract** - Modified versions add scaffolds, don't remove content
2. **Same objectives** - All versions target the same learning goals
3. **Invisible to students** - Scaffolds feel like helpful tools, not "easy version"

---

## Persona Definitions

### Alex (Struggling Learner / ELL)
- Reading 2-3 years below grade level
- Vocabulary gaps in academic language
- Benefits from: visual supports, chunked text, sentence starters, word banks
- Barriers: dense text, undefined terms, complex instructions, time pressure

### Jordan (Unmotivated Capable)
- High ability, low engagement
- Asks "Why does this matter?"
- Benefits from: real-world connections, choice, autonomy, relevant examples
- Barriers: busywork, obvious answers, no clear purpose, rigid structure

### Maya (Interested Capable)
- High ability, high engagement
- Wants to go deeper
- Benefits from: inquiry opportunities, complex questions, extension paths
- Barriers: surface-level tasks, waiting for others, no depth options

### Marcus (High Achieving)
- Gifted learner, rapid mastery
- Often 3+ years above grade level
- Benefits from: challenge, open-ended problems, independence, ceiling removal
- Barriers: repetitive practice, waiting, no differentiation upward

---

## Version History

**v4.0.0** (2026-02)
- Removed script-based generation in favor of Claude-direct generation
- Simplified workflow while keeping pedagogical rigor
- Integrated Discovery Principle for discussion materials
- Materials now match activity requirements (not generic templates)

**v3.0.0** (2026-01)
- Added multi-lesson sequence support
- Added all 4 personas

**v2.0.0** (2026-01)
- Added persona feedback loop
- Added worksheet formatting improvements

**v1.0.0** (2026-01)
- Initial release with Marzano framework
