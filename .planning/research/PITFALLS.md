# Domain Pitfalls: Educational AI Tools & Lesson Planning

**Domain:** Educational AI Tools and Lesson Planning (Marzano Framework)
**Researched:** 2026-01-25
**Confidence:** MEDIUM-HIGH (based on current 2026 research, known user issues, and Claude skill development patterns)

---

## Critical Pitfalls

Mistakes that cause rewrites, user rejection, or fundamental product failure.

### Pitfall 1: AI-Generated Content That Promotes Only Basic-Level Thinking

**What goes wrong:** AI-generated lesson plans skew heavily toward lower-order cognitive tasks (memorization, reciting, summarizing) rather than higher-order thinking (analyzing, evaluating, creating).

**Why it happens:** LLMs default to formulaic patterns from training data that emphasize simple recall over critical thinking. Research analyzing 311 AI-generated lesson plans found that 90% promoted only basic-level thinking.

**Consequences:**
- Teachers reject the tool as pedagogically weak
- Students aren't challenged appropriately
- Lessons fail to align with modern educational standards emphasizing critical thinking
- Violates Marzano framework emphasis on higher-order cognitive processing

**Warning signs:**
- Activities dominated by "list," "define," "recall," "match" verbs
- Questions asking for factual recall rather than analysis
- Minimal synthesis, evaluation, or creation tasks
- Teacher feedback mentions lessons feel "dumbed down" or "worksheet heavy"

**Prevention strategy:**
- Implement Bloom's Taxonomy enforcement in lesson generation
- Require balance: minimum 40% of activities must target higher-order thinking
- Include specific Marzano strategy markers (hypothesis generation, experimental inquiry, investigation)
- Use example-based prompting with high-quality lesson models
- Build verification step that analyzes cognitive demand distribution

**Which phase should address it:**
- Phase 1 (Core lesson generation): Build taxonomy awareness into prompts
- Phase 3 (Quality assurance): Add cognitive demand analysis
- Phase 5 (Teacher customization): Allow teachers to specify cognitive level requirements

---

### Pitfall 2: Content Written for Self-Study Instead of Teacher-Led Instruction

**What goes wrong:** Generated materials (especially slides and handouts) are written as if students will read them independently, not as support for teacher-led classroom instruction.

**Why it happens:**
- LLMs trained on textbooks and educational websites that are designed for self-study
- No explicit distinction in prompts between instructional modes
- Known issue from user's existing tool: "Slides written for self-study instead of teacher-led instruction"

**Consequences:**
- Slides contain dense text paragraphs rather than talking points
- Teachers can't use materials as designed
- Breaks teacher-student interaction flow
- Classroom engagement drops
- Tool abandoned after first use

**Warning signs:**
- Slides with full paragraphs instead of bullet points
- Materials explain concepts in complete detail without leaving room for teacher elaboration
- No presenter notes or teacher guidance
- Absence of discussion prompts or interaction cues
- Materials feel like "reading assignments" rather than teaching tools

**Prevention strategy:**
- Enforce instructional mode parameter: explicitly specify "teacher-led classroom instruction"
- Separate generation logic for presentation materials vs. student handouts
- Slides should contain: concise bullet points, discussion prompts, visual anchors, presenter notes
- Student materials should include: space for notes, guided questions, structured writing areas
- Add examples showing teacher-led vs. self-study patterns

**Which phase should address it:**
- Phase 1 (Core generation): Separate templates for teacher materials vs. student materials
- Phase 2 (Material formatting): Build format validation for each material type
- Phase 6 (Multi-lesson sequences): Ensure consistency across lesson sequence

---

### Pitfall 3: Context Window Bloat Causing Performance Degradation

**What goes wrong:** As lessons accumulate context (multi-lesson sequences, revision history, framework documentation), the AI agent's performance degrades, producing lower-quality outputs or missing critical details.

**Why it happens:**
- "Context rot": as token count increases, model's ability to recall information decreases
- Multi-agent systems amplify the problem through context explosion
- Models claiming 200k tokens become unreliable around 130k tokens
- Research shows 11 of 12 tested LLMs dropped below 50% performance at 32k tokens

**Consequences:**
- Quality degrades in later lessons of a sequence
- Agent fixates on past patterns rather than current instructions
- Token costs skyrocket
- Increased latency
- Inconsistent outputs that confuse users

**Warning signs:**
- Lesson 5 in a sequence is noticeably worse than Lesson 1
- Agent repeats information from earlier in context
- Responses become generic or miss specific requirements
- Token usage grows exponentially with sequence length
- Users report "it worked better for single lessons"

**Prevention strategy:**
- Treat context as finite resource with diminishing returns
- Implement context compression: summarize completed lessons, retain only essential info
- Use structured handoffs between phases (key decisions, not full history)
- Set hard limits: if generating 10-lesson unit, compress after every 3 lessons
- Maintain "lesson essence" summaries (1-2 paragraphs) rather than full content
- Follow GSD pattern: small, focused agents with minimal context sharing

**Which phase should address it:**
- Phase 6 (Multi-lesson sequences): Critical - implement context management from start
- Phase 7 (Scaffolding): Prevent accumulation across lesson progression
- All phases: Keep agent instructions under 13KB (production best practice)

---

### Pitfall 4: Generic, Uninspiring, and Culturally Homogeneous Content

**What goes wrong:** AI-generated lessons are "decidedly boring, traditional and uninspiring" and fail to include multicultural, diverse, or inclusive content.

**Why it happens:**
- LLMs gravitate toward dominant patterns in training data
- No explicit diversity or engagement requirements
- Default to traditional "teacher shows PowerPoint" approach
- Miss local context and cultural relevance

**Consequences:**
- Teachers find content unusable for diverse classrooms
- Students disengage with culturally irrelevant examples
- Tool perceived as perpetuating educational inequity
- Fails Universal Design for Learning (UDL) principles
- Negative word-of-mouth from teachers

**Warning signs:**
- Examples use only Western/majority culture references
- Activities lack variety (mostly worksheets and lectures)
- No accommodation for different learning styles
- Feedback mentions "boring," "generic," "cookie-cutter"
- Absence of student choice or voice

**Prevention strategy:**
- Require diverse examples across cultures, contexts, backgrounds
- Implement activity variety requirements (minimum 3 different activity types per lesson)
- Include UDL framework checkpoints in generation
- Provide multiple means of representation, expression, and engagement
- Build "engagement audit" into quality checks
- Allow teachers to specify cultural context and student demographics

**Which phase should address it:**
- Phase 1 (Core generation): Embed diversity and engagement requirements
- Phase 4 (Activity generation): Ensure activity type variety
- Phase 5 (Customization): Allow cultural context specification
- Phase 8 (Assessment): Include engagement criteria in quality metrics

---

### Pitfall 5: Vague or Ambiguous Prompts Leading to Unpredictable Outputs

**What goes wrong:** Prompts lack sufficient specificity, causing inconsistent or unusable lesson outputs. "Vague prompts produce vague results."

**Why it happens:**
- Assumption that AI "understands" educational context
- Underestimating importance of structured instructions
- Complex Claude skills with bloated context windows degrade performance
- Anti-pattern: treating complexity as sophistication

**Consequences:**
- Output quality varies wildly between uses
- Teachers can't rely on the tool
- Increased support burden ("it doesn't work")
- Users abandon tool after inconsistent experiences
- Difficult to debug or improve

**Warning signs:**
- Same input produces dramatically different outputs
- Teacher reports "sometimes it's great, sometimes terrible"
- Generated content misses obvious requirements
- Support requests asking "how do I make it work like last time?"
- Outputs ignore specified parameters

**Prevention strategy:**
- Apply 2026 prompt engineering best practices: precise, structured, goal-oriented phrasing
- Specify format explicitly: "5 bullet points, each under 15 words" not "be concise"
- Use structured input format with required fields
- Implement parameter validation before generation
- Follow GSD best practice: avoid complex slash commands and bloated context
- Maintain lean, focused prompts (production teams use <13KB agent files)
- Build examples into prompts showing exact desired output format

**Which phase should address it:**
- Phase 0 (Planning): Establish prompt engineering standards
- Phase 1 (Core generation): Implement structured input validation
- All phases: Regular prompt refinement based on output quality metrics
- Phase 9 (Testing): Test consistency across varied inputs

---

## Moderate Pitfalls

Mistakes that cause delays, technical debt, or reduced user satisfaction.

### Pitfall 6: Worksheet Formatting Unsuitable for Student Writing

**What goes wrong:** Generated worksheets use single-spacing or insufficient space for student responses, making them impractical for actual classroom use.

**Why it happens:**
- LLMs optimize for visual density (screen reading) not physical writing
- No explicit formatting requirements for student work
- Known issue from user's existing tool: "Worksheets not formatted for writing (single-spaced)"

**Consequences:**
- Teachers must manually reformat every worksheet
- Time savings promised by AI tool evaporate
- Students frustrated by cramped writing space
- Printed materials look unprofessional

**Warning signs:**
- Teacher feedback about "cramped" or "single-spaced" worksheets
- Support requests about formatting
- Users manually editing every generated worksheet
- Worksheets look good on screen but terrible when printed

**Prevention:**
- Implement formatting rules specific to material type
- Worksheets: 1.5 or double spacing, minimum line heights, adequate margins
- Specify "formatted for handwritten student responses"
- Include format validation step
- Provide print preview or "classroom-ready" formatting option
- Follow best practices: larger fonts and white space for K-2, consistent spacing for all grades

**Which phase should address it:**
- Phase 2 (Material formatting): Implement print-friendly formatting rules
- Phase 4 (Activity generation): Apply formatting to all student-facing materials
- Phase 9 (Testing): Include print quality in acceptance criteria

---

### Pitfall 7: Discussion Activities Without Timing or Structure

**What goes wrong:** Generated lessons include "think-pair-share" or discussions without time allocations, facilitation guidance, or clear structure.

**Why it happens:**
- AI includes activities without operational detail
- No requirement for timing or facilitation notes
- Known issue from user's existing tool: "No structure/timing for discussions"

**Consequences:**
- Teachers don't know how long to allocate
- Discussions fall flat or run over time
- Classroom management issues
- Teachers revert to safer, more predictable activities
- Tool seen as "good for ideas, not practical implementation"

**Warning signs:**
- Lesson plans list "class discussion" with no further detail
- No time estimates for activities
- Missing facilitation prompts or question sequences
- Teacher feedback: "I don't know how to actually do this"
- Timing estimates "bewilderingly inaccurate"

**Prevention:**
- Require time allocation for every activity (with ranges: 10-15 minutes)
- Generate discussion structure: opening question, facilitation prompts, closing synthesis
- Include differentiation: what if discussion finishes early? runs long?
- Provide teacher notes with common pitfalls and tips
- Align with Marzano framework discussion strategies

**Which phase should address it:**
- Phase 4 (Activity generation): Build timing and structure into all interactive activities
- Phase 7 (Scaffolding): Ensure progression logic includes time management
- Phase 1 (Core generation): Require timing for all lesson components

---

### Pitfall 8: Subject-Specific Limitations Preventing Universal Application

**What goes wrong:** Tool works well for certain subjects (e.g., social studies) but fails for others (math, lab sciences, arts) due to hard-coded assumptions.

**Why it happens:**
- LLMs have different performance across domains
- Framework designed around one subject area
- Insufficient testing across disciplines
- User goal: "universal (any academic subject)"

**Consequences:**
- Limited market adoption
- Bad reviews from teachers in unsupported subjects
- Feature requests for subject-specific customization
- Competitive disadvantage

**Warning signs:**
- Math lesson plans lack proper equation formatting
- Science lessons don't include lab safety or materials lists
- Arts lessons missing visual examples or demonstration steps
- Different quality levels across subjects in testing

**Prevention:**
- Design subject-agnostic core framework
- Build subject-specific enhancement modules (optional)
- Test across minimum 5 diverse subjects: math, science, ELA, social studies, arts
- Create subject-specific templates that extend base template
- Include subject parameter in generation with domain-specific validation
- Align with UDL principles: framework should work across all disciplines

**Which phase should address it:**
- Phase 1 (Core generation): Design subject-agnostic base
- Phase 5 (Customization): Add subject-specific enhancements
- Phase 9 (Testing): Test across all major subject areas
- Phase 6 (Multi-lesson): Ensure sequences work for all subjects

---

### Pitfall 9: Timing Estimates That Are "Bewilderingly Inaccurate"

**What goes wrong:** AI-generated time estimates for activities are wildly off (30-minute activity takes 10 minutes or 60 minutes in practice).

**Why it happens:**
- LLMs have no grounded understanding of classroom time
- No validation against real classroom data
- Timing varies by grade level, student ability, class size
- AI can't account for transitions, setup, cleanup

**Consequences:**
- Teachers lose trust in the tool
- Lesson pacing breaks down
- Teacher scrambles to fill time or rushes through content
- Classroom management issues

**Warning signs:**
- Teacher feedback about inaccurate timing
- Same activity type gets wildly different estimates
- No consideration of grade level in timing
- Missing time for transitions, setup, cleanup
- Timing doesn't account for differentiation

**Prevention:**
- Build timing database from real classroom observations
- Include grade-level multipliers (K-2 activities take 1.5x longer)
- Add transition time buffers (5 minutes between activities)
- Provide time ranges, not exact times (15-20 minutes, not 17 minutes)
- Include "flex time" recommendations
- Generate backup activities for early finishers
- Add teacher customization: adjust all timings by % based on their class

**Which phase should address it:**
- Phase 1 (Core generation): Implement realistic timing algorithm
- Phase 4 (Activity generation): Include activity-specific timing data
- Phase 5 (Customization): Allow teacher timing adjustments
- Phase 7 (Scaffolding): Account for learning curve in sequences

---

### Pitfall 10: Over-Reliance on AI Reduces Teacher Confidence and Expertise

**What goes wrong:** Teachers use AI-generated lessons without critical engagement, leading to reduced confidence in delivering content and atrophy of pedagogical reasoning.

**Why it happens:**
- "Cognitive offloading": external tools do mental work, causing reasoning to atrophy
- Tool positioned as replacement rather than augmentation
- No prompts for teacher reflection or customization
- Research finding: "while generative AI improved teachers' productivity, it reduced their confidence"

**Consequences:**
- Teachers feel deskilled
- Quality of instruction declines
- Teachers can't adapt when lessons don't work
- Professional development concerns
- Ethical concerns about AI replacing teacher expertise

**Warning signs:**
- Teachers use outputs without modification
- Inability to explain pedagogical choices in lessons
- Requests for AI to "just tell me what to do"
- Decreased teacher engagement in planning process
- Teachers can't troubleshoot when lessons fail

**Prevention:**
- Position tool as "augmentation not automation"
- Design 80/20 workflow: AI drafts 80%, teacher customizes 20%
- Require teacher input on key decisions (learning objectives, assessment criteria)
- Include prompts for reflection: "Why does this sequence make sense?"
- Provide pedagogical explanations alongside generated content
- Make customization easy and expected
- Follow educational best practice: "AI enhances but cannot replace teacher-led instruction"

**Which phase should address it:**
- Phase 0 (Planning): Establish augmentation philosophy
- Phase 5 (Teacher customization): Make customization central to workflow
- Phase 1 (Core generation): Include pedagogical reasoning in outputs
- Phase 10 (Documentation): Emphasize teacher expertise in guidance

---

### Pitfall 11: Poor Integration with Existing Teacher Workflows

**What goes wrong:** Tool exists in isolation, requiring teachers to manually copy/paste content into their actual planning systems (Google Classroom, LMS, grade book).

**Why it happens:**
- Focus on generation quality, not workflow integration
- Underestimating importance of "last mile" problem
- 2026 research finding: "barriers to AI adoption: lack of seamless integration"

**Consequences:**
- Tool feels like "extra work" rather than time-saver
- Teachers abandon after initial trial
- Competitive disadvantage vs. integrated solutions
- Reduced actual time savings

**Warning signs:**
- Teachers copy/paste outputs into other tools
- Requests for export to specific formats
- Low retention despite good generation quality
- Feedback: "good content but too much manual work"

**Prevention:**
- Export to common formats: Google Docs, Microsoft Word, PDF
- Consider future integration with Google Classroom, Canvas, Schoology
- Provide structured export (not just plain text)
- Allow direct sharing/collaboration
- Maintain formatting in exports
- Design outputs that work in multiple contexts

**Which phase should address it:**
- Phase 2 (Material formatting): Design export-friendly formats
- Phase 11 (Export/sharing): Implement multiple export options
- Phase 5 (Customization): Ensure customizations survive export

---

## Minor Pitfalls

Mistakes that cause annoyance but are easily fixable.

### Pitfall 12: Inconsistent Terminology Across Lesson Sequence

**What goes wrong:** In multi-lesson units, terms, definitions, or concept names vary between lessons, confusing students.

**Why it happens:**
- Each lesson generated independently
- No terminology dictionary maintained across sequence
- LLMs use synonym variation for "natural" writing

**Consequences:**
- Student confusion
- Teacher must edit for consistency
- Appears unprofessional

**Warning signs:**
- Same concept called different names in different lessons
- Definitions shift slightly across lessons
- Inconsistent capitalization or formatting of key terms

**Prevention:**
- Maintain terminology registry for each unit
- First lesson establishes key terms, subsequent lessons use same terms
- Validate consistency across lesson sequence
- Provide glossary generation

**Which phase should address it:**
- Phase 6 (Multi-lesson sequences): Implement terminology tracking
- Phase 3 (Quality assurance): Add consistency validation

---

### Pitfall 13: Missing Materials Lists or Unrealistic Resource Requirements

**What goes wrong:** Lessons require materials not specified in materials list, or specify resources teachers don't have access to.

**Why it happens:**
- Materials generation separate from activity generation
- No validation that activities match materials
- AI suggests ideal resources without considering availability

**Consequences:**
- Teachers can't execute lesson as designed
- Last-minute scrambling for materials
- Frustration and tool abandonment

**Warning signs:**
- Activities mention materials not in materials list
- Expensive or specialized equipment required without alternatives
- No consideration of school budget or resources
- Science labs requiring unavailable equipment

**Prevention:**
- Generate materials list from activities, not separately
- Validate: all activity materials appear in list
- Provide alternatives for specialized resources
- Include "materials-light" options
- Allow teacher to specify available resources
- Flag expensive/specialized items with budget estimates

**Which phase should address it:**
- Phase 4 (Activity generation): Generate materials lists from activities
- Phase 3 (Quality assurance): Validate materials/activity alignment
- Phase 5 (Customization): Resource availability parameters

---

### Pitfall 14: Accessibility Overlooked (Violates UDL Principles)

**What goes wrong:** Generated materials don't consider students with disabilities, English language learners, or different learning needs.

**Why it happens:**
- Default to "typical" student assumptions
- UDL principles not embedded in generation
- No accessibility validation

**Consequences:**
- Materials don't meet legal requirements (ADA, IEP)
- Teachers must retrofit accessibility
- Excludes significant student populations
- Ethical concerns about equitable access

**Warning signs:**
- No alternative text for images
- Single modality for information (text-only or visual-only)
- No scaffolding for different ability levels
- Missing accommodations or modifications sections
- Colorblind-unfriendly materials

**Prevention:**
- Embed UDL framework in all generation
- Provide multiple means of representation, expression, engagement
- Include alt text for all visuals
- Generate differentiation suggestions automatically
- Validate against WCAG accessibility guidelines
- Include accommodation suggestions for common needs

**Which phase should address it:**
- Phase 1 (Core generation): Embed UDL from start
- Phase 4 (Activity generation): Multiple modalities for all activities
- Phase 7 (Scaffolding): Accessibility in differentiation

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation | Detection Method |
|-------------|---------------|------------|------------------|
| Core Lesson Generation | Generic, low-cognitive-demand content | Implement Bloom's Taxonomy validation; require Marzano strategy markers | Analyze verb distribution; teacher feedback |
| Material Formatting | Self-study formatting instead of teacher-led | Separate templates for teacher vs. student materials; enforce presenter notes | Review slide density; check for discussion prompts |
| Quality Assurance | Missing validation of cognitive demand and engagement | Build multi-dimensional quality rubric (cognitive level, engagement, diversity) | Automated analysis of activity types and thinking levels |
| Activity Generation | Timing estimates wildly inaccurate | Time database from real classrooms; grade-level multipliers | Teacher timing feedback; pilot testing |
| Teacher Customization | Teachers skip customization, leading to over-reliance | Make customization required step; show pedagogical reasoning | Track customization rates; teacher confidence surveys |
| Multi-lesson Sequences | Context window bloat causing quality degradation | Implement context compression after every 3 lessons | Monitor token usage; compare lesson 1 vs. lesson 10 quality |
| Scaffolding & Progression | Inconsistent terminology across lessons | Maintain terminology registry; validate consistency | Automated term tracking; glossary generation |
| Assessment Integration | Assessments misaligned with activities | Generate assessments from learning objectives, not independently | Alignment validation; Bloom's level matching |
| Testing & Validation | Insufficient cross-subject testing | Test across minimum 5 subjects; subject-specific validation | Subject matter expert review; multi-domain pilots |
| Documentation | Positioning as replacement vs. augmentation | Emphasize teacher expertise; show 80/20 workflow | User interviews; teacher confidence metrics |
| Export & Sharing | Poor format preservation in exports | Test exports in target systems; maintain formatting | Export quality testing; integration validation |

---

## Known Issues from User's Existing Tool

These pitfalls have already manifested in the user's current lesson planning tool and MUST be addressed:

### 1. **Slides Written for Self-Study** ✓ Addressed as Critical Pitfall #2
- Root cause: No distinction between instructional modes
- Solution: Separate generation logic for teacher-led materials

### 2. **Worksheets Not Formatted for Writing (Single-Spaced)** ✓ Addressed as Moderate Pitfall #6
- Root cause: Screen-optimized formatting, not print-optimized
- Solution: Material-type-specific formatting rules

### 3. **No Structure/Timing for Discussions** ✓ Addressed as Moderate Pitfall #7
- Root cause: Activities generated without operational detail
- Solution: Required timing and facilitation structure

### 4. **Limited to Single Lessons, Single Subject Area** ✓ Addressed as Moderate Pitfall #8 and Critical Pitfall #3
- Root cause: No multi-lesson architecture; subject-specific assumptions
- Solution: Context management for sequences; subject-agnostic framework

---

## Sources

### Educational AI Quality & Pedagogy
- [NPR: The risks of AI in schools outweigh the benefits](https://www.npr.org/2026/01/14/nx-s1-5674741/ai-schools-education)
- [The Conversation: AI-generated lesson plans fall short on inspiring students and promoting critical thinking](https://theconversation.com/ai-generated-lesson-plans-fall-short-on-inspiring-students-and-promoting-critical-thinking-265355)
- [EdWeek: Why AI May Not Be Ready to Write Your Lesson Plans](https://www.edweek.org/technology/why-ai-may-not-be-ready-to-write-your-lesson-plans/2025/06)
- [Medium: AI in Education Is a Wicked Problem](https://medium.com/the-balanced-sheet/ai-in-education-is-a-wicked-problem-6c01a68b48ec)
- [EdSurge: AI Is Changing Classrooms. Teacher Expertise Still Sets the Direction.](https://www.edsurge.com/news/2026-01-12-ai-is-changing-classrooms-teacher-expertise-still-sets-the-direction)

### Teacher Workflow & Integration
- [Lifehub: AI Lesson Planning Guide: Strategies for Teachers in 2026](https://www.lifehubeducation.com/blog/ai-lesson-planning)
- [Jotform: 12 best online lesson planners for teachers in 2026](https://www.jotform.com/blog/best-online-lesson-planner/)
- [Truth For Teachers: How to use AI to plan a lesson and still make it YOURS](https://truthforteachers.com/truth-for-teachers-podcast/ai-lesson-planning-for-teachers/)

### Lesson Planning Challenges
- [Ditch That Textbook: 15 Best Lesson Planning AI Tools For Teachers](https://ditchthattextbook.com/ai-lesson-planning/)
- [SchoolAI: A complete AI lesson planning guide for teachers](https://schoolai.com/blog/ai-lesson-planning-guide-teachers)
- [Medium: The Case Against Lesson Plans](https://medium.com/@LenaAngel/the-case-against-lesson-plans-fdf141c095f7)
- [Constructive Learning Design: When Lesson Plans Flop in the Classroom](https://www.constructivelearningdesign.org/2021/12/18/when-lesson-plans-flop-in-the-classroom/)

### Claude AI Skills & Anti-Patterns
- [KDNuggets: Claude Code Anti-Patterns Exposed](https://ai-report.kdnuggets.com/p/claude-code-anti-patterns-exposed)
- [Anthropic: Claude Code Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Medium: Claude Code Got 100x Better With Superpowers Skill](https://medium.com/@codeandbird/claude-code-got-100x-better-with-superpowers-skill-a36450f708b1)
- [Steve Kinney: Common Sub-Agent Anti-Patterns and Pitfalls](https://stevekinney.com/courses/ai-development/subagent-anti-patterns)

### Context Window Management
- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Medium: 3 Design Patterns to Stop Polluting Your AI Agent's Context Window](https://medium.com/@_init_/3-design-patterns-to-stop-polluting-your-ai-agents-context-window-dc979930db1d)
- [Chroma Research: Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot)
- [Factory.ai: The Context Window Problem: Scaling Agents Beyond Token Limits](https://factory.ai/news/context-window-problem)
- [Google Developers: Architecting efficient context-aware multi-agent framework for production](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)

### Prompt Engineering Best Practices
- [IBM: The 2026 Guide to Prompt Engineering](https://www.ibm.com/think/prompt-engineering)
- [Prompt Builder: Claude Prompt Engineering Best Practices (2026)](https://promptbuilder.cc/blog/claude-prompt-engineering-best-practices-2026)
- [Analytics Vidhya: Prompt Engineering Guide 2026](https://www.analyticsvidhya.com/blog/2026/01/master-prompt-engineering/)
- [Prompting Guide: Prompt Engineering Guide](https://www.promptingguide.ai/)

### Educational Materials Design & Formatting
- [Great Resources For Teachers: Creating Fun and Effective Worksheets](https://greatresourcesforteachers.com/creating-fun-and-effective-worksheets-tips-for-teachers/)
- [Design Work Life: These 38 School Fonts get an "A+" in 2026](https://designworklife.com/these-38-school-fonts-get-an-a-plus/)

### Universal Design for Learning
- [CAST: Universal Design for Learning Guidelines](https://udlguidelines.cast.org/)
- [Vanderbilt IRIS: Universal Design for Learning](https://iris.peabody.vanderbilt.edu/module/udl/)
- [Harvard GSE: Universal Design for Learning: Explore](https://www.gse.harvard.edu/professional-education/program/universal-design-learning-explore)

### Educational AI Trends & Content Generation
- [Integra: AI in Education: 5 Trends Shaping Publishing, Assessment, and Platforms in 2026](https://integranxt.com/blog/top-5-ai-in-education-trends-2026/)
- [MDPI: Generative AI in Education: Assessing Usability, Ethical Implications, and Communication Effectiveness](https://www.mdpi.com/2075-4698/14/12/267)
- [Fordham Institute: Some predictions about AI in education in 2026](https://fordhaminstitute.org/national/commentary/some-predictions-about-ai-education-2026)

### Teacher-Led Instruction vs. AI
- [Microsoft Education: Introducing Microsoft innovations and programs to support AI-powered teaching and learning](https://www.microsoft.com/en-us/education/blog/2026/01/introducing-microsoft-innovations-and-programs-to-support-ai-powered-teaching-and-learning/)
- [USAII: Part 1: AI in Education, Classroom Integration, and Impact in 2026](https://www.usaii.org/ai-insights/ai-in-education-classroom-integration-and-impact-in-2026)
- [Getting Smart: How Teachers Can Orchestrate a Classroom Filled with AI Tools](https://www.gettingsmart.com/2025/01/07/how-teachers-can-orchestrate-a-classroom-filled-with-ai-tools/)

---

## Research Methodology Note

This pitfalls analysis combines:
1. **Current 2026 research** on educational AI challenges and best practices
2. **Known issues** from the user's existing lesson planning tool
3. **Claude AI skill development** anti-patterns and production best practices
4. **Educational framework alignment** (Marzano, UDL, Bloom's Taxonomy)

Confidence level is MEDIUM-HIGH due to strong current research base and known user issues, with some areas (particularly multi-lesson context management and cross-subject validation) requiring empirical testing during development.
