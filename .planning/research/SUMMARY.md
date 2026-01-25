# Project Research Summary

**Project:** Lesson Planning Skill for Claude
**Domain:** Educational design systems with AI-driven multi-stage workflows
**Researched:** 2026-01-25
**Confidence:** HIGH

## Executive Summary

The lesson-designer skill is a Marzano framework-based educational tool that generates classroom-ready PowerPoint and Word documents through a five-stage pipeline with student persona feedback loops. This is NOT a typical CRUD app or API service—it's a Claude skill using filesystem-based orchestration, Python document generation libraries (python-pptx, docxtpl), and prompt chaining to implement complex multi-stage workflows entirely within Claude's execution environment.

The recommended approach is to build incrementally: start with core lesson generation (Stage 0-1-4, skipping feedback loops), validate file generation and Marzano framework implementation, then add single-persona feedback (Stage 2-3) before scaling to full multi-persona validation. This de-risks the most critical unknowns—can we generate pedagogically sound materials that address known pain points (overly detailed slides, single-spaced worksheets, missing discussion structure)?—before investing in the sophisticated feedback architecture.

The primary risk is context window bloat degrading quality across multi-lesson sequences. Research shows 11 of 12 LLMs drop below 50% performance at 32k tokens, and lesson sequences accumulate context rapidly (framework docs + lesson history + persona definitions + feedback). Mitigation: implement context compression after every 3 lessons, maintain "lesson essence" summaries rather than full content, and follow the GSD pattern of small focused agents with minimal context sharing.

## Key Findings

### Recommended Stack

Claude Skills are filesystem-based instruction sets executed in Claude's native Python environment—NOT separate agents or API services. This fundamentally shapes the architecture: multi-stage workflows use prompt chaining within a single skill (or coordinator + subagents), the filesystem serves as state management, and there's zero deployment complexity.

**Core technologies:**
- **python-pptx (1.0.0+)**: PowerPoint generation — Industry standard, template support (critical for branded materials), can read existing files for round-trip editing
- **docxtpl (0.20.x+)**: Word document templating — Enables Jinja2 templates in .docx, separates content generation from formatting, allows teacher customization of templates without touching code
- **Filesystem-based state**: Session management via JSON files — Token-efficient, resumable, survives context compaction, enables parallel execution, proven pattern (74.0% LoCoMo benchmark)
- **Prompt chaining**: Sequential workflow stages — No external orchestration, Claude handles state between steps, follows Anthropic's documented best practices

**Why this stack wins:** Zero infrastructure (no deployment, no network calls, no databases), libraries are pre-installed in Claude's environment, templates separate design from content (teachers control formatting), and the filesystem pattern outperforms specialized graph-based memory systems in benchmarks.

### Expected Features

Educational AI tools in 2026 are dominated by AI-powered automation, but current tools focus on generating planning documents rather than delivery-optimized materials. This creates the opportunity: build for the teaching moment, not just the planning artifact.

**Must have (table stakes):**
- Standards alignment (Common Core + 50 state standards) — Required for compliance, users expect AI-assisted mapping
- Cloud storage & collaboration — Cross-device access is baseline expectation
- Multi-format export (PDF, Word, PowerPoint) — Interoperability requirement, teachers need to print and share
- Lesson plan templates — Industry standard since pre-digital era
- Multi-lesson sequence planning — Market gap: most tools focus on single lessons, teachers need 2-4 week units

**Should have (competitive differentiators):**
- **Marzano taxonomy-guided design** — Structures lessons through Retrieval → Comprehension → Analysis → Knowledge Utilization levels, ensures cognitive rigor (CORE DIFFERENTIATOR)
- **Competency decomposition** — Converts high-level competencies into discrete skills + knowledge components (addresses "where do I start?" problem)
- **Teacher-led slide design** — Minimal text, visual prompts, NOT text-heavy self-study materials (ADDRESSES KNOWN PAIN POINT)
- **Properly formatted worksheets** — Double-spaced, adequate answer space, writable (ADDRESSES KNOWN PAIN POINT)
- **Student persona feedback** — Simulates 4 student types (struggling, on-level, advanced, neurodivergent) to catch design flaws before classroom (UNIQUE INNOVATION)
- **Discussion protocol integration** — Pre-designed structures with timing, roles, prompts (fills gap in current tools)

**Defer (v2+):**
- Advanced differentiation scaffolds (provide basic supports in MVP, automate later)
- Image/diagram generation (use placeholders in MVP)
- Cognitive load analysis (manual validation first, automate later)
- Extensive collaboration features (basic sharing sufficient)

**Anti-features (do NOT build):**
- Generic "AI lesson generator" without pedagogical framework (produces low-quality one-size-fits-all)
- Extensive pre-built lesson library (teachers want customization, not canned lessons)
- All-in-one LMS (scope creep, competing with established players)
- Overly detailed slides (the exact pain point to avoid)

### Architecture Approach

The skill should follow an orchestrator-worker pattern with filesystem-based state management. Each stage (input validation → lesson design → feedback collection → revision planning → output generation) produces verifiable intermediate outputs stored as JSON/markdown files, creating explicit state transitions that survive context resets and enable debugging.

**Major components:**

1. **State Management Layer** — Session directories with immutable stage outputs (.lesson-designer/sessions/{id}/)
   - Provides token efficiency (stages read only relevant artifacts)
   - Enables resumability (checkpoint files track progress)
   - Supports parallel execution (Stage 2 personas all read lesson_draft_v1.json)
   - Survives context compaction (filesystem persists beyond conversation)

2. **Plan-Validate-Execute Pattern** — Each stage follows: generate proposal → validate against rules → execute if passing
   - Stage 1: Draft lesson → validate Marzano framework (script) → save if valid
   - Stage 2: Generate persona feedback → validate format → save to individual files
   - Stage 3: Aggregate feedback into revision plan → teacher approval (human-in-the-loop) → proceed if confirmed
   - Stage 4: Generate files → validate outputs exist and are not corrupt → deliver

3. **Progressive Disclosure** — Main SKILL.md references stage-specific docs loaded on-demand
   - MARZANO_FRAMEWORK.md loads only when designing lessons (saves tokens)
   - STUDENT_PERSONAS.md loads only during feedback stage
   - Output generation scripts executed, not read (documentation in SKILL.md, not docstrings)

**Build order recommendation:** Single skill for MVP (simpler debugging, faster iteration), refactor to coordinator + subagents for production (parallelizes Stage 2 personas, uses Haiku for evaluations to cut costs, enforces context isolation).

### Critical Pitfalls

Research identified 14 pitfalls ranging from critical to minor. Top 5 by severity and relevance:

1. **AI content promotes only basic-level thinking** — 90% of AI lesson plans in research emphasized recall over analysis/evaluation. Prevention: Bloom's Taxonomy enforcement, minimum 40% higher-order activities, Marzano strategy markers embedded in prompts. **Address in Phase 1.**

2. **Content written for self-study instead of teacher-led instruction** — Known issue from user's existing tool. Slides contain dense paragraphs, not talking points. Prevention: Separate generation logic for teacher materials (minimal text, presenter notes, discussion prompts) vs. student materials (space for notes, guided questions). **Address in Phase 1.**

3. **Context window bloat causing quality degradation** — Lesson 5 in a sequence becomes worse than Lesson 1 as context accumulates. Research shows performance drops below 50% at 32k tokens. Prevention: Context compression every 3 lessons, "lesson essence" summaries, structured handoffs (key decisions only, not full history), GSD pattern of small focused agents. **Address in Phase 6 (multi-lesson sequences).**

4. **Generic, uninspiring, culturally homogeneous content** — Default AI outputs gravitate toward dominant training patterns, fail UDL principles. Prevention: Require diverse examples across cultures, activity variety requirements (minimum 3 types per lesson), UDL framework checkpoints, teacher-specified cultural context. **Address in Phase 1 (core generation) and Phase 4 (activity generation).**

5. **Vague prompts leading to unpredictable outputs** — Complex skills with bloated context windows degrade performance. Prevention: Apply 2026 prompt engineering best practices (precise, structured, goal-oriented), specify format explicitly, use structured input validation, maintain lean prompts (<13KB per production teams), build format examples into prompts. **Address in Phase 0 (planning standards).**

**Also critical from known user issues:**
- Worksheets not formatted for writing (single-spaced) — Prevention: Material-type-specific formatting rules, double-spacing for student responses. **Address in Phase 2.**
- No structure/timing for discussions — Prevention: Required time allocation (ranges: 10-15 min), discussion structure (opening, prompts, closing), teacher facilitation notes. **Address in Phase 4.**

## Implications for Roadmap

Based on research, the highest-risk-first build order is:

### Phase 1: Core Pipeline (No Feedback Loop)
**Rationale:** Validate the fundamental value proposition—can we generate pedagogically sound, delivery-optimized materials?—before investing in complex feedback architecture. Addresses user's known pain points immediately.

**Delivers:** Teacher provides competency → receives .pptx slides + .docx worksheets + lesson plan

**Addresses (from FEATURES.md):**
- Marzano taxonomy-guided design (core differentiator)
- Competency decomposition (solves "where do I start?")
- Teacher-led slide generation (addresses known pain point #1)
- Properly formatted worksheets (addresses known pain point #2)
- Basic standards alignment (table stakes)

**Avoids (from PITFALLS.md):**
- Self-study formatting (Pitfall #2) — Separate templates for teacher vs. student materials
- Basic-level thinking only (Pitfall #1) — Bloom's/Marzano taxonomy enforcement
- Generic content (Pitfall #4) — Diversity requirements, activity variety

**Implementation:** Stages 0 (input validation) + 1 (lesson generation) + 4 (output generation). Skip Stages 2-3 entirely.

**Why this order:** De-risks file generation (.pptx/.docx creation), tests Marzano framework implementation, validates core value before adding complexity. Simpler to debug (no multi-agent), faster iteration.

### Phase 2: Material Formatting & Quality Validation
**Rationale:** Before adding feedback loops, ensure generated materials are physically usable and pedagogically rigorous.

**Delivers:** Format validation scripts, print-quality worksheets, discussion timing/structure, cognitive demand analysis

**Addresses:**
- Discussion protocol integration (competitive differentiator)
- Timing guidance (practical usability)
- Worksheet formatting (known pain point #3)
- No discussion structure (known pain point #4)

**Avoids:**
- Worksheet formatting issues (Pitfall #6)
- Discussion activities without timing (Pitfall #7)
- Timing estimates wildly inaccurate (Pitfall #9)

**Implementation:** Build validation scripts (validate_marzano.py, validate_outputs.py), implement material-specific formatting rules, add timing database for activities.

### Phase 3: Single Persona Feedback Loop
**Rationale:** Prove feedback architecture with minimal complexity before scaling to 4 personas. Tests plan-validate-execute pattern.

**Delivers:** Lesson with single-perspective feedback (struggling learner) + revision planning + teacher confirmation gate

**Addresses:**
- Student persona feedback (unique innovation, but simplified to 1 persona)
- Teacher customization workflow (augmentation not automation)

**Avoids:**
- Over-reliance on AI (Pitfall #10) — Teacher approval required before revisions
- Missing human-in-the-loop gates (Architecture pitfall #3)

**Implementation:** Add Stage 2 (1 persona evaluation only) + Stage 3 (synthesis, revision planning, teacher confirmation). Sequential execution (simpler than parallel).

**Why this order:** Tests feedback loop architecture, validates revision synthesis, identifies issues with persona definitions. Easier to debug than 4 parallel personas.

### Phase 4: Multi-Persona Feedback System
**Rationale:** Full pedagogical validation with 4 complementary perspectives. Still sequential (parallelization deferred to optimization phase).

**Delivers:** Comprehensive multi-perspective feedback from struggling learner, on-level, advanced, neurodivergent personas

**Addresses:**
- Student persona feedback (full implementation of unique innovation)
- Marzano alignment audit (quality assurance)

**Implementation:** Expand Stage 2 to 4 personas, sequential evaluation (save parallelization for Phase 7), feedback aggregation logic handles conflicting feedback.

### Phase 5: Multi-Lesson Sequences
**Rationale:** Teachers need units (2-4 weeks), not just single lessons. This is where context management becomes critical.

**Delivers:** Unit-level planning with lesson interdependencies and skill-building progression

**Addresses:**
- Multi-lesson sequence planning (market gap, table stakes)
- Subject-agnostic design (any academic subject)

**Avoids:**
- Context window bloat (Pitfall #3) — **CRITICAL: Implement context compression from start**
- Inconsistent terminology (Pitfall #12) — Terminology registry across sequence
- Limited to single lessons (known user issue)

**Implementation:** Context compression after every 3 lessons, lesson essence summaries, terminology tracking, sequence-level validation. **Research flag:** This phase needs empirical testing for context management effectiveness.

### Phase 6: Cross-Subject Validation & Optimization
**Rationale:** Ensure universal applicability (math, science, ELA, social studies, arts) and optimize resource usage.

**Delivers:** Subject-specific enhancements, production-ready performance

**Addresses:**
- Universal subject coverage (user requirement)
- Subject-specific limitations (Pitfall #8)

**Implementation:** Test across minimum 5 subjects, subject-specific templates extend base template, refactor to coordinator + subagents architecture (parallel Stage 2, Haiku for evaluations).

**Why this order:** Optimization only matters once workflow is validated. Refactoring from working system is safer than premature optimization.

### Phase Ordering Rationale

- **Phase 1 first:** Highest risk = can we generate quality materials? Validate core value before complexity.
- **Phase 2 before feedback:** Materials must be usable before we can get meaningful feedback on them.
- **Phase 3 before Phase 4:** Prove feedback architecture with 1 persona before scaling to 4.
- **Phase 5 deferred until feedback works:** Multi-lesson context management is complex; ensure single-lesson quality first.
- **Phase 6 last:** Cross-subject testing and optimization require stable foundation.

This sequence follows software engineering principle: integrate vertically (end-to-end value) before expanding horizontally (more features).

### Research Flags

**Phases likely needing deeper research during planning:**

- **Phase 1:** File generation capabilities
  - **Gap:** Which Python libraries are available in Claude's execution environment? Are python-pptx and docxtpl pre-installed or do they require pip install (which won't work in API context)?
  - **Research:** Test library availability, validate .pptx/.docx generation, check template loading capabilities
  - **Flag for:** `/gsd:research-phase` to investigate document generation libraries

- **Phase 5:** Context management for sequences
  - **Gap:** What is optimal context compression strategy? How much degradation actually occurs across 10-lesson units?
  - **Research:** Benchmark token usage across sequences, test different compression approaches (full history vs. summaries vs. key decisions only)
  - **Flag for:** `/gsd:research-phase` to investigate context window management patterns

**Phases with standard patterns (skip research):**

- **Phase 2:** Validation scripts — Standard Python scripting, well-documented patterns
- **Phase 3:** Feedback loops — Architecture research completed, implementation is straightforward
- **Phase 4:** Multi-persona scaling — No new research needed, just expansion of Phase 3 pattern
- **Phase 6:** Subagent refactoring — Anthropic documentation is comprehensive

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Official Anthropic docs verified, python-pptx and docxtpl are mature and actively maintained, filesystem pattern validated by benchmarks (74.0% LoCoMo), skill architecture from production best practices |
| Features | HIGH | 2026 market analysis comprehensive, known user issues provide concrete pain points, Marzano framework well-documented, competitive landscape clear |
| Architecture | HIGH | Anthropic's multi-agent research system architecture documented, Claude Code subagent patterns official, filesystem state management proven, prompt chaining best practices from API docs |
| Pitfalls | MEDIUM-HIGH | Strong research base (2026 educational AI analysis, Claude skill anti-patterns, known user issues), some areas need empirical testing (context management thresholds, cross-subject validation) |

**Overall confidence:** HIGH

The stack, architecture, and features are all well-researched with authoritative sources. Pitfalls are based on current research and known issues, though some (particularly context window degradation thresholds) will require empirical validation during implementation.

### Gaps to Address

**During Phase 1 planning:**
- **Gap:** Library availability in Claude environment (python-pptx, docxtpl)
  - **How to handle:** Test in Claude Code first, have fallback to python-docx only (more verbose but guaranteed available)
  - **Validation:** Create test script that imports libraries and generates sample files

**During Phase 2 planning:**
- **Gap:** Marzano framework token limits (is reference doc too large for single load?)
  - **How to handle:** Check MARZANO_FRAMEWORK.md size, split into sections if needed (retrieval.md, comprehension.md, etc.)
  - **Validation:** Test progressive loading vs. full load, measure token impact

**During Phase 5 planning:**
- **Gap:** Actual context degradation thresholds for lesson sequences
  - **How to handle:** Build monitoring into implementation, measure quality metrics (Lesson 1 vs. Lesson 5 vs. Lesson 10)
  - **Validation:** Empirical testing with 10-lesson unit generation, A/B test compression strategies

**During Phase 6 planning:**
- **Gap:** Subject-specific requirements (math equation formatting, science lab safety, etc.)
  - **How to handle:** Teacher interviews per subject, subject matter expert review, domain-specific templates
  - **Validation:** Generate sample lessons across 5 subjects, SME evaluation

**Cross-cutting gap:**
- **Gap:** Optimal persona definition length and structure for consistent feedback
  - **How to handle:** Start with detailed rubrics (Phase 3), refine based on feedback quality, test variations
  - **Validation:** Compare feedback quality across different persona definition approaches

## Sources

### Primary (HIGH confidence)

**Claude Skills & Architecture:**
- Anthropic: How Anthropic built their multi-agent research system — Orchestrator-worker pattern, state management
- Anthropic: Building agents with Skills — Progressive disclosure, multi-stage design
- Claude API Docs: Skill authoring best practices — Plan-validate-execute, feedback loops
- Claude Code Docs: Create custom subagents — Subagent architecture, orchestration
- Claude API Docs: Chain complex prompts for stronger performance — Prompt chaining patterns

**Document Generation:**
- python-pptx official documentation — PowerPoint generation capabilities
- docxtpl official documentation — Jinja2 templating in Word
- GitHub: elapouya/python-docx-template — Template architecture reference

**Filesystem State Management:**
- Letta: Benchmarking AI Agent Memory — 74.0% LoCoMo benchmark for filesystem agents
- Arize: AI Agent interfaces in 2026 — Filesystem vs API vs Database tradeoffs
- Anthropic: Effective context engineering for AI agents — Context management patterns

**Educational AI & Pitfalls:**
- The Conversation: AI-generated lesson plans fall short (2026) — 90% promote only basic-level thinking
- NPR: The risks of AI in schools outweigh the benefits (2026) — Known quality issues
- EdWeek: Why AI May Not Be Ready to Write Your Lesson Plans (2025) — Timing, diversity issues

**Marzano Framework:**
- Marzano Evaluation Center: Focused Teacher Evaluation Model — 23 competencies, 4 domains
- Education Walkthrough: Understanding the Marzano Framework — New Taxonomy structure
- Marzano Resources: Compendium of Instructional Strategies — 332 strategies reference

### Secondary (MEDIUM confidence)

**Educational Tools Market:**
- Lifehub: AI Lesson Planning Guide 2026 — Current tool landscape
- Jotform: 12 Best Online Lesson Planners 2026 — Feature comparison
- Cognitive Future: Best AI Tools for Educators 2026 — Market trends

**Context Window Research:**
- Chroma Research: Context Rot — 11 of 12 LLMs drop below 50% at 32k tokens
- Medium: 3 Design Patterns to Stop Polluting AI Context Window — Compression strategies
- Factory.ai: The Context Window Problem — Scaling agents beyond token limits

**Prompt Engineering:**
- IBM: 2026 Guide to Prompt Engineering — Current best practices
- Prompt Builder: Claude Prompt Engineering Best Practices (2026) — Specificity requirements

### Tertiary (LOW confidence, needs validation)

**Implementation Details:**
- KDNuggets: Claude Code Anti-Patterns Exposed — Community observations, not official
- Medium: Claude Code Got 100x Better — Anecdotal improvements
- Steve Kinney: Sub-Agent Anti-Patterns — Training course material, not research

---
*Research completed: 2026-01-25*
*Ready for roadmap: YES*
