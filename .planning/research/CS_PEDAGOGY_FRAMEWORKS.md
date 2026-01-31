# Evidence-Based Pedagog ical Frameworks for CS Education

**Domain:** Computer Science Instructional Design (Grades 9-12)
**Researched:** 2026-01-31
**Confidence:** HIGH

## Overview

This document details specific pedagogical frameworks validated through empirical research for high school computer science instruction. Each framework includes implementation guidance for automated lesson design.

---

## Framework 1: PRIMM (Predict, Run, Investigate, Modify, Make)

### Origin and Validation

**Developed by:** Dr. Sue Sentance et al. (2017, updated through 2025)
**Research base:** Based on Use-Modify-Create methodology, levels of abstraction in programming, and code comprehension research
**Empirical validation:**
- 13 schools, 493 students aged 11-14 (scalable to high school)
- 8-12 week implementation studies
- Positive teacher feedback on collaborative approach, structure, and differentiation

**Global adoption:** England, Germany, USA, Tasmania, Hong Kong, Argentina, Norway, Turkey

### The Five Stages

**1. Predict (5-15 minutes)**
**What:** Students look at a short program and predict what it will do
**Pedagogical rationale:** Activates prior knowledge, creates cognitive engagement before execution
**Can be:**
- Starter activity (5 min warm-up)
- Paired discussion (think-pair-share format)
- Whole-lesson activity for complex code (novices may need extended time)

**Implementation for automated lessons:**
```
- Present code snippet (5-15 lines for novices, up to 30 for advanced)
- Prediction prompt: "What will this program output? Explain your reasoning."
- Prediction format: Written response, diagram, or verbal explanation
- Scaffolding: Provide vocabulary list, annotate complex sections
- Assessment: Compare prediction to actual output (metacognitive reflection)
```

**Example prompt templates:**
- "Before running this code, predict what value will be stored in variable X."
- "What will appear on the screen when this program executes? Sketch the output."
- "Will this code produce an error? If so, where and why?"

**2. Run (2-5 minutes)**
**What:** Students download and execute the code to check predictions
**Pedagogical rationale:** Immediate feedback, no typing errors to debug (teacher-provided code)
**Key principle:** Students do NOT copy code manually - they download working code to focus on behavior, not syntax

**Implementation for automated lessons:**
```
- Provide downloadable code file or copy-paste ready code
- Clear execution instructions (IDE-specific or language-specific)
- Observation prompts: "What actually happened? How does it differ from your prediction?"
- Reflection question: "Why did the output match/differ from your prediction?"
- Error handling: If code doesn't run, troubleshoot environment (not code errors)
```

**3. Investigate (10-20 minutes)**
**What:** Structured activities to deepen understanding of code behavior
**Pedagogical rationale:** Develops program comprehension, builds code reading skills
**Activity types:**
- **Annotating code:** Add comments explaining each line/section
- **Parsons Problems:** Rearrange scrambled lines to match original
- **Debugging:** Find and fix intentional errors
- **Tracing:** Step through execution, tracking variable values
- **Labeling:** Identify components (variables, loops, conditionals)
- **Explaining:** Describe code function to a partner

**Implementation for automated lessons:**
```
SELECT activity type based on learning objective:
  - Code structure understanding → Annotating, labeling
  - Logic flow understanding → Tracing, diagramming
  - Syntax understanding → Parsons problems, error identification
  - Conceptual understanding → Explaining, summarizing

PROVIDE scaffolding:
  - Sentence starters: "This line of code..."
  - Guiding questions: "What happens when X equals 5?"
  - Partially completed examples

INCLUDE formative assessment:
  - Check annotations for accuracy
  - Validate trace tables
  - Review partner explanations
```

**Example investigation activities:**
```
Novice level (first exposure to loops):
- "Add comments to explain what each line does."
- "Draw a diagram showing how the loop counter changes."
- "Identify the loop condition and explain when it will stop."

Intermediate level (familiar with loops):
- "Trace the values of variables i and sum through each iteration."
- "Find the bug that causes an infinite loop and explain the fix."
- "Rearrange these scrambled lines to match the original program."

Advanced level (applying loop concepts):
- "Explain to a partner how this nested loop creates a multiplication table."
- "Identify efficiency issues in this loop and suggest improvements."
```

**4. Modify (15-25 minutes)**
**What:** Students make incremental changes to the code, progressing from simple to complex
**Pedagogical rationale:** Scaffolds from comprehension to creation, allows differentiation
**Progression strategy:** Start with simple changes, increase complexity gradually

**Implementation for automated lessons:**
```
MODIFICATION SEQUENCE (scaffold complexity):

Level 1 - Parameter changes:
  - "Change the loop to count from 1 to 20 instead of 1 to 10."
  - "Modify the message printed to include the user's name."

Level 2 - Logic changes:
  - "Add an else statement to handle negative numbers."
  - "Change the loop to count backwards."

Level 3 - Feature additions:
  - "Add input validation to reject non-numeric values."
  - "Extend the program to calculate average as well as sum."

Level 4 - Algorithmic changes:
  - "Modify the search algorithm to find all matches, not just the first."
  - "Change from iterative to recursive implementation."

DIFFERENTIATION built-in:
  - Struggling students: Stay at Levels 1-2, provide scaffolds
  - On-level students: Progress through Levels 1-3
  - Advanced students: Complete Level 4, add creative extensions
```

**Critical principle:** Modifications should be **incremental, not wholesale rewrites**. Students build confidence through successful small changes before tackling larger modifications.

**5. Make (20-30 minutes, can extend to full lesson or homework)**
**What:** Students create a brand new program using learned concepts in a different context
**Pedagogical rationale:** Transfer of learning, creative application, ownership of learning
**Key principle:** New context/problem, but can "borrow" code structures from original program

**Implementation for automated lessons:**
```
MAKE activity characteristics:
- Different problem domain than original code
- Same programming concepts/structures
- Clear success criteria
- Permission to reference original code

Example progression:
  Original: Calculate sum of numbers 1-10
  Make: Calculate product of user-input numbers

  Original: Count vowels in a string
  Make: Count palindromes in a list of words

  Original: Linear search for a value
  Make: Binary search with user-chosen target

SCAFFOLDING for Make phase:
  - Provide starter code structure (main function, imports)
  - List required components (variables, loops, conditionals needed)
  - Success criteria as test cases: "Your program should output X when given input Y"
  - Debugging hints for common issues

FORMATIVE ASSESSMENT:
  - Code review checklist (does it solve the problem? is it readable? efficient?)
  - Test case validation (passes all provided test cases)
  - Peer code review (explain code to partner)
```

### PRIMM Time Allocation

Based on research and teacher implementation data:

| Phase | Novice (First exposure) | Intermediate | Advanced |
|-------|------------------------|--------------|----------|
| Predict | 10-15 min | 5-10 min | 5 min |
| Run | 5 min | 2 min | 2 min |
| Investigate | 20-25 min | 15-20 min | 10-15 min |
| Modify | 20-25 min | 20-25 min | 15-20 min |
| Make | 25-35 min (or HW) | 30-40 min | 30-40 min |
| **Total** | **80-105 min (2 lessons)** | **72-97 min** | **62-82 min (1 lesson)** |

**Implication:** Novice learners need 2 class periods for full PRIMM sequence, while advanced students can complete in single extended period.

### PRIMM Collaboration Integration

**Research finding:** Teachers "particularly value the collaborative approach taken in PRIMM"

**Collaboration points:**
- **Predict:** Think-pair-share (individual prediction, then discuss with partner)
- **Investigate:** Partner annotation, peer code explanation
- **Modify:** Pair programming for complex modifications
- **Make:** Collaborative problem-solving, code reviews

**Implementation guidance:**
```
STRUCTURE collaboration explicitly:
- Define roles (driver/navigator, explainer/questioner)
- Set time limits for each phase (5 min individual, 3 min pair discussion)
- Provide discussion prompts: "Explain your reasoning to your partner"
- Include accountability: "Be ready to share your partner's idea"
```

### PRIMM Differentiation

**Research finding:** Teachers value "the way that resources can be differentiated"

**Differentiation strategies within PRIMM:**

**By phase depth:**
- Struggling: Extended Predict-Run-Investigate, simplified Modify, optional Make
- On-level: Standard PRIMM sequence
- Advanced: Brief Predict-Run, complex Investigate, challenging Modify, creative Make

**By scaffolding level:**
- Struggling: More scaffolding in Investigate (sentence starters, guiding questions), structured Modify tasks
- Advanced: Less scaffolding, open-ended challenges, extension tasks

**By code complexity:**
- Struggling: 5-10 line code examples, single concept
- On-level: 10-20 lines, integrated concepts
- Advanced: 20+ lines, nested structures, efficiency challenges

### PRIMM Assessment Opportunities

**Formative assessment built into framework:**
- **Predict:** Reveals prior knowledge, misconceptions
- **Run:** Confirms/challenges mental model
- **Investigate:** Demonstrates comprehension through annotation, tracing, explanation
- **Modify:** Shows application of understanding
- **Make:** Transfer of learning, creative problem-solving

**Assessment data points:**
- Accuracy of predictions (improving over time indicates developing mental model)
- Quality of code annotations (depth of understanding)
- Success rate on modifications (readiness for independent coding)
- Make program functionality (mastery of concepts)

---

## Framework 2: Use-Modify-Create (UMC)

### Origin and Validation

**Developed by:** Lee et al. (2011)
**Research base:** Cognitive Load Theory, scaffolded learning progressions
**Empirical validation:** Students in UMC classrooms finished tasks more quickly, particularly on Day 3 (modifying a bunny vs. coding from scratch)
**Key finding:** Time savings allow for additional elements or teacher-led discussions

### Three Stages

**1. Use (10-15 minutes)**
**What:** Students use an existing, working program
**Pedagogical rationale:** Builds familiarity with program behavior before examining code
**Activities:**
- Execute program with various inputs
- Observe outputs and behavior
- Document program features
- Identify program purpose

**Implementation:**
```
- Provide executable program (not source code yet)
- Use prompts: "Try different inputs. What does the program do?"
- Observation worksheet: "List 3 features you noticed"
- Purpose identification: "What problem does this solve?"
```

**2. Modify (20-30 minutes)**
**What:** Students make changes to the program's source code
**Pedagogical rationale:** Scaffolded entry into coding through guided changes
**Progression:** Simple → Complex modifications (same as PRIMM Modify)

**Key difference from PRIMM:** UMC emphasizes remixing and building on others' code as valid programming practice (aligns with real-world development)

**3. Create (20-30 minutes+)**
**What:** Students build original programs from scratch
**Pedagogical rationale:** Full creative expression after scaffolded practice
**Timing advantage:** UMC students reach this stage faster due to scaffold efficiency

**Implementation:**
```
- New problem related to Use/Modify context
- Reference materials from Use/Modify phases available
- Success criteria provided
- Scaffolding still available (starter code, hints)
```

### UMC vs. PRIMM Comparison

| Aspect | PRIMM | Use-Modify-Create |
|--------|-------|-------------------|
| **Phases** | 5 (Predict-Run-Investigate-Modify-Make) | 3 (Use-Modify-Create) |
| **Code reading** | Explicit (Predict-Run-Investigate) | Implicit (through Use) |
| **Scaffolding depth** | High (3 phases before modification) | Moderate (1 phase before modification) |
| **Research validation** | Extensive (13 schools, 493 students) | Moderate (comparison studies) |
| **Teacher preference** | High (valued for structure and differentiation) | Moderate |
| **Time efficiency** | Comprehensive but time-intensive | Faster to Create phase |
| **Code comprehension** | Strong emphasis | Less explicit emphasis |

**When to use each:**
- **PRIMM:** Novice programmers, complex concepts, when deep comprehension needed
- **UMC:** Intermediate programmers, when speed to creation valued, remix culture contexts

---

## Framework 3: Subgoal Labeling

### Origin and Validation

**Developed by:** Margulieux et al. (adapted for CS from psychology research)
**Research base:** Cognitive Load Theory, worked example effect
**Empirical validation:**
- Students performed better on initial assessments
- **Less likely to get failing grades or drop the course** (critical retention benefit)
- **Especially effective for struggling students**

**NSF funding:** Subgoals identified for CS1 topics and integrated into Runestone e-book

### What Are Subgoals?

**Definition:** Labels that group functionally-similar steps under a description of their function

**Purpose:** Reduce cognitive load by chunking information into manageable pieces

**CS1 subgoals documented for:**
- Variables and expressions
- Conditionals (if-else structures)
- Loops (for, while)
- Arrays/lists
- Functions/methods
- Classes and objects

### Implementation Strategy

**Worked example with subgoal labels:**

```python
# Subgoal: Initialize accumulator variable
total = 0

# Subgoal: Iterate through each element
for num in numbers:
    # Subgoal: Update accumulator
    total += num

# Subgoal: Return result
return total
```

**Without subgoal labels** (typical approach):
```python
# Calculate sum
total = 0
for num in numbers:
    total += num
return total
```

**Critical difference:** Subgoal labels name the **function/purpose** of code blocks, not just what they do

### Subgoal Fading Strategy

**Progression:** Full labels → Partial labels → No labels

**Phase 1 - Full subgoal labels (first 2-3 examples):**
```
# Subgoal: Initialize accumulator variable
count = 0

# Subgoal: Iterate through each element
for item in items:
    # Subgoal: Check condition
    if item > 0:
        # Subgoal: Update accumulator
        count += 1

# Subgoal: Return result
return count
```

**Phase 2 - Partial labels (next 2-3 examples):**
```
count = 0

# Subgoal: Iterate through each element
for item in items:
    if item > 0:
        # Subgoal: Update accumulator
        count += 1

return count
```

**Phase 3 - Student-generated labels (practice):**
Students add subgoal labels to unlabeled code

**Phase 4 - No labels (independent coding):**
Students internalized subgoal structure

### Subgoals for Common CS1 Patterns

**Variable initialization:**
- Subgoal: Initialize accumulator variable
- Subgoal: Set up counter variable
- Subgoal: Create storage variable

**Looping patterns:**
- Subgoal: Iterate through each element
- Subgoal: Repeat until condition met
- Subgoal: Process each item in collection

**Conditional patterns:**
- Subgoal: Check condition
- Subgoal: Validate input
- Subgoal: Test for special case

**Accumulator patterns:**
- Subgoal: Update accumulator
- Subgoal: Aggregate results
- Subgoal: Build output

**Result handling:**
- Subgoal: Return result
- Subgoal: Output final value
- Subgoal: Display result to user

### Integration with PRIMM

**Subgoals enhance PRIMM phases:**

**Investigate phase:**
- Students annotate code with subgoal labels (not just line-by-line comments)
- Identify functional chunks rather than individual lines

**Modify phase:**
- Modifications framed as subgoal changes: "Modify the accumulator update step to multiply instead of add"

**Make phase:**
- Students plan programs by listing needed subgoals first, then implement

**Example integrated activity:**
```
1. Predict: What will this labeled code do?
2. Run: Execute and verify prediction
3. Investigate: Match unlabeled code to subgoal labels
4. Modify: Change the "update accumulator" subgoal to calculate average
5. Make: Write a new program for [problem]; list subgoals first, then code
```

---

## Framework 4: Parsons Problems

### Origin and Validation

**Developed by:** Dale Parsons and Patricia Haden (2006)
**Research base:** Worked example effect, cognitive load management
**Empirical validation:**
- **"More efficient but just as effective" form of practice** than writing code from scratch
- Students with **low self-efficacy** benefit most (significantly higher performance and efficiency)
- Creates more supportive environment for struggling students

### What Are Parsons Problems?

**Definition:** Programming puzzles where students rearrange scrambled lines of code to form a correct program

**Format:**
- Provide all necessary code lines in random order
- Students drag-drop or reorder to create working program
- May include distractor lines (incorrect code to identify and exclude)

**Cognitive load benefit:** Eliminates syntax burden, focuses on logic and structure

### Variants and Complexity Levels

**1. Basic Parsons Problem**
- All lines provided in scrambled order
- No distractors
- Correct solution is unique
- **Difficulty:** Novice

**Example:**
```
Scrambled lines (rearrange these):
    total += num
total = 0
for num in numbers:
    return total
```

**2. Parsons Problem with Distractors**
- Includes 1-3 incorrect lines to identify and exclude
- Tests comprehension of correct vs. incorrect code
- **Difficulty:** Intermediate

**Example:**
```
Scrambled lines (some are wrong - exclude them):
    total += num
total = 0
total = []  # DISTRACTOR (wrong type)
for num in numbers:
    return total
return sum(total)  # DISTRACTOR (wrong function)
```

**3. Faded Parsons Problem (FPP)**
- Some lines provided, others are blanks to fill in
- Bridges from rearranging to writing
- **Difficulty:** Intermediate to Advanced

**Example:**
```
Provided structure:
total = ___________  # FILL IN
for num in numbers:
    ___________  # FILL IN
return ___________  # FILL IN
```

**4. Two-Dimensional Parsons Problem**
- Lines must be ordered AND indented correctly
- Tests understanding of code structure (loops, conditionals, functions)
- **Difficulty:** Intermediate

**5. Adaptive/Personalized Parsons Problem**
- Difficulty adjusts based on student performance
- Generated from student's own code attempts (fix their errors via rearranging)
- **Difficulty:** Varies

### Implementation in Lesson Sequence

**Progression strategy: Parsons → Faded Parsons → Write from Scratch**

**Week 1 (Introduction to concept):**
- Day 1: Worked example + Basic Parsons Problem
- Day 2: Parsons with distractors
- Day 3: Two-dimensional Parsons (ordering + indentation)

**Week 2 (Developing fluency):**
- Day 1: Faded Parsons (fill in 30% of code)
- Day 2: Faded Parsons (fill in 50% of code)
- Day 3: Faded Parsons (fill in 70% of code)

**Week 3 (Independence):**
- Day 1: Write from scratch with scaffolding
- Day 2: Write from scratch with minimal scaffolding
- Day 3: Independent coding

**Time savings:** Research shows Parsons problems can be solved faster, allowing more practice problems in same timeframe

### Parsons + PRIMM Integration

**Enhanced PRIMM sequence:**

1. **Predict:** Show scrambled Parsons problem, predict correct order
2. **Run:** After reordering, run the code to verify
3. **Investigate:** Analyze why correct order works, what would happen with different orders
4. **Modify:** Change the reordered code (e.g., modify loop condition)
5. **Make:** Write similar code from scratch

**Benefits of integration:**
- Reduces cognitive load during Modify phase
- Provides scaffold for struggling students
- Allows differentiation (some students do Parsons, others write from scratch)

### Automated Generation of Parsons Problems

**Algorithm:**
1. Take working code example
2. Identify logical line boundaries
3. Scramble lines (while preserving dependencies for very novice levels)
4. Optionally add distractors (common misconceptions, syntax errors)
5. Present to students with reordering interface

**Distractor selection strategies:**
- Common syntax errors (missing colons, wrong indentation)
- Logical errors (off-by-one in loops, wrong variable names)
- Misconception-based errors (parallelism assumptions, hidden mind bugs)

---

## Framework 5: Worked Examples and Fading

### Origin and Validation

**Research base:** Cognitive Load Theory, expertise reversal effect
**Empirical validation:** Worked examples reduce cognitive load for novices, but become ineffective for intermediate/advanced learners (must fade)

### Worked Example Structure

**Complete worked example (full support):**
```
Problem: Calculate the sum of all even numbers from 1 to N

Step 1: Initialize accumulator variable
    total = 0

Step 2: Iterate through range from 1 to N+1
    for num in range(1, N+1):

Step 3: Check if number is even
        if num % 2 == 0:

Step 4: Add even number to accumulator
            total += num

Step 5: Return the accumulated sum
    return total

Explanation: We use the modulo operator (%) to check if a number
is even (remainder 0 when divided by 2). The accumulator pattern
adds each even number to a running total.
```

### Fading Strategy

**Level 1 - Full worked example:** Complete solution with explanations
**Level 2 - Completion problem:** Partial solution, student fills gaps
**Level 3 - Scaffolded problem:** Structure provided, student implements
**Level 4 - Independent problem:** No scaffolding

**Example progression:**

**Level 1 (worked example):**
```python
# Complete solution provided
def sum_even(N):
    total = 0
    for num in range(1, N+1):
        if num % 2 == 0:
            total += num
    return total
```

**Level 2 (completion problem):**
```python
def sum_even(N):
    total = 0
    for num in range(1, N+1):
        # FILL IN: Check if number is even and add to total
        ____________________
    return total
```

**Level 3 (scaffolded problem):**
```python
# Write a function that sums all multiples of 3 from 1 to N
# Steps:
# 1. Initialize accumulator
# 2. Loop through range
# 3. Check if divisible by 3
# 4. Add to accumulator
# 5. Return result

def sum_multiples_of_three(N):
    # YOUR CODE HERE
```

**Level 4 (independent problem):**
```
Write a function that calculates the product of all odd numbers from 1 to N.
```

### Optimal Fading Rate

**Research guidance:** Fade too slowly = boredom and disengagement; fade too quickly = cognitive overload

**Indicators to increase scaffolding (fade slower):**
- Student error rate >50% on completion problems
- Students report feeling overwhelmed
- Wide variance in completion times

**Indicators to decrease scaffolding (fade faster):**
- Student error rate <20%
- Students complete early and request more challenge
- Students skip scaffolded steps

**Adaptive fading:** Adjust scaffolding level based on individual student performance

---

## Framework Integration Matrix

| Learning Goal | Recommended Framework | Rationale |
|---------------|----------------------|-----------|
| **First exposure to new concept** | PRIMM (full sequence) | Comprehensive scaffolding, code comprehension before creation |
| **Practicing new concept** | Parsons Problems → Faded Parsons | Efficient practice, reduces cognitive load |
| **Complex multi-step procedures** | Subgoal Labeling | Chunks information, especially helps struggling students |
| **Skill retention** | Use-Modify-Create | Active application, builds on prior work |
| **Transfer to new context** | PRIMM (Make phase) or UMC (Create) | Transfer of learning with scaffolding |
| **Differentiation** | Faded strategies (all frameworks) | Adjust scaffolding to student ability |

### Combined Framework Lesson Example

**Topic:** Introduction to while loops (Grade 9-10)

**Lesson structure:**

**Part 1 - PRIMM (Predict-Run-Investigate): 20 minutes**
- Provide working while loop code
- Students predict output
- Run code to verify
- Annotate code with subgoal labels (Framework 3)

**Part 2 - Parsons Problem: 15 minutes**
- Scrambled while loop code (different example)
- Students rearrange to create working program
- Includes 2 distractors (common while loop errors)

**Part 3 - PRIMM (Modify): 15 minutes**
- Modify the Parsons solution to solve related problem
- Scaffold with subgoal labels

**Part 4 - Worked Example + Fading: 15 minutes**
- Full worked example of sentinel-controlled loop
- Completion problem: Fill in condition check

**Part 5 - PRIMM (Make): 20 minutes (or HW)**
- Create new while loop program for different problem
- Can reference all previous examples

**Total time:** 85 minutes (one block period or two standard periods)

---

## Sources

### PRIMM
- [PRIMM Support Portal](https://primmportal.com/)
- [Barefoot Computing: PRIMM Research Zone](https://www.barefootcomputing.org/my-barefoot/research-zone/primm)
- [ACM SIGCSE 2019: Teachers' Experiences of using PRIMM](https://dl.acm.org/doi/10.1145/3287324.3287477)
- [Raspberry Pi: Teaching Programming with PRIMM](https://www.raspberrypi.org/app/uploads/2022/08/Teaching_Programming_with_PRIMM-1.pdf)
- [Teach Computing: Using PRIMM to structure programming lessons](https://blog.teachcomputing.org/using-primm-to-structure-programming-lessons/)

### Use-Modify-Create
- [NSF: Use, Modify, Create: Comparing Computational Thinking](https://par.nsf.gov/servlets/purl/10122993)

### Subgoal Labeling
- [CS1 Subgoals Project](https://www.cs1subgoals.org/publications/)
- [AAAS IUSE: Using Subgoal Labels](https://aaas-iuse.org/resource/using-subgoal-labels-to-better-support-student-learning-in-introductory-programming-courses/)
- [ACM SIGCSE 2018: Subgoal Labeled Worked Examples in K-3](https://dl.acm.org/doi/10.1145/3159450.3159494)

### Parsons Problems
- [ACM SIGCSE 2024: Integrating Personalized Parsons Problems](https://dl.acm.org/doi/10.1145/3626253.3635606)
- [ACM ITiCSE 2025: Fading Strategies for Parsons Problems](https://dl.acm.org/doi/10.1145/3724363.3729062)
- [Raspberry Pi: AI-generated Parson's Problems](https://www.raspberrypi.org/blog/supporting-learners-with-programming-tasks-through-ai-generated-parsons-problems/)
- [arXiv 2023: Effects of Scaffolding Parsons Problems](https://arxiv.org/abs/2311.18115)
