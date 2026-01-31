# Evidence-Based Mathematics Pedagogy Research: Grades 9-12

**Domain:** High School Mathematics Instruction (Grades 9-12)
**Research Focus:** Instructional sequences, lesson structures, and pedagogical approaches
**Researched:** 2026-01-31
**Overall Confidence:** HIGH

## Executive Summary

Evidence-based mathematics pedagogy for grades 9-12 reveals a paradigm shift from traditional direct instruction models toward more sophisticated, content-responsive approaches. **The central finding is that effective instruction is not a binary choice between direct instruction and inquiry, but rather strategic integration based on three factors: (1) content type (discovered concepts vs. decided conventions), (2) learner expertise level (novice vs. experienced), and (3) learning phase (initial exposure vs. practice vs. application).**

The research strongly contradicts the assumption that gradual release of responsibility ("I Do, We Do, You Do") represents best practice for all mathematical content. NCTM, cognitive science research, and practitioner evidence converge on the finding that this model often **prevents authentic mathematical problem-solving** and creates procedural dependency. When teachers demonstrate solutions before students grapple with problems, they eliminate the productive struggle essential for developing both conceptual understanding and problem-solving competence.

**Conceptual understanding must precede and coincide with procedural fluency instruction**—this is NCTM's official position (HIGH confidence) and is supported by cognitive load theory and multiple empirical studies. However, the relationship is iterative: procedural practice can deepen conceptual understanding when procedures are built from reasoning strategies rather than memorized algorithms.

A critical but often-overlooked finding is the **expertise reversal effect**: instructional techniques highly effective for novices (worked examples, explicit scaffolding) can produce negative learning outcomes for more experienced students. This has profound implications for automated lesson design—the system must assess prior knowledge and adjust scaffolding accordingly.

Research identifies distinct lesson frameworks for different purposes:
- **Launch-Explore-Summarize** for problem-centered learning of new concepts
- **Concrete-Representational-Abstract (CRA)** for building conceptual foundations
- **5 Practices model** for orchestrating mathematical discourse
- **Explicit instruction** for mathematical conventions and vocabulary

The most actionable finding for lesson design automation: **content type determines instructional approach**. If mathematicians discovered it (e.g., Pythagorean theorem, properties of functions), students should explore it. If mathematicians decided it (e.g., notation conventions, terminology), students should be told directly.

## 1. Direct Instruction Effectiveness: When and Why

### Key Findings

**Direct instruction (I Do, We Do, You Do / Gradual Release of Responsibility) is effective for:**

1. **Mathematical conventions and vocabulary** (HIGH confidence)
   - Source: [Math Coach's Corner](https://www.mathcoachscorner.com/2015/09/direct-instruction-do-we-need-it/)
   - Rationale: Content that was "decided" by mathematicians (notation, terminology, agreed-upon conventions) cannot be discovered through inquiry
   - Example: Teaching that "f(x)" means "function of x", that perpendicular symbol is ⊥, that "domain" refers to input values

2. **Foundational skill building for novice learners** (HIGH confidence)
   - Source: [PMC: Just How Effective is Direct Instruction?](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476697/)
   - Finding: Direct Instruction model shows strong evidence base across 50+ years of research (Engelmann et al.)
   - Caveat: This refers to capital-D-capital-I "Direct Instruction" (specific curriculum model), not generic teacher-centered instruction
   - Application: Explicit, systematic instruction particularly effective for building basic fluency before inquiry-based exploration

3. **Formalizing understanding after exploration** (HIGH confidence)
   - Source: [Edutopia: Direct Instruction and Inquiry in Math](https://www.edutopia.org/article/direct-instruction-inquiry-math-classes/)
   - Pattern: 20-30 min inquiry task → debrief discussion → note-taking and explicit instruction → guided practice
   - Rationale: "Inquiry opens questions that explicit instruction then answers"
   - Application: Direct instruction establishes common vocabulary, formalizes procedures, provides structured practice

4. **Worked examples for novice learners** (HIGH confidence)
   - Source: [Cognitive Load Theory research](https://www.tandfonline.com/doi/full/10.1080/01443410.2023.2273762)
   - Finding: Worked examples reduce cognitive load for novices, superior to unguided problem-solving on both retention and transfer tests
   - Pattern: Full worked example → faded worked example (student completes final steps) → independent practice
   - Critical caveat: Effectiveness decreases as learner expertise increases (expertise reversal effect)

**Direct instruction is NOT effective for:**

1. **Teaching problem-solving as the primary approach** (HIGH confidence)
   - Source: [NCTM: Rethinking Gradual Release](https://www.nctm.org/Publications/MTMS-Blog/Blog/Rethinking-the-Gradual-Release-of-Responsibility-Model/)
   - Problem: "When teachers show students how to solve problems, they aren't actually problem-solving but just following procedures"
   - Consequence: Students learn to execute algorithms but cannot adapt to novel situations
   - Research: 90% of AI-generated lessons emphasize recall over analysis/evaluation (The Conversation, 2026)

2. **Developing conceptual understanding of discoverable mathematics** (HIGH confidence)
   - Source: [Teaching Mathematics Through Problem Solving](https://fhsu.pressbooks.pub/ecumath/chapter/chapter-4-teaching-mathematics-through-problem-solving/)
   - Distinction: Content discovered by mathematicians (Pythagorean theorem, function properties, geometric relationships) should be discovered by students
   - Research: "Exploring mathematics problems before instruction improves understanding compared with instruct-then-practice sequence" ([PubMed](https://pubmed.ncbi.nlm.nih.gov/22849809/))
   - Mechanism: Problem exploration leads students to "accurately gauge competence, attempt larger variety of strategies, attend more to problem features—better preparing them to learn from instruction"

3. **Building mathematical agency and flexibility** (MEDIUM-HIGH confidence)
   - Source: [NCTM: Procedural Fluency Position](https://www.nctm.org/Standards-and-Positions/Position-Statements/Procedural-Fluency-in-Mathematics/)
   - Finding: Limiting instruction to single method "disadvantages learners and denies them access to intuitive approaches"
   - Goal: Students should think "Which strategy fits this problem?" not "How did my teacher show me?"
   - Evidence: Students learning fact strategies through reasoning outperform those using memorization ([IRIS Peabody](https://iris.peabody.vanderbilt.edu/module/math/cresource/q1/p03/))

### Critical Nuance: The Blended Model

**Research consensus (2024-2026): Both approaches needed, sequenced strategically** (HIGH confidence)

Pattern emerging across multiple authoritative sources:
1. **Inquiry/exploration first** (20-30 minutes) - Students grapple with novel problem, develop multiple strategies
2. **Facilitated discussion** - Gallery walks, peer review, sharing solution paths
3. **Explicit instruction** - Teacher formalizes concepts, introduces vocabulary, demonstrates efficient procedures
4. **Guided practice** - Students apply with decreasing scaffolding
5. **Independent application** - Transfer to new contexts

**Source convergence:**
- [Edutopia: Direct Instruction and Inquiry](https://www.edutopia.org/article/direct-instruction-inquiry-math-classes/)
- [Balancing Explicit and Inquiry-Based Learning](https://blog.booknook.com/balancing-explicit-and-inquiry-based-learning-math-intervention)
- [Teaching Math: Inquiry vs. Direct Instruction](https://teachpastthepotholes.com/math-inquiry-based-learning/)

Key quote: "There is clearly space for both of these approaches to coexist, and students do in fact benefit from both for different reasons" (Edutopia, 2026)

### Actionable Decision Rules for Automation

**DECISION TREE: When to use direct instruction**

```
IF content_type == "mathematical convention" OR content_type == "vocabulary":
    → START with explicit instruction
    → Follow with immediate application

ELSE IF content_type == "procedure" AND learner_expertise == "novice":
    → START with worked examples
    → Fade to guided practice
    → End with independent practice

ELSE IF content_type == "discoverable concept":
    → START with exploration/problem task (15-30 min)
    → FOLLOW with facilitated discussion
    → THEN explicit instruction to formalize
    → END with guided and independent practice

ELSE IF learner_expertise == "experienced":
    → MINIMIZE worked examples (expertise reversal)
    → START with problem-solving
    → Provide just-in-time scaffolding only when needed
```

**Content classification** (critical for automation):
- **Discovered by mathematicians** → students should explore: function behavior, geometric relationships, pattern generalization, proof strategies
- **Decided by mathematicians** → direct instruction: notation, terminology, conventional representations
- **Procedures** → CRA sequence (concrete → representational → abstract) with worked examples for novices

## 2. Productive Struggle and Problem-Based Learning

### Definition and Research Base

**Productive struggle** = "Students' effort to make sense of mathematics, to figure something out that is not immediately apparent" ([Springer](https://link.springer.com/article/10.1007/s10857-014-9286-3))

**Critical distinction:**
- **Productive struggle** ≠ frustration, despair, giving up
- **Productive struggle** = effortful thinking that leads to sense-making
- **Unproductive struggle** = lack of prior knowledge prevents progress

### Research Findings (HIGH confidence)

**1. Productive struggle is necessary for learning with understanding**
   - Source: [Multiple research studies](https://www.tandfonline.com/doi/full/10.1080/2331186X.2024.2442234)
   - Finding: "Struggling to make sense of mathematics is a necessary component of learning mathematics with understanding"
   - Problem-Based Teaching and Learning (PBTL) model identified as highly effective for first instruction ([Savvas Research](https://www.savvas.com/resource-center/more-topics/teacher-resources/mathematics/2020/envision-mathematics-problem-based-teaching))

**2. Four types of student struggles identified** ([University of Texas research](https://repositories.lib.utexas.edu/items/e824085b-5df9-4ad5-a0e3-e95b79672a2a)):
   - **Get started** - difficulty understanding problem or identifying entry point
   - **Carry out a process** - knows approach but encounters execution difficulties
   - **Give mathematical explanation** - can solve but cannot articulate reasoning
   - **Express misconception/errors** - reveals flawed understanding

**3. Teacher response continuum** (CRITICAL for automation):
   - **Telling** → **Directed guidance** → **Probing guidance** → **Affordance**
   - Effective teaching matches response to struggle type and learner needs
   - Research shows teachers with professional development in problem-based approaches have more positive attitudes toward struggle

**4. Eight effective teaching practices for supporting productive struggle** ([AAAS ARISE](https://aaas-arise.org/2022/11/09/productive-struggle-an-opportunity-for-in-depth-mathematics-learning/)):
   - Focus on students who don't provide correct answers
   - Praise perseverance (not just correctness)
   - Showcase creative solutions
   - Present non-routine problems
   - Provide feedback (not answers)
   - Avoid relegating struggling students to easy problems
   - Give sufficient discussion time
   - Encourage productive mental habits

### When Struggle Becomes Unproductive (MEDIUM confidence)

**Warning signs from research:**
- Student lacks sufficient prior knowledge ([WebSearch finding](https://www.edutopia.org/article/inquiry-based-learning-math/))
- Frustration replaces engagement
- Student stops attempting strategies
- Time investment exceeds learning benefit

**Prevention strategies:**
- Ensure prerequisite knowledge before exploration task
- Provide "just enough" scaffolding to restart thinking without removing challenge
- Set time boundaries (15-30 min for exploration phase)
- Use teacher response continuum (probing guidance before telling)

**2026 research emphasis** ([Make Math Moments](https://makemathmoments.com/math-resilience-2026-strategies/)):
- Focus on what makes struggle productive vs. frustrating
- Teach resilience explicitly with scaffolding, tools, and connections
- Provide access through multiple entry points

### Actionable Implementation for Automation

**PRODUCTIVE STRUGGLE PROTOCOL:**

**Phase 1: Problem Launch (5-10 min)**
- Present non-routine problem
- Activate prior knowledge
- Ensure all students understand WHAT is being asked (not HOW to solve)
- Multiple entry points (low floor, high ceiling)

**Phase 2: Exploration (15-25 min)**
- Students work independently or in small groups
- Teacher monitors for struggle types (get started, carry out process, explain, misconceptions)
- Teacher asks probing questions (not leading questions)
- Encourage multiple solution strategies

**Phase 3: Discussion (10-15 min)**
- Share student strategies (correct AND incorrect)
- Compare approaches
- Highlight creative thinking
- Connect to mathematical concepts

**Phase 4: Consolidation (10-15 min)**
- Formalize learning
- Introduce precise vocabulary
- Connect to standard procedures
- Bridge from student strategies to conventional methods

**Automated scaffolding decision tree:**
```
IF time_elapsed < 5 minutes AND student_stuck:
    → Clarify problem understanding (not solution path)

ELSE IF 5 min < time_elapsed < 15 min AND student_stuck:
    → Ask probing questions ("What have you tried?" "What do you know?")

ELSE IF 15 min < time_elapsed < 25 min AND student_stuck:
    → Provide directed guidance (hint at strategy, not solution)

ELSE IF time_elapsed > 25 min:
    → Transition to discussion phase (even if incomplete)
    → Struggle has exceeded productive window
```

## 3. Teaching Through vs. Teaching For Problem-Solving

### Core Distinction (HIGH confidence)

**Source:** [FHSU Pressbooks](https://fhsu.pressbooks.pub/ecumath/chapter/chapter-4-teaching-mathematics-through-problem-solving/), [Lesson Research](https://lessonresearch.net/teaching-problem-solving/overview/), [The Curriculum Journal](https://bera-journals.onlinelibrary.wiley.com/doi/10.1002/curj.213)

**Teaching FOR problem-solving:**
- Teach skill/procedure FIRST
- THEN apply to story problems
- Focus: Select tasks that promote understanding AFTER skill is learned
- Example: Learn two-digit multiplication algorithm → solve word problems requiring multiplication
- Issue: "Little or no evidence that students' problem-solving abilities improve" with generic strategy teaching ("draw a picture," "make a table")

**Teaching THROUGH problem-solving (TTP):**
- Students learn NEW mathematics BY solving problems
- Grapple with novel problem BEFORE instruction
- Present and discuss solution strategies
- Together build the next concept/procedure in curriculum
- Focus: "Focuses students' attention on ideas and sense-making, develops mathematical practices, builds confidence"

**Teaching ABOUT problem-solving:**
- Teach generic strategies ("draw a picture," "work backwards," "guess and check")
- Research verdict: Ineffective as standalone approach
- Students see word problems as "separate endeavor" and focus on steps rather than mathematics

### Research Evidence

**1. Current scholarly consensus** ([BERA](https://www.bera.ac.uk/blog/the-teaching-of-problem-solving-in-the-school-mathematics-curriculum)):
- "Recent scholarship leans towards teaching mathematics THROUGH problem solving"
- Means for students to "learn mathematics and come to appreciate what it means to do mathematics"

**2. Tension in research** ([Curriculum Journal 2023](https://bera-journals.onlinelibrary.wiley.com/doi/10.1002/curj.213)):
- Teaching all mathematics through problem-solving may be "effective and authentic way to learn content"
- BUT "not clear that this approach reliably results in students developing knowledge and skills to be powerful problem solvers when facing novel problems"
- Implication: May need combination of TTP for content learning + explicit problem-solving strategy instruction

**3. Implementation via Lesson Study** ([Frontiers](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2024.1331674/full)):
- Japanese Lesson Study approach uses TTP extensively
- Teachers report success "helping mathematics teachers enhance students' problem-solving skills with teaching through problem solving"
- Elementary teachers engaging with TTP using Lesson Study showed positive outcomes ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9099342/))

### Comparison of Approaches

| Aspect | Teaching FOR | Teaching THROUGH | Teaching ABOUT |
|--------|--------------|-------------------|----------------|
| **Sequence** | Skill → Application | Problem → Concept Development | Strategy → Application |
| **Student Role** | Apply learned procedure | Construct understanding | Follow strategy steps |
| **Problem Type** | Practice problems | Novel problems | Generic scenarios |
| **Outcome** | Procedure execution | Conceptual understanding + problem-solving | Variable (research shows limited effectiveness) |
| **When to Use** | Skill consolidation | New concept introduction | Rarely (research doesn't support) |
| **Research Support** | Traditional approach | Growing evidence base | Weak evidence |

### Actionable Implementation

**DECISION FRAMEWORK:**

**Use Teaching THROUGH Problem-Solving when:**
- Introducing new conceptual content (functions, similarity, probability)
- Content is discoverable (relationships, patterns, properties)
- Students have sufficient prerequisite knowledge
- Goal is deep understanding and sense-making
- Example: Launch with "Water Tank Problem" to develop linear function understanding

**Use Teaching FOR Problem-Solving when:**
- Consolidating learned procedures
- Providing application practice
- Building fluency with known methods
- Preparing for assessments that require standard procedures
- Example: After learning quadratic formula, solve various application problems

**AVOID Teaching ABOUT Problem-Solving as primary approach:**
- Generic strategies ("draw a picture") lack mathematical substance
- Research shows limited transfer to novel problems
- Exception: Can supplement TTP by making implicit strategies explicit during discussion phase

**LESSON STRUCTURE FOR TTP:**

1. **Launch** (5-10 min)
   - Present problem that creates "need" for new content
   - Activate prior knowledge
   - Ensure understanding of context (not solution method)

2. **Explore** (15-25 min)
   - Students grapple with problem using current knowledge
   - Multiple solution paths emerge
   - Partial solutions valued

3. **Discuss** (15-20 min)
   - Share student strategies (multiple approaches)
   - Compare efficiency and elegance
   - Identify mathematical relationships
   - Connect to new concept

4. **Consolidate** (10-15 min)
   - Formalize the mathematics
   - Introduce vocabulary and notation
   - Connect student methods to standard approaches
   - Name the concept/procedure developed

**Example (Teaching slope through problem-solving):**
- Launch: "Two phone plans: Plan A ($20 + $0.10/min), Plan B ($5 + $0.25/min). Which is better?"
- Explore: Students create tables, graphs, equations to compare
- Discuss: Share approaches, notice rate of change in each representation
- Consolidate: Formalize concept of slope/rate of change, m in y = mx + b

## 4. Conceptual Understanding Before Procedural Fluency

### NCTM Official Position (HIGH confidence)

**Source:** [NCTM Procedural Fluency Position Statement](https://www.nctm.org/Standards-and-Positions/Position-Statements/Procedural-Fluency-in-Mathematics/)

**Core principle:** "Conceptual understanding must precede and coincide with instruction on procedures"

**Key points:**
1. **Definition of procedural fluency:** "Ability to apply procedures efficiently, flexibly, and accurately; to transfer procedures to different problems and contexts"
   - Note: Fluency ≠ speed alone
   - Requires efficiency + flexibility + accuracy

2. **Relationship is iterative:** "Learning is supported when instruction on procedures and concepts is explicitly connected in ways that make sense to students and iterative"
   - Not strictly sequential (concept → procedure)
   - Mutual reinforcement pattern

3. **Build strategy repertoires:** "Students need multiple solution strategies before they can flexibly choose among them"
   - Limiting to single method "disadvantages learners and denies them access to intuitive approaches"

4. **Teach basic facts through reasoning:** "Basic facts should develop through number relationships and reasoning strategies"
   - Research shows students learning fact strategies outperform those using rote memorization
   - NOT timed drills (see anti-recommendations below)

5. **Assessment principles:** "Avoid timed tests, which can negatively impact students and don't measure true fluency"
   - Should evaluate efficiency, flexibility, accuracy—not just speed

### Supporting Research Evidence

**1. Conceptual foundations lead to better outcomes** (HIGH confidence)
- Source: [HMH: Conceptual Understanding in Math](https://www.hmhco.com/blog/what-is-conceptual-understanding-in-math)
- Finding: "Conceptual understanding makes learning skills easier, less error-prone, and easier to remember"
- Mechanism: Understanding WHY procedures work enables error detection and self-correction

**2. Mutual reinforcement model** (HIGH confidence)
- Source: [IM Certified Blog](https://illustrativemathematics.blog/2019/04/29/developing-conceptual-understanding-and-procedural-fluency/)
- Finding: "Conceptual and procedural knowledge are mutually reinforcing, but conceptual knowledge generally provides stronger foundation"
- Pattern: Conceptual foundations → reasoning strategies → procedural fluency (which deepens conceptual understanding)
- Research: "Memorizing an algorithm does not" support this iterative development

**3. Intervention research** (HIGH confidence)
- Source: [Multiple studies cited](https://greatminds.org/math/blog/eureka/how-to-help-students-build-deep-understanding-of-math-concepts)
- Finding: "Students who lack understanding of underlying concepts respond better to interventions that explicitly teach the concept instead of focusing on arithmetic or procedural fluency"
- Implication: Remediation should rebuild conceptual foundation, not drill procedures

**4. Recent emphasis (2024)** (MEDIUM-HIGH confidence)
- Source: [EdSurge](https://www.edsurge.com/news/2024-06-05-when-teaching-students-math-concepts-matter-more-than-process)
- Title: "When Teaching Students Math, Concepts Matter More Than Process"
- Context: Growing consensus that conceptual emphasis should increase

### The "AND" Not "OR" Principle

**Important nuance from research:**

Both are essential. The debate is not "conceptual OR procedural" but rather:
1. **Sequence question:** Which comes first? (Answer: Conceptual foundation)
2. **Emphasis question:** Which gets more time? (Answer: Depends on learning phase)
3. **Connection question:** How do we link them? (Answer: Explicitly, iteratively)

**Source:** [Minnesota STEM Teacher Center](https://stemtc.scimathmn.org/build-procedural-fluency-conceptual-understanding)
- "Build Procedural Fluency FROM Conceptual Understanding"
- NOT: Build concepts OR build fluency
- Key: "FROM" indicates directionality and foundation

**Source:** [Colorado Dept of Education](https://ed.cde.state.co.us/comath/onlinepd-facilitationguide-proceduralfluencyandconceptualunderstanding)
- "Procedural Fluency and Conceptual Understanding: Two Sides of the Same Coin"
- Cannot be separated; must develop together
- Conceptual provides foundation, procedural provides practice that deepens concepts

### Actionable Implementation

**LESSON DESIGN SEQUENCE:**

**Phase 1: Build Conceptual Foundation**
- Use concrete manipulatives or visual models
- Explore multiple representations
- Develop understanding of WHY procedure works
- Connect to prior knowledge
- Time: 1-2 lessons for new concept

**Phase 2: Bridge to Procedures**
- Show how understanding leads to efficient method
- Compare student-invented strategies to conventional procedure
- Explicitly connect conceptual model to symbolic representation
- Emphasize flexibility (multiple valid approaches)
- Time: 1 lesson

**Phase 3: Develop Fluency Through Meaningful Practice**
- Practice with decreasing scaffolding
- Varied problem types (not repetitive drill)
- Connect back to conceptual model when errors occur
- Emphasize reasoning ("Why does this work?")
- Time: Multiple lessons with spaced practice

**Phase 4: Application and Transfer**
- Apply procedures in novel contexts
- Choose appropriate strategy for problem type
- Explain reasoning behind procedural choices
- Time: Ongoing

**CONCRETE-REPRESENTATIONAL-ABSTRACT (CRA) SEQUENCE:**

**Source:** [Multiple research sources](https://thirdspacelearning.com/us/blog/concrete-representational-abstract-math-cpa/)

**Stage 1: Concrete (Enactive)**
- Physical manipulatives (blocks, algebra tiles, geometric models)
- Students physically model mathematical relationships
- Example: Use algebra tiles to model (x + 3)(x + 2)
- Research: Based on Bruner's theory of cognitive development

**Stage 2: Representational (Iconic)**
- Draw pictures/diagrams that represent concrete objects
- Bridge from physical to symbolic
- Example: Draw rectangles representing algebra tiles
- Reduces cognitive load while maintaining connection to concepts

**Stage 3: Abstract (Symbolic)**
- Numbers and symbols only
- Standard mathematical notation
- Example: (x + 3)(x + 2) = x² + 5x + 6
- Only after conceptual foundation established

**Research evidence:**
- "CRA sequence is an explicit methodology for teaching mathematics using multiple representations"
- "Learning concepts through multiple representations fosters conceptual understanding and mathematical thinking"
- Effective for diverse learners including students with disabilities ([PMC 2025 study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11660403/))

**AUTOMATION DECISION RULES:**

```
IF introducing_new_procedure:
    1. Start with conceptual exploration (CRA: Concrete phase)
    2. Build visual/representational understanding (CRA: Representational)
    3. Connect to symbolic procedure (CRA: Abstract)
    4. Practice with explicit conceptual connections
    5. AVOID teaching procedure as rote algorithm

ELSE IF building_fluency_with_known_procedure:
    1. Begin with brief conceptual reminder (WHY it works)
    2. Varied practice (different problem types)
    3. Emphasize flexibility (multiple valid approaches)
    4. Connect errors back to conceptual understanding
    5. AVOID timed tests or speed emphasis

ELSE IF student_struggling_with_procedure:
    1. Return to conceptual foundation (CRA: back to Concrete)
    2. Identify misconception in understanding
    3. Rebuild connection between concept and procedure
    4. Practice with scaffolding
    5. AVOID more procedural drill
```

## 5. Inquiry-Based Mathematics Instruction

### Research on Effectiveness (MEDIUM-HIGH confidence)

**Positive findings:**

**1. Student attitudes and self-efficacy** (HIGH confidence)
- Source: [PMC: Inquiry-Based Instruction in Middle School](https://pmc.ncbi.nlm.nih.gov/articles/PMC11245149/)
- Finding: "Positive and significant association between frequency of inquiry-based classroom activities and students' level of self-efficacy in mathematics"
- Effect: "Higher frequency predicted higher self-efficacy, interest, and perceptions of relevance"

**2. Achievement gains** (MEDIUM-HIGH confidence)
- Source: [Study of pre-algebra students](https://digitalcommons.cedarville.edu/cgi/viewcontent.cgi?article=1025&context=education_theses)
- Finding: "Both classes improved from pre-test to post-test, but students receiving inquiry-based instruction showed significantly more improvement on second unit"
- Caveat: Sample size and generalizability questions

**3. Transformative effects on attitudes** (MEDIUM confidence)
- Source: [Springer: Inquiry-Based Math and Attitudes](https://link.springer.com/article/10.1007/s13394-023-00468-8)
- Population: Secondary and high school students (ages 12-17)
- Approach: "Instructional methods offering mathematical practice with information about nature of mathematical inquiry and socio-historical aspects"
- Finding: Positive transformative effects on attitudes toward mathematics

**4. Competence development** (MEDIUM confidence)
- Source: [Research cited](https://online.nsu.edu/degrees/education/masters-urban/mathematics/inquiry-based-learning-math-classroom/)
- Finding: "Inquiry-based learning is effective way to support building competences"
- Outcomes: "Prepare young people who can create, innovate, collaborate, be critical, explore, communicate and make thoughtful decisions"

**Limitations and critiques:**

**1. Causal evidence concerns** (MEDIUM confidence)
- Source: [Multiple sources note](https://www.thescienceofmath.com/misconceptions-inquiry-based-versus-explicit-instruction)
- Critique: "Claims about benefits of inquiry-based instruction are not supported by rigorous experimental studies capable of supporting such causal claims"
- Issue: Much research is correlational or quasi-experimental

**2. Implementation variability** (HIGH confidence)
- Source: General finding across multiple sources
- Problem: "Inquiry-based learning" means different things to different educators
- Range: From minimal guidance (pure discovery) to heavily scaffolded exploration
- Implication: Research findings may not be comparing equivalent implementations

**3. The false dichotomy** (HIGH confidence)
- Source: [Edutopia](https://www.edutopia.org/article/direct-instruction-inquiry-math-classes/), [Science of Math](https://www.thescienceofmath.com/misconceptions-inquiry-based-versus-explicit-instruction)
- Finding: "Debate that pits inquiry-based learning against explicit instruction is a false dichotomy"
- Reality: "Both are needed; dividing them is ultimately harmful to educators and students"
- Best practice: Strategic integration based on content and learning goals

### When Inquiry-Based Instruction Works Best

**Optimal conditions identified in research:**

**1. Later grades with stronger foundation** (MEDIUM confidence)
- Source: [Fordham Institute](https://fordhaminstitute.org/national/commentary/when-choose-inquiry-based-learning-over-direct-instruction-stem)
- Pattern: "Evidence suggesting students learn better with inquiry in later grades"
- Rationale: Requires sufficient prior knowledge to engage productively
- Application: High school (grades 9-12) is appropriate for inquiry approaches

**2. Discoverable content** (HIGH confidence)
- Source: [Multiple sources](https://www.mathcoachscorner.com/2015/09/direct-instruction-do-we-need-it/)
- Rule: "If mathematicians discovered it, students can discover it"
- Examples: Function behavior, geometric relationships, pattern generalization
- Contrast: Conventions and vocabulary require direct instruction

**3. With explicit scaffolding** (HIGH confidence)
- Source: [Balance framework](https://blog.booknook.com/balancing-explicit-and-inquiry-based-learning-math-intervention)
- Finding: Pure discovery (minimal guidance) less effective than guided inquiry
- Effective model: Structured exploration with teacher facilitation
- Components: Clear problem, sufficient time, strategic questioning, consolidation phase

**4. Combined with explicit instruction** (HIGH confidence)
- Source: [Edutopia](https://www.edutopia.org/article/direct-instruction-inquiry-math-classes/)
- Pattern: Inquiry (20-30 min) → Discussion → Explicit instruction → Practice
- Rationale: "Inquiry builds understanding; explicit instruction formalizes and extends"
- Neither alone is sufficient

### Inquiry-Based Instruction Framework

**Structure from research:**

**Phase 1: Problem Posing**
- Present authentic, engaging mathematical situation
- Open-ended or multiple solution paths
- Appropriately challenging (not too easy, not impossible)
- Connected to students' experiences where possible

**Phase 2: Student Investigation**
- Individual or small group work
- Access to tools and resources
- Teacher as facilitator, not director
- Questions to extend thinking, not lead to answers

**Phase 3: Sharing and Discussion**
- Multiple solution strategies presented
- Student-to-student interaction
- Comparison of approaches
- Challenge and defend reasoning

**Phase 4: Consolidation**
- Connect informal exploration to formal mathematics
- Introduce precise vocabulary
- Formalize procedures or concepts discovered
- Make connections to broader mathematical ideas

**Phase 5: Application**
- Apply newly constructed understanding
- Transfer to new contexts
- Practice with variations

**Source:** Composite from [Inquiry Maths](https://www.inquirymaths.com/), [Educational Designer](https://www.educationaldesigner.org/ed/volume3/issue9/article30/), [TEACH Magazine](https://teachmag.com/using-inquiry-based-learning-teach-math/)

### Actionable Decision Rules

**USE INQUIRY-BASED APPROACH WHEN:**
- Content is discoverable (patterns, relationships, properties)
- Students have prerequisite knowledge
- Goal is conceptual understanding or problem-solving development
- Time allows for exploration (minimum 45-60 min lesson)
- High school level (grades 9-12) with adequate foundation

**AVOID PURE INQUIRY (use guided inquiry instead) WHEN:**
- Students lack prerequisite knowledge
- Content is conventional (notation, terminology)
- Time is limited
- Goal is skill consolidation rather than new learning

**ALWAYS COMBINE WITH:**
- Explicit scaffolding and strategic questioning
- Consolidation phase with formalization
- Follow-up explicit instruction to establish common language
- Structured practice to build fluency

**AUTOMATION IMPLICATIONS:**
```
IF content_type == "discoverable_concept" AND grade_level >= 9 AND time_available >= 45:
    lesson_structure = "inquiry_based"
    phases = ["problem_pose", "investigate", "discuss", "consolidate", "apply"]
    teacher_role = "facilitator"
    scaffolding = "probing_questions" (not "telling")

ELSE IF content_type == "convention" OR prerequisite_knowledge == "insufficient":
    lesson_structure = "explicit_instruction"
    phases = ["explain", "model", "guided_practice", "independent_practice"]

ELSE:
    lesson_structure = "hybrid"
    phases = ["brief_inquiry", "discuss", "explicit_instruction", "practice"]
```

## 6. Lesson Structures for Different Content Types

### Overview: Content-Responsive Design (HIGH confidence)

**Core principle:** Lesson structure should match content type, not follow single template for all mathematics

**Three primary content categories:**
1. **Procedures** - Step-by-step algorithms (polynomial multiplication, solving equations)
2. **Concepts** - Mathematical ideas and relationships (function behavior, similarity, probability)
3. **Problem-solving** - Application of knowledge to novel situations

**Source convergence:** NAEP 2026 Framework, NCTM Effective Teaching Practices, multiple research studies

### Structure 1: Launch-Explore-Summarize (for concepts and problem-solving)

**Source:** [Connected Mathematics Project](https://connectedmath.msu.edu/classroom/getting-organized/lesson.aspx), [Multiple implementations](https://www.drandrewgoodman.com/instructional-procedures-launchexploresummarize)

**When to use:**
- Introducing new conceptual content
- Developing problem-solving skills
- Content that is discoverable through exploration
- High school level with adequate prerequisites

**LAUNCH Phase (5-10 minutes)**

**Purpose:** Set stage for exploration without giving away solution
- Introduce problem context
- Activate prior knowledge
- Ensure understanding of WHAT is being asked (not HOW to solve)
- Engagement and clarity focus

**Teacher actions:**
- Present problem or mathematical situation
- Ask clarifying questions to ensure comprehension
- Make connections to previous learning
- Set expectations for exploration phase

**Student actions:**
- Make sense of problem context
- Ask clarifying questions
- Consider what they already know
- Prepare to explore

**EXPLORE Phase (15-25 minutes)**

**Purpose:** Students actively engage with mathematical problem
- Student thinking, collaboration, multiple strategies
- Teachers facilitate, observe, question

**Teacher actions:**
- Circulate and monitor student work
- Ask strategic questions (probing, not leading)
- Note different solution strategies for discussion
- Identify misconceptions to address
- Resist urge to tell or demonstrate

**Student actions:**
- Work individually or in small groups
- Try multiple approaches
- Use tools and representations
- Explain thinking to peers
- Revise strategies based on feedback

**SUMMARIZE Phase (10-15 minutes)**

**Purpose:** Share strategies, make connections, consolidate learning
- Mathematical communication and comparison
- Teacher facilitates to ensure key concepts emerge

**Teacher actions:**
- Select students to share (variety of approaches)
- Sequence presentations strategically
- Ask comparison questions
- Highlight key mathematical ideas
- Formalize concepts and vocabulary
- Make connections to broader mathematics

**Student actions:**
- Present solution strategies
- Compare different approaches
- Question peers' reasoning
- Revise understanding
- Record formalized concepts

**Time allocations:**
- Launch: 5-10 min (15-20% of lesson)
- Explore: 15-25 min (40-50% of lesson)
- Summarize: 10-15 min (30-35% of lesson)
- Total: 45-60 min lesson

**Example application:**
- **Topic:** Introduction to exponential functions
- **Launch:** "A rumor spreads: 1 person tells 2 people, each tells 2 more. How many know after 5 rounds?"
- **Explore:** Students create tables, graphs, equations; notice doubling pattern
- **Summarize:** Compare representations, formalize exponential function concept, introduce notation f(x) = 2^x

### Structure 2: Concrete-Representational-Abstract (for building new procedures)

**Source:** [Research base](https://thirdspacelearning.com/us/blog/concrete-representational-abstract-math-cpa/), [PATTAN](https://www.pattan.net/getmedia/9059e5f0-7edc-4391-8c8e-ebaf8c3c95d6/CRA_Methods0117), [Recent studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC11660403/)

**When to use:**
- Teaching new procedures
- Building conceptual foundation for algorithms
- Students need concrete understanding before symbolic work
- Particularly effective for diverse learners

**CONCRETE Phase (Lesson 1, 30-40 min)**

**Purpose:** Physical manipulation builds understanding
- Use manipulatives to model mathematical relationships
- Hands-on exploration precedes symbolic representation

**Materials:** Algebra tiles, fraction bars, geometric models, base-10 blocks

**Teacher actions:**
- Model procedure with physical objects
- Think aloud while manipulating
- Connect actions to mathematical meaning
- Guide students in parallel manipulation

**Student actions:**
- Manipulate concrete objects to solve problems
- Explain reasoning using physical models
- Make connections between actions and mathematical ideas
- Practice multiple examples with manipulatives

**Example:** Solving 2x + 3 = 7 using algebra tiles
- Use tiles to represent equation
- Physically remove 3 from both sides
- Divide remaining tiles to find x = 2

**REPRESENTATIONAL Phase (Lesson 2, 30-40 min)**

**Purpose:** Bridge from concrete to abstract
- Draw pictures/diagrams representing concrete objects
- Semi-abstract representation maintains conceptual connection

**Teacher actions:**
- Demonstrate drawing representations of concrete models
- Explicitly connect pictures to manipulative actions
- Gradually reduce scaffolding
- Introduce some symbolic notation alongside pictures

**Student actions:**
- Draw diagrams to solve problems
- Explain how drawings represent mathematical relationships
- Connect representations to prior concrete experience
- Begin transitioning to symbols

**Example:** Solving 2x + 3 = 7 using drawings
- Draw rectangles for x-tiles, small squares for unit tiles
- Show removal of 3 squares from both sides
- Illustrate division to find x

**ABSTRACT Phase (Lesson 3+, 30-40 min)**

**Purpose:** Formal symbolic mathematics
- Numbers and symbols only
- Efficient standard algorithms
- Only after conceptual foundation established

**Teacher actions:**
- Model symbolic procedure
- Explicitly connect to prior concrete and representational work
- Emphasize efficiency of symbolic approach
- Return to earlier phases if students struggle

**Student actions:**
- Use standard symbolic algorithms
- Explain why procedure works (referencing concepts)
- Practice with varied problems
- Self-correct using conceptual understanding

**Example:** Solving 2x + 3 = 7 symbolically
```
2x + 3 = 7
2x + 3 - 3 = 7 - 3  (subtract 3 from both sides)
2x = 4
2x/2 = 4/2  (divide both sides by 2)
x = 2
```

**CRA SEQUENCE VARIATIONS:**

**Fast-paced CRA** (single lesson, 60 min):
- Concrete: 15 min
- Representational: 15 min
- Abstract: 20 min
- Practice: 10 min

**Extended CRA** (multiple lessons):
- Concrete: 1-2 full lessons
- Representational: 1-2 full lessons
- Abstract: 2-3 full lessons with practice
- Return to earlier phases as needed

### Structure 3: Worked Example → Faded Example → Independent Practice (for procedures with novice learners)

**Source:** [Cognitive Load Theory research](https://www.tandfonline.com/doi/full/10.1080/01443410.2023.2273762), [Effectiveness studies](https://iris.peabody.vanderbilt.edu/module/math/cresource/q2/p08/)

**When to use:**
- Teaching procedures to novice learners
- Building initial procedural fluency
- Reducing cognitive load during skill acquisition
- **WARNING:** Effectiveness decreases with expertise (expertise reversal effect)

**Phase 1: Worked Example (10-15 min)**

**Purpose:** Demonstrate complete procedure with explanation
- Show step-by-step process
- Explain reasoning at each step
- Reduce cognitive load for novices

**Teacher actions:**
- Solve complete example while thinking aloud
- Highlight decision points
- Connect steps to underlying concepts
- Use consistent format and language

**Student actions:**
- Observe demonstration
- Take notes
- Ask clarifying questions
- Identify key steps

**Cognitive Load Theory principle:** Studying worked examples reduces load compared to problem-solving for novices

**Phase 2: Faded Worked Example (15-20 min)**

**Purpose:** Gradual transition to student work
- Provide partial solutions, students complete
- Scaffold decreases across examples

**Fading pattern:**
Example 1: Teacher completes steps 1-4, students complete steps 5-6
Example 2: Teacher completes steps 1-3, students complete steps 4-6
Example 3: Teacher completes steps 1-2, students complete steps 3-6
Example 4: Teacher completes step 1, students complete steps 2-6

**Teacher actions:**
- Provide partially completed examples
- Scaffold decreases systematically
- Monitor student completion
- Provide feedback on errors

**Student actions:**
- Complete partially worked examples
- Explain reasoning for their steps
- Compare with peers
- Self-check using worked example format

**Phase 3: Independent Practice (15-20 min)**

**Purpose:** Build fluency and consolidate learning
- Varied problem types
- Decreasing scaffolding
- Monitor for mastery

**Teacher actions:**
- Assign varied practice problems
- Circulate and provide feedback
- Note common errors for reteaching
- Assess readiness for application

**Student actions:**
- Solve problems independently
- Self-check work
- Seek help when stuck
- Practice until fluent

**IMPORTANT CAVEAT - Expertise Reversal Effect:**

**Source:** [Research on expertise reversal](https://link.springer.com/article/10.1007/s11251-009-9102-0)

**Finding:** "Instructional techniques highly effective for novices can lose effectiveness and sometimes produce negative consequences for experienced learners"

**Implication:** As students gain expertise, DECREASE worked examples and INCREASE problem-solving

**Progression over time:**
- Novice: Heavy worked example use
- Developing: Faded examples, some independent problem-solving
- Proficient: Minimal worked examples, mostly problem-solving
- Expert: NO worked examples (they become redundant and waste time)

**Automation decision:**
```
IF learner_expertise == "novice" AND content_type == "procedure":
    use_worked_examples = True
    fading_rate = "gradual"  # Many scaffolded examples

ELIF learner_expertise == "developing":
    use_worked_examples = True
    fading_rate = "moderate"  # Some scaffolding

ELIF learner_expertise == "proficient":
    use_worked_examples = False
    provide_independent_practice = True

ELSE:  # expert
    use_worked_examples = False  # Redundant and harmful
    provide_challenging_problems = True
```

### Structure 4: 5 Practices for Productive Discussion (for all content types)

**Source:** [NCTM: 5 Practices](https://www.nctm.org/Store/Products/5-Practices-for-Orchestrating-Productive-Mathematics-Discussions,-2nd-edition-(Download)/), [High School Implementation](https://www.amazon.com/Five-Practices-Practice-High-School/dp/1544321236)

**Authors:** Margaret (Peg) Smith & Mary Kay Stein

**When to use:**
- When lesson includes student problem-solving
- To orchestrate meaningful mathematical discussions
- Applicable to any content type where students produce work to share
- High school specific implementation guidance available

**The Five Practices:**

**1. ANTICIPATING (Before lesson)**

**Purpose:** Predict student solutions and prepare responses
- Identify likely solution strategies (correct and incorrect)
- Anticipate misconceptions
- Prepare questions to advance thinking

**Teacher actions:**
- Solve problem multiple ways
- Consider student prior knowledge and common approaches
- List likely correct strategies, likely errors, likely misconceptions
- Prepare advancing questions for each anticipated response

**Why essential:** Enables strategic in-the-moment decisions during monitoring and selecting

**2. MONITORING (During student work)**

**Purpose:** Observe what students actually do
- Note which strategies students use
- Identify errors and misconceptions
- Gather evidence of thinking

**Teacher actions:**
- Circulate strategically (different groups/students)
- Observe without interrupting productive struggle
- Take notes on solution strategies observed
- Ask probing questions to understand thinking
- Compare actual student work to anticipated solutions

**Tools:** Monitoring sheet with anticipated solutions, checkmarks for each observed

**3. SELECTING (During student work)**

**Purpose:** Choose which student work to share publicly
- Select variety of approaches
- Include correct and instructive errors
- Consider mathematical goals

**Teacher actions:**
- Identify specific students to present
- Choose work that advances mathematical agenda
- Include multiple approaches when valuable
- Sometimes select unexpected or creative solutions
- Consider which errors would be instructive to discuss

**Criteria:**
- Variety of strategies (show mathematical flexibility)
- Correct solutions using different methods
- Common errors worth discussing
- Elegant or efficient approaches
- Connections to mathematical goals

**4. SEQUENCING (During student work / transition to discussion)**

**Purpose:** Order presentations for maximum learning
- Strategic sequence builds understanding
- Simple → complex, concrete → abstract, or error → correct

**Teacher actions:**
- Determine presentation order
- Consider mathematical storyline (what order builds understanding?)
- Sometimes start with familiar approaches, build to sophisticated
- Sometimes start with error to create need for correct approach
- Plan transitions between presentations

**Common sequences:**
- Concrete → Pictorial → Abstract
- Inefficient → Efficient (to highlight why standard algorithms help)
- Incorrect → Correct (to build from common errors)
- Multiple correct (to show mathematical flexibility)

**5. CONNECTING (During discussion)**

**Purpose:** Make mathematical relationships explicit
- Link different solution strategies
- Highlight key mathematical ideas
- Build coherent understanding

**Teacher actions:**
- Ask comparison questions: "How is this approach similar/different from previous?"
- Highlight connections: "This strategy uses the same idea we saw in..."
- Make mathematical ideas explicit: "What both approaches show is..."
- Connect to formal mathematics: "Your method is actually using the distributive property"
- Synthesize learning: "What we've discovered today is..."

**Student actions:**
- Present solution strategies
- Explain reasoning
- Compare approaches
- Question peers
- Identify connections

**IMPLEMENTATION TIMELINE FOR LESSON:**

**Before class (ANTICIPATING):** 15-30 min planning
- Solve problem multiple ways
- List anticipated solutions
- Prepare questions

**During class:**
- Launch problem: 5-10 min
- Student work (MONITORING, SELECTING, SEQUENCING): 15-25 min
- Discussion (CONNECTING): 15-20 min
- Consolidation: 5-10 min

**AUTOMATION IMPLICATIONS:**

The 5 Practices require human judgment but can be partially automated:

**Anticipating:** Can be automated
- AI generates multiple solution strategies
- Predicts common errors based on misconception research
- Prepares question stems for each anticipated approach

**Monitoring:** Cannot be fully automated (requires real-time observation)
- Can provide monitoring sheet template
- Can suggest what to look for

**Selecting:** Requires human judgment
- Can provide selection criteria
- Can suggest "aim to include 3-4 different strategies"

**Sequencing:** Can provide guidance
- Suggest sequence patterns (concrete→abstract, simple→complex)
- Provide decision framework

**Connecting:** Can prepare questions
- Generate comparison question stems
- Identify mathematical connections between anticipated strategies
- Prepare synthesis statements

### Content-Type Decision Matrix

**DECISION FRAMEWORK FOR LESSON STRUCTURE:**

| Content Type | Primary Structure | Duration | Key Features |
|--------------|------------------|----------|--------------|
| **New Concept (Discoverable)** | Launch-Explore-Summarize | 45-60 min | Problem-based, multiple strategies, consolidation |
| **New Procedure** | CRA Sequence | 2-4 lessons | Manipulatives → drawings → symbols, conceptual foundation |
| **Procedure (Novice Learners)** | Worked Example → Faded → Practice | 45-60 min | Cognitive load reduction, gradual release |
| **Procedure (Experienced Learners)** | Problem-Solving + Discussion | 45-60 min | Skip worked examples (expertise reversal) |
| **Problem-Solving Skills** | Teaching Through Problem-Solving | 45-60 min | Novel problem → discussion → formalization |
| **Application/Practice** | Teaching For Problem-Solving | 30-45 min | Brief review → varied practice → reflection |
| **Conventions/Vocabulary** | Direct Instruction + Application | 20-30 min | Explicit explanation → immediate use |

**ALL structures can incorporate 5 Practices** when discussion phase is included

**Automation pseudocode:**
```
def select_lesson_structure(content_type, learner_expertise, learning_phase):

    if content_type == "discoverable_concept":
        return "launch_explore_summarize"

    elif content_type == "procedure" and learning_phase == "introduction":
        return "CRA_sequence"  # 2-4 lessons

    elif content_type == "procedure" and learner_expertise == "novice":
        return "worked_example_to_practice"

    elif content_type == "procedure" and learner_expertise in ["proficient", "expert"]:
        return "problem_solving_discussion"  # Skip worked examples

    elif content_type == "problem_solving":
        return "teaching_through_problem_solving"

    elif content_type == "application":
        return "teaching_for_problem_solving"

    elif content_type == "convention_or_vocabulary":
        return "direct_instruction_with_application"

    else:
        return "hybrid_inquiry_explicit"  # Default blended model

def add_discussion_orchestration(lesson_structure):
    if includes_student_work(lesson_structure):
        incorporate_5_practices(lesson_structure)
    return lesson_structure
```

## 7. NCTM's 8 Effective Mathematics Teaching Practices

**Source:** [NCTM Principles to Actions](https://www.nctm.org/PtA/), [Effective Teaching Practices](https://www.nctm.org/Conferences-and-Professional-Development/Principles-to-Actions-Toolkit/Resources/7-EffectiveMathematicsTeachingPractices/)

**Confidence:** HIGH (Official NCTM position, research-based framework)

### The Eight Practices

**1. Establish mathematics goals to focus learning**
- Clear, explicit learning targets
- Goals focus on mathematical understanding, not just task completion
- Shared with students in accessible language

**2. Implement tasks that promote reasoning and problem-solving**
- High-cognitive-demand tasks
- Multiple entry points and solution strategies
- Require explanation and justification

**3. Use and connect mathematical representations**
- Multiple representations (concrete, visual, symbolic, contextual, verbal)
- Explicit connections between representations
- Students choose appropriate representations

**4. Facilitate meaningful mathematical discourse**
- Student-to-student interaction
- Mathematical argumentation
- Teacher facilitates, doesn't dominate

**5. Pose purposeful questions**
- Advance reasoning, not just check answers
- Probing questions reveal thinking
- Questions assess and advance learning

**6. Build procedural fluency from conceptual understanding**
- **This is the practice most relevant to our research question**
- Procedures develop FROM understanding, not before
- Explicit connections between concepts and procedures
- Multiple solution strategies precede standard algorithms

**7. Support productive struggle in learning mathematics**
- Struggle is expected and valued
- Teacher provides scaffolding, not solutions
- Time for sense-making
- Differentiate between productive and unproductive struggle

**8. Elicit and use evidence of student thinking**
- Formative assessment throughout lesson
- Instruction adjusted based on evidence
- Student thinking informs next instructional moves

### Implications for Lesson Design

**These practices should be present in EVERY lesson, regardless of structure**

Can be checklist for automated lesson quality:
- [ ] Clear mathematics goal established
- [ ] Task promotes reasoning (not just procedure execution)
- [ ] Multiple representations used and connected
- [ ] Student discussion structured into lesson
- [ ] Purposeful questions planned (not just "Does everyone understand?")
- [ ] Procedural work connected to conceptual understanding
- [ ] Productive struggle time allocated
- [ ] Formative assessment checkpoints included

## Key Findings Summary for Automation

### 1. Content Classification is Critical

**Mathematics content falls into categories requiring different instructional approaches:**

| Category | Examples | Optimal Approach | Rationale |
|----------|----------|------------------|-----------|
| Discovered Concepts | Function behavior, geometric relationships, Pythagorean theorem | Exploration → Discussion → Formalization | Students can/should discover what mathematicians discovered |
| Decided Conventions | Notation (f(x)), terminology (domain, perpendicular), symbolic representations | Direct Instruction → Immediate Application | Cannot be discovered; must be told |
| Procedures (New) | Solving equations, factoring, polynomial operations | CRA Sequence (Concrete → Representational → Abstract) | Build conceptual foundation before symbolic work |
| Procedures (Practice) | Fluency building with known algorithms | Worked Examples (novices) or Problem-Solving (experts) | Expertise level determines approach |
| Problem-Solving | Applications, non-routine problems, novel situations | Teaching Through Problem-Solving | Learn mathematics BY solving problems |

**Automation requirement:** System must classify learning objectives into these categories to select appropriate instructional sequence.

### 2. Prior Knowledge/Expertise Level Matters (Expertise Reversal Effect)

**Same content, different instruction based on learner expertise:**

| Expertise Level | Worked Examples | Scaffolding | Primary Activity |
|-----------------|----------------|-------------|------------------|
| Novice | Heavy use (reduces cognitive load) | Extensive | Studying examples, guided practice |
| Developing | Faded examples | Moderate | Mix of examples and problem-solving |
| Proficient | Minimal | Light, just-in-time | Independent problem-solving |
| Expert | None (counterproductive) | None | Novel, challenging problems |

**Research finding:** Instructional techniques effective for novices can produce NEGATIVE learning outcomes for experts.

**Automation requirement:** System must assess prior knowledge and adjust scaffolding accordingly.

### 3. Lesson Structure Templates Matched to Content

**Five evidence-based structures identified:**

**A. Launch-Explore-Summarize** (45-60 min)
- Use for: Discoverable concepts, problem-solving
- Structure: Launch (5-10 min) → Explore (15-25 min) → Summarize (10-15 min)
- Key: Students grapple with problem BEFORE instruction

**B. CRA Sequence** (2-4 lessons)
- Use for: New procedures requiring conceptual foundation
- Structure: Concrete (manipulatives) → Representational (drawings) → Abstract (symbols)
- Key: Physical and visual understanding precede symbolic work

**C. Worked Example → Faded → Practice** (45-60 min)
- Use for: Procedures with novice learners only
- Structure: Full example → Partial examples → Independent practice
- Key: Gradually decrease scaffolding; skip for experienced learners

**D. Teaching Through Problem-Solving** (45-60 min)
- Use for: Learning new mathematics through problem contexts
- Structure: Problem → Exploration → Discussion → Formalization → Application
- Key: Problem comes BEFORE concept introduction

**E. Direct Instruction + Application** (20-30 min)
- Use for: Conventions, vocabulary, brief skill instruction
- Structure: Explain → Model → Immediate application
- Key: Used sparingly, only for content that cannot be discovered

**Automation requirement:** Map learning objectives → content type → appropriate structure template.

### 4. Conceptual-Procedural Relationship is Iterative

**NCTM Position: "Conceptual understanding must precede and coincide with procedural instruction"**

**Pattern:**
1. Build conceptual foundation (CRA: Concrete phase, exploration activities)
2. Connect concepts to procedures explicitly (CRA: Representational phase, "This is why the algorithm works")
3. Practice procedures with conceptual connections (CRA: Abstract phase, "When error occurs, return to concept")
4. Procedural practice deepens conceptual understanding (Application phase, varied problems reveal deeper patterns)

**NOT: Concept → Procedure (strictly sequential)**
**YES: Concept ⇄ Procedure (iterative, mutually reinforcing)**

**Automation requirement:**
- Every procedural lesson must include conceptual foundation
- Practice problems should vary to deepen concepts
- Error remediation returns to conceptual models, not more procedural drill

### 5. Productive Struggle Must Be Calibrated

**Research identifies sweet spot between:**
- Too little challenge → No meaningful learning
- Productive struggle → Optimal learning (15-30 min exploration)
- Too much struggle → Frustration, giving up

**Four struggle types + teacher response continuum:**

| Struggle Type | Student Issue | Teacher Response |
|---------------|---------------|------------------|
| Get Started | Can't identify entry point | Probing questions: "What do you know?" "What are you trying to find?" |
| Carry Out Process | Knows approach, execution difficulty | Directed guidance: "Try this tool" "What if you organized the data?" |
| Give Explanation | Can solve, can't articulate | Probing questions: "Why did you choose that?" "What pattern do you see?" |
| Express Misconception | Reveals flawed understanding | Affordance: Provide counterexample, tool, or representation to challenge thinking |

**Time boundaries from research:**
- Launch: 5-10 min (clarify problem, don't solve)
- Explore: 15-25 min (productive struggle window)
- If still stuck after 25 min → Move to discussion (struggle window closed)

**Automation requirement:**
- Allocate 15-30 min exploration time for problem-based lessons
- Provide question stems for different struggle types
- Include transition to discussion even if students haven't fully solved (partial solutions valued)

### 6. Discussion Orchestration Follows Structured Protocol

**5 Practices Model (Smith & Stein):**
1. **Anticipate** (pre-lesson): Predict student strategies, prepare questions
2. **Monitor** (during work): Observe actual student approaches
3. **Select** (during work): Choose which work to share publicly
4. **Sequence** (transition): Order presentations strategically
5. **Connect** (during discussion): Make mathematical relationships explicit

**Can be partially automated:**
- Anticipate: AI generates multiple solution strategies, common errors, questions
- Monitor: Provide observation template (what to look for)
- Select: Suggest criteria (variety of approaches, instructive errors, elegant solutions)
- Sequence: Recommend patterns (concrete→abstract, simple→complex, error→correct)
- Connect: Prepare comparison question stems, connection statements

**Automation requirement:**
- Generate anticipated solutions for problem-based tasks
- Provide monitoring and selection guidance
- Prepare discussion questions that connect different strategies

### 7. Cognitive Load Principles Apply

**Key findings from Cognitive Load Theory research:**

1. **Worked examples reduce load for novices** (use them)
2. **Worked examples are redundant for experts** (skip them - expertise reversal)
3. **Modality effect**: Audio + visual better than text + visual
4. **Faded examples**: Gradually transition from observation to practice
5. **Prior knowledge is everything**: Same problem is "difficult" for novice, "easy" for expert

**Automation implications:**
- Adjust scaffolding based on prior knowledge assessment
- Use worked examples strategically (novices only)
- Provide visual representations + verbal explanations
- Implement fading pattern (full example → partial → independent)

### 8. Avoid Traditional Gradual Release as Default

**Research critique of "I Do, We Do, You Do":**
- Not designed for mathematics learning
- Prevents authentic problem-solving
- Creates procedural dependency
- Students follow steps without understanding

**When GRR is acceptable:**
- Teaching conventions (after exploration has occurred)
- Formalizing after inquiry phase
- Explicit instruction phase within blended model

**When GRR is problematic:**
- As primary/default lesson structure
- For discoverable content
- When used to bypass productive struggle

**Automation requirement:**
- Default to Launch-Explore-Summarize or Teaching Through Problem-Solving
- Use direct instruction only for conventions or formalization phases
- Reserve "I Do, We Do, You Do" for specific, limited contexts

## Actionable Decision Framework for Automated Lesson Design

### Step 1: Classify the Content

```python
def classify_content(learning_objective):
    """
    Classify content type to determine appropriate instructional approach
    """
    keywords_discovered_concepts = [
        "understand", "explore", "discover", "relationship", "pattern",
        "why", "investigate", "compare", "analyze", "generalize"
    ]

    keywords_conventions = [
        "notation", "symbol", "vocabulary", "terminology", "definition",
        "represent", "name", "label"
    ]

    keywords_procedures = [
        "solve", "calculate", "compute", "find", "determine", "simplify",
        "factor", "graph", "evaluate"
    ]

    keywords_problem_solving = [
        "apply", "use", "create", "model", "design", "prove",
        "justify", "explain", "construct"
    ]

    # Classification logic (simplified)
    if any(kw in learning_objective.lower() for kw in keywords_conventions):
        return "convention"
    elif any(kw in learning_objective.lower() for kw in keywords_discovered_concepts):
        return "discoverable_concept"
    elif any(kw in learning_objective.lower() for kw in keywords_procedures):
        return "procedure"
    elif any(kw in learning_objective.lower() for kw in keywords_problem_solving):
        return "problem_solving"
    else:
        return "hybrid"  # Needs human review
```

### Step 2: Assess Prior Knowledge Level

```python
def assess_expertise(student_history, prerequisite_skills):
    """
    Determine expertise level for this specific content
    Returns: "novice", "developing", "proficient", or "expert"
    """
    # Check prerequisite mastery
    prerequisites_met = check_prerequisites(student_history, prerequisite_skills)

    # Check prior exposure to this specific content
    prior_exposure = check_prior_exposure(student_history, current_topic)

    if not prerequisites_met:
        return "novice"  # Lacks foundation
    elif prerequisites_met and not prior_exposure:
        return "developing"  # Ready to learn
    elif prior_exposure and performance == "partial":
        return "proficient"  # Has some mastery
    elif prior_exposure and performance == "high":
        return "expert"  # Has strong mastery
```

### Step 3: Select Lesson Structure

```python
def select_lesson_structure(content_type, expertise_level, time_available):
    """
    Match content and expertise to appropriate lesson structure
    """
    structure_map = {
        ("discoverable_concept", any): {
            "structure": "launch_explore_summarize",
            "duration": 50,
            "phases": {
                "launch": 10,
                "explore": 25,
                "summarize": 15
            }
        },
        ("procedure", "novice"): {
            "structure": "CRA_sequence",
            "duration": 150,  # 2-3 lessons
            "phases": {
                "concrete": 50,
                "representational": 50,
                "abstract": 50
            }
        },
        ("procedure", "developing"): {
            "structure": "worked_example_faded_practice",
            "duration": 50,
            "phases": {
                "worked_example": 15,
                "faded_examples": 20,
                "independent_practice": 15
            }
        },
        ("procedure", "proficient"): {
            "structure": "problem_solving_with_discussion",
            "duration": 50,
            "phases": {
                "problem": 25,
                "discussion": 15,
                "practice": 10
            }
        },
        ("convention", any): {
            "structure": "direct_instruction_application",
            "duration": 25,
            "phases": {
                "explain": 10,
                "model": 5,
                "apply": 10
            }
        },
        ("problem_solving", any): {
            "structure": "teaching_through_problem_solving",
            "duration": 55,
            "phases": {
                "problem_pose": 10,
                "investigate": 25,
                "discuss": 15,
                "consolidate": 5
            }
        }
    }

    # Lookup structure
    key = (content_type, expertise_level)
    if key not in structure_map:
        key = (content_type, "any")  # Fallback to content-only match

    return structure_map.get(key, default_hybrid_structure())
```

### Step 4: Generate Lesson Components

```python
def generate_lesson(learning_objective, content_type, expertise_level, structure):
    """
    Generate lesson components based on selected structure
    """
    lesson = {
        "objective": learning_objective,
        "structure": structure["structure"],
        "duration": structure["duration"],
        "phases": []
    }

    # Launch-Explore-Summarize structure
    if structure["structure"] == "launch_explore_summarize":
        lesson["phases"] = [
            {
                "name": "Launch",
                "duration": 10,
                "teacher_actions": [
                    "Present problem context: [CONTEXT]",
                    "Activate prior knowledge: Ask 'What do you know about...?'",
                    "Ensure understanding of WHAT is asked (not HOW to solve)",
                    "Set expectations: 'You'll have 25 min to explore'"
                ],
                "student_actions": [
                    "Make sense of problem",
                    "Ask clarifying questions",
                    "Consider prior knowledge"
                ],
                "materials": ["Problem statement", "Context visuals"],
                "scaffolding": generate_launch_scaffolds(content_type)
            },
            {
                "name": "Explore",
                "duration": 25,
                "teacher_actions": [
                    "Circulate and monitor (use 5 Practices monitoring sheet)",
                    "Ask probing questions (not leading): 'What have you tried?' 'What patterns do you notice?'",
                    "Note different solution strategies for discussion",
                    "Identify 3-4 students to present (variety of approaches)"
                ],
                "student_actions": [
                    "Work individually or in pairs",
                    "Try multiple approaches",
                    "Use tools and representations",
                    "Explain thinking to partner"
                ],
                "materials": ["Graphing tools", "Manipulatives", "Graph paper"],
                "scaffolding": generate_exploration_scaffolds(expertise_level),
                "struggle_support": {
                    "get_started": "Clarify: 'What are you trying to find? What do you already know?'",
                    "carry_out": "Provide tool: 'Would a table help organize your thinking?'",
                    "explain": "Probe: 'Why did you choose that approach?'",
                    "misconception": "Challenge: 'What if you tried this case?'"
                }
            },
            {
                "name": "Summarize",
                "duration": 15,
                "teacher_actions": [
                    "Select and sequence student presentations (simple → complex)",
                    "Facilitate comparison: 'How is this similar/different from previous?'",
                    "Make connections explicit: 'What both methods show is...'",
                    "Formalize concept and vocabulary",
                    "Connect to broader mathematics"
                ],
                "student_actions": [
                    "Present solution strategies",
                    "Compare different approaches",
                    "Question peers' reasoning",
                    "Record formalized concepts"
                ],
                "materials": ["Presentation space", "Chart paper for synthesis"],
                "discussion_questions": generate_connecting_questions(content_type),
                "formalization": generate_formalization(learning_objective)
            }
        ]

    # CRA Sequence structure
    elif structure["structure"] == "CRA_sequence":
        lesson["phases"] = [
            {
                "name": "Concrete Phase",
                "duration": 50,
                "lesson_number": 1,
                "teacher_actions": [
                    "Model procedure with manipulatives",
                    "Think aloud while manipulating objects",
                    "Connect actions to mathematical meaning",
                    "Guide students in parallel manipulation"
                ],
                "student_actions": [
                    "Manipulate concrete objects to solve problems",
                    "Explain reasoning using physical models",
                    "Practice 5-7 examples with manipulatives"
                ],
                "materials": generate_concrete_materials(content_type),
                "conceptual_focus": "WHY the procedure works (physical model)"
            },
            {
                "name": "Representational Phase",
                "duration": 50,
                "lesson_number": 2,
                "teacher_actions": [
                    "Demonstrate drawing representations of concrete models",
                    "Explicitly connect pictures to manipulative actions from previous lesson",
                    "Introduce some symbolic notation alongside pictures"
                ],
                "student_actions": [
                    "Draw diagrams to solve problems",
                    "Explain how drawings represent mathematical relationships",
                    "Begin transitioning to symbols"
                ],
                "materials": ["Graph paper", "Colored pencils", "Diagram templates"],
                "conceptual_focus": "Bridge from physical to symbolic"
            },
            {
                "name": "Abstract Phase",
                "duration": 50,
                "lesson_number": 3,
                "teacher_actions": [
                    "Model symbolic procedure",
                    "Explicitly connect to prior concrete and representational work",
                    "Emphasize efficiency of symbolic approach",
                    "Return to earlier phases if students struggle"
                ],
                "student_actions": [
                    "Use standard symbolic algorithms",
                    "Explain why procedure works (referencing concepts)",
                    "Practice with varied problems",
                    "Self-correct using conceptual understanding"
                ],
                "materials": ["Practice problems (varied)"],
                "conceptual_focus": "Symbolic efficiency grounded in understanding"
            }
        ]

    # Worked Example structure (novices only)
    elif structure["structure"] == "worked_example_faded_practice":
        if expertise_level in ["proficient", "expert"]:
            # Expertise reversal: skip this structure
            return generate_problem_solving_lesson(learning_objective, content_type)

        lesson["phases"] = [
            {
                "name": "Worked Example",
                "duration": 15,
                "teacher_actions": [
                    "Solve complete example with think-aloud",
                    "Highlight decision points",
                    "Connect steps to underlying concepts",
                    "Use consistent format and language"
                ],
                "student_actions": [
                    "Observe demonstration",
                    "Take notes in structured format",
                    "Ask clarifying questions"
                ],
                "materials": ["Worked example template"],
                "examples": generate_worked_examples(content_type, count=2)
            },
            {
                "name": "Faded Examples",
                "duration": 20,
                "teacher_actions": [
                    "Provide partially completed examples",
                    "Scaffold decreases systematically across 4 examples",
                    "Monitor student completion",
                    "Provide immediate feedback"
                ],
                "student_actions": [
                    "Complete partially worked examples",
                    "Explain reasoning for their steps",
                    "Self-check using worked example format"
                ],
                "materials": generate_faded_examples(content_type, fading_pattern="gradual")
            },
            {
                "name": "Independent Practice",
                "duration": 15,
                "teacher_actions": [
                    "Assign varied practice problems",
                    "Circulate and provide feedback",
                    "Note common errors for reteaching"
                ],
                "student_actions": [
                    "Solve problems independently",
                    "Self-check work",
                    "Seek help when stuck"
                ],
                "materials": generate_practice_problems(content_type, variety="high")
            }
        ]

    # Direct Instruction (conventions only)
    elif structure["structure"] == "direct_instruction_application":
        lesson["phases"] = [
            {
                "name": "Explain",
                "duration": 10,
                "teacher_actions": [
                    "Explicitly state the convention/vocabulary",
                    "Provide rationale: 'Mathematicians agreed to use this notation because...'",
                    "Show multiple examples of use"
                ],
                "student_actions": [
                    "Listen and take notes",
                    "Ask clarifying questions"
                ],
                "materials": ["Notation examples", "Visual reference sheet"]
            },
            {
                "name": "Model",
                "duration": 5,
                "teacher_actions": [
                    "Demonstrate using the convention in context",
                    "Show correct and incorrect usage"
                ],
                "student_actions": [
                    "Observe examples"
                ]
            },
            {
                "name": "Immediate Application",
                "duration": 10,
                "teacher_actions": [
                    "Provide practice opportunities",
                    "Check for correct usage"
                ],
                "student_actions": [
                    "Use convention in problems",
                    "Practice with feedback"
                ],
                "materials": generate_application_exercises(content_type)
            }
        ]

    # Add formative assessment checkpoints
    lesson["formative_assessments"] = generate_formative_assessments(
        learning_objective, structure["structure"]
    )

    # Add NCTM 8 Practices alignment
    lesson["nctm_practices"] = identify_nctm_practices(structure["structure"])

    return lesson
```

### Step 5: Quality Assurance Checks

```python
def validate_lesson_quality(lesson, content_type, expertise_level):
    """
    Check lesson against research-based quality criteria
    """
    quality_checks = {
        "conceptual_foundation": False,
        "productive_struggle_time": False,
        "multiple_representations": False,
        "student_discussion": False,
        "formative_assessment": False,
        "appropriate_scaffolding": False,
        "avoids_rote_memorization": False,
        "nctm_practices": 0
    }

    # Check conceptual foundation for procedures
    if content_type == "procedure":
        has_concrete_phase = any(p["name"] in ["Concrete Phase", "Exploration"]
                                 for p in lesson["phases"])
        quality_checks["conceptual_foundation"] = has_concrete_phase

    # Check productive struggle time allocation
    explore_time = sum(p.get("duration", 0) for p in lesson["phases"]
                      if "explore" in p["name"].lower() or "investigate" in p["name"].lower())
    quality_checks["productive_struggle_time"] = 15 <= explore_time <= 30

    # Check multiple representations
    materials = [item for phase in lesson["phases"] for item in phase.get("materials", [])]
    representation_types = ["visual", "concrete", "symbolic", "verbal", "contextual"]
    representations_present = sum(1 for r in representation_types
                                 if any(r in str(materials).lower()))
    quality_checks["multiple_representations"] = representations_present >= 2

    # Check student discussion included
    has_discussion = any("discuss" in p["name"].lower() or "summarize" in p["name"].lower()
                        for p in lesson["phases"])
    quality_checks["student_discussion"] = has_discussion

    # Check formative assessment
    quality_checks["formative_assessment"] = len(lesson.get("formative_assessments", [])) >= 2

    # Check scaffolding matches expertise
    if expertise_level == "novice":
        quality_checks["appropriate_scaffolding"] = lesson["structure"] in [
            "worked_example_faded_practice", "CRA_sequence"
        ]
    elif expertise_level in ["proficient", "expert"]:
        # Should NOT use worked examples (expertise reversal)
        quality_checks["appropriate_scaffolding"] = lesson["structure"] != "worked_example_faded_practice"

    # Check avoids rote memorization
    rote_indicators = ["memorize", "drill", "timed test", "speed"]
    lesson_text = str(lesson).lower()
    quality_checks["avoids_rote_memorization"] = not any(ind in lesson_text for ind in rote_indicators)

    # Count NCTM practices addressed
    quality_checks["nctm_practices"] = len(lesson.get("nctm_practices", []))

    # Overall quality score
    checks_passed = sum(1 for v in quality_checks.values() if v == True or (isinstance(v, int) and v > 0))
    quality_score = checks_passed / len(quality_checks)

    return {
        "quality_score": quality_score,
        "checks": quality_checks,
        "recommendations": generate_quality_recommendations(quality_checks)
    }

def generate_quality_recommendations(quality_checks):
    """
    Provide specific recommendations to improve lesson quality
    """
    recommendations = []

    if not quality_checks["conceptual_foundation"]:
        recommendations.append(
            "Add conceptual foundation phase. Use CRA sequence or exploration activity "
            "before introducing symbolic procedures."
        )

    if not quality_checks["productive_struggle_time"]:
        recommendations.append(
            "Allocate 15-30 minutes for student exploration/productive struggle. "
            "Research shows this is optimal window for sense-making."
        )

    if not quality_checks["multiple_representations"]:
        recommendations.append(
            "Include multiple representations (concrete, visual, symbolic, contextual). "
            "Explicitly connect representations to build deep understanding."
        )

    if not quality_checks["student_discussion"]:
        recommendations.append(
            "Add discussion phase where students share and compare strategies. "
            "Use 5 Practices model: anticipate, monitor, select, sequence, connect."
        )

    if quality_checks["nctm_practices"] < 5:
        recommendations.append(
            f"Only {quality_checks['nctm_practices']} of 8 NCTM Effective Teaching Practices "
            f"addressed. Consider adding: purposeful questioning, procedural fluency from concepts, "
            f"evidence of student thinking."
        )

    return recommendations
```

## Sources

### Primary Sources (HIGH Confidence)

**NCTM Official Positions:**
- [NCTM: Procedural Fluency in Mathematics](https://www.nctm.org/Standards-and-Positions/Position-Statements/Procedural-Fluency-in-Mathematics/) - Official position on conceptual-procedural relationship
- [NCTM: Principles to Actions - Effective Teaching Practices](https://www.nctm.org/PtA/) - 8 Effective Mathematics Teaching Practices framework
- [NCTM: Rethinking Gradual Release of Responsibility](https://www.nctm.org/Publications/MTMS-Blog/Blog/Rethinking-the-Gradual-Release-of-Responsibility-Model/) - Critique of "I Do, We Do, You Do"

**Research-Based Frameworks:**
- [Connected Mathematics Project: Launch-Explore-Summarize](https://connectedmath.msu.edu/classroom/getting-organized/lesson.aspx) - Structure for problem-centered lessons
- [NCTM: 5 Practices for Orchestrating Productive Discussions](https://www.nctm.org/Store/Products/5-Practices-for-Orchestrating-Productive-Mathematics-Discussions,-2nd-edition-(Download)/) - Discussion orchestration protocol (Smith & Stein)
- [IRIS Peabody: Evidence-Based Mathematics Practices](https://iris.peabody.vanderbilt.edu/module/math/cresource/q1/p03/) - Explicit instruction, visual representations, schema instruction, metacognitive strategies

**Cognitive Science Research:**
- [Cognitive Load Theory and Mathematics](https://www.tandfonline.com/doi/full/10.1080/01443410.2023.2273762) - Worked examples, expertise reversal effect
- [Expertise Reversal Effect](https://link.springer.com/article/10.1007/s11251-009-9102-0) - Springer article on expertise-based instructional design
- [Exploring Before Instruction](https://pubmed.ncbi.nlm.nih.gov/22849809/) - PubMed study: exploration prepares students to learn from instruction

**Productive Struggle Research:**
- [Springer: Productive Struggle in Middle School](https://link.springer.com/article/10.1007/s10857-014-9286-3) - Definition, types of struggle, teacher responses
- [AAAS: Productive Struggle as Learning Opportunity](https://aaas-arise.org/2022/11/09/productive-struggle-an-opportunity-for-in-depth-mathematics-learning/) - Eight effective teaching practices
- [Make Math Moments: Teaching Resilience 2026](https://makemathmoments.com/math-resilience-2026-strategies/) - Current guidance on productive vs. unproductive struggle

**Direct Instruction Research:**
- [PMC: Just How Effective is Direct Instruction?](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476697/) - 50+ years of research on Direct Instruction model
- [Edutopia: Direct Instruction and Inquiry in Math](https://www.edutopia.org/article/direct-instruction-inquiry-math-classes/) - Blended model guidance

### Secondary Sources (MEDIUM-HIGH Confidence)

**Teaching Through Problem-Solving:**
- [FHSU: Teaching Mathematics Through Problem Solving](https://fhsu.pressbooks.pub/ecumath/chapter/chapter-4-teaching-mathematics-through-problem-solving/) - Comparison of FOR vs. THROUGH vs. ABOUT
- [Lesson Research: Teaching Through Problem-Solving](https://lessonresearch.net/teaching-problem-solving/overview/) - Japanese Lesson Study approach
- [Frontiers: Using Lesson Study with Teaching Through Problem Solving](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2024.1331674/full) - 2024 research on implementation
- [Curriculum Journal: Problem Solving in Mathematics Curriculum](https://bera-journals.onlinelibrary.wiley.com/doi/10.1002/curj.213) - Scholarly analysis of teaching through vs. about problem-solving

**Conceptual Understanding Research:**
- [HMH: What Is Conceptual Understanding in Math?](https://www.hmhco.com/blog/what-is-conceptual-understanding-in-math) - Overview of research
- [IM Certified Blog: Developing Conceptual Understanding and Procedural Fluency](https://illustrativemathematics.blog/2019/04/29/developing-conceptual-understanding-and-procedural-fluency/) - Mutual reinforcement model
- [EdSurge: Concepts Matter More Than Process (2024)](https://www.edsurge.com/news/2024-06-05-when-teaching-students-math-concepts-matter-more-than-process) - Recent emphasis on conceptual priority
- [Minnesota STEM: Build Procedural Fluency FROM Conceptual Understanding](https://stemtc.scimathmn.org/build-procedural-fluency-conceptual-understanding) - Implementation guidance

**CRA Sequence Research:**
- [Third Space Learning: Concrete-Representational-Abstract](https://thirdspacelearning.com/us/blog/concrete-representational-abstract-math-cpa/) - Overview of CRA approach
- [PATTAN: CRA Instructional Methods](https://www.pattan.net/getmedia/9059e5f0-7edc-4391-8c8e-ebaf8c3c95d6/CRA_Methods0117) - Implementation guide
- [PMC: CRA with Autism Spectrum Disorder (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11660403/) - Recent effectiveness study

**Inquiry-Based Learning:**
- [PMC: Inquiry-Based Instruction and Student Attitudes](https://pmc.ncbi.nlm.nih.gov/articles/PMC11245149/) - Self-efficacy and interest outcomes
- [Springer: Inquiry-Based Math and Attitudes](https://link.springer.com/article/10.1007/s13394-023-00468-8) - Transformative effects study
- [Fordham Institute: When to Choose Inquiry vs. Direct Instruction](https://fordhaminstitute.org/national/commentary/when-choose-inquiry-based-learning-over-direct-instruction-stem) - Decision framework

**Blended Approaches:**
- [Balancing Explicit and Inquiry-Based Learning](https://blog.booknook.com/balancing-explicit-and-inquiry-based-learning-math-intervention) - Both/and framework
- [Teaching Math: Inquiry vs. Direct Instruction](https://teachpastthepotholes.com/math-inquiry-based-learning/) - Practitioner perspective on integration
- [Math Coach's Corner: Do We Need Direct Instruction?](https://www.mathcoachscorner.com/2015/09/direct-instruction-do-we-need-it/) - When direct instruction is appropriate

### Tertiary Sources (MEDIUM Confidence)

**Practitioner Resources:**
- [Instructional Models for Math - Colorado](https://www.cde.state.co.us/comath/math-instructional-models) - State guidance on lesson structures
- [Instructional Procedures: Launch-Explore-Summarize](https://www.drandrewgoodman.com/instructional-procedures-launchexploresummarize) - Implementation framework
- [Inquiry Maths](https://www.inquirymaths.com/) - Inquiry-based math teaching resources

**Market and Framework Analysis:**
- [NAEP 2026 Mathematics Framework](https://www.nagb.gov/content/dam/nagb/en/documents/publications/frameworks/mathematics/2026-math-frameowork/NAEP-2026-Mathematics-Framework-Combined.pdf) - National assessment framework
- [Science of Math: Misconceptions About Inquiry vs. Explicit Instruction](https://www.thescienceofmath.com/misconceptions-inquiry-based-versus-explicit-instruction) - Critique of false dichotomy

**Additional Research:**
- [EdWeek: Math Teaching Debates Heating Up (2026)](https://www.edweek.org/teaching-learning/debates-over-math-teaching-are-heating-up-they-could-affect-classrooms/2026/01) - Current state of debate
- [Learning Progressions in Mathematics](https://journals.sagepub.com/doi/abs/10.1177/00049441211045745) - Conceptual vs. procedural trajectories

---

## Research Complete

**Overall Confidence:** HIGH

The research draws primarily from authoritative sources (NCTM official positions, peer-reviewed research, established frameworks like 5 Practices and CRA). Key findings are corroborated across multiple independent sources. Areas of ongoing debate (pure inquiry vs. explicit instruction) are clearly identified with evidence on both sides.

**Gaps Requiring Phase-Specific Research:**
1. Operational classification criteria for "discovered vs. decided" mathematics (needs algorithmic rules for automation)
2. Prior knowledge assessment mechanisms (how to quickly determine novice vs. expert status)
3. Real-time productive struggle calibration (when to intervene, when to allow continued struggle)
4. Content-specific implementation for advanced high school topics (calculus, statistics, proofs)

**Ready for Implementation:** YES

Research provides sufficient foundation to:
- Build content classification system
- Create lesson structure templates matched to content types
- Implement expertise-responsive scaffolding
- Generate discussion protocols and question stems
- Apply NCTM 8 Effective Teaching Practices framework
- Integrate conceptual-procedural connections throughout

**Next Steps:**
1. Create operational definitions for content classification
2. Develop prior knowledge assessment protocol
3. Build lesson structure template library (Launch-Explore-Summarize, CRA, etc.)
4. Generate question banks for productive struggle scaffolding
5. Implement quality assurance checks based on research criteria
