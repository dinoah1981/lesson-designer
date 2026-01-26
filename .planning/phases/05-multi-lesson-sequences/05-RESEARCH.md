# Phase 5: Multi-Lesson Sequences - Research

**Researched:** 2026-01-26
**Domain:** Multi-lesson context management, curriculum sequencing, vector embeddings
**Confidence:** MEDIUM

## Summary

Phase 5 transforms the tool from single-lesson generation to multi-lesson sequence planning with context awareness. The primary technical challenge is managing LLM context across 2-4 week units (potentially 10+ lessons) while maintaining quality and coherence. Research reveals that naive context window approaches fail past 32K tokens, even with modern 200K+ token models, requiring structured context management strategies.

The standard approach in 2026 for multi-turn, multi-document AI applications combines:
1. **Structured metadata schemas** for lesson interdependencies (competency progression, prerequisite tracking, vocabulary continuity)
2. **Semantic retrieval (RAG)** using vector embeddings to fetch relevant prior lesson content rather than stuffing all previous lessons into context
3. **Hierarchical summarization** creating compressed "essence summaries" at lesson and unit levels
4. **Terminology tracking** maintaining vocabulary consistency across sequences

This is NOT a theoretical architectural exercise. Multiple production AI systems (coding assistants, customer support, educational tools) solve similar multi-session context problems using these proven patterns.

**Primary recommendation:** Implement a hybrid approach with session-level metadata (JSON) for structured dependencies, selective context loading (fetch only relevant prior lessons), and progressive summarization (compress older lessons as sequence grows).

## Standard Stack

The established libraries/tools for context management and semantic retrieval:

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **FAISS** | Latest (2026) | In-memory vector similarity search | 1000x faster than cloud alternatives for local search, zero latency, no API costs. Facebook AI Research library, battle-tested at scale. |
| **sentence-transformers** | Latest (2026) | Generate text embeddings locally | State-of-the-art embeddings without API calls. Open source, many pre-trained models (all-MiniLM-L6-v2 for speed, all-mpnet-base-v2 for accuracy). |
| **json** (stdlib) | Python 3.x | Structured metadata storage | Already in use for lesson JSON, extend for sequence metadata. No dependencies. |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **numpy** | Latest | Vector operations for FAISS | Required dependency for FAISS similarity search |
| **tiktoken** | Latest | Token counting for context management | OpenAI's tokenizer, accurate token counts for Claude's tokenizer (similar BPE approach) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| FAISS (local) | **ChromaDB** | ChromaDB provides database-like persistence and is easier to use, but adds dependency overhead for simple retrieval tasks. Use if persistence across sessions is critical. |
| FAISS (local) | **Pinecone** (cloud) | Pinecone is fully managed and scales automatically, but requires API calls (latency), costs money, and introduces external dependency. Use only if scaling beyond thousands of lessons. |
| sentence-transformers | **OpenAI Embeddings API** | Higher quality embeddings for complex semantic matching, but costs per embedding call and requires API dependency. Use if local embeddings prove insufficient. |
| Structured metadata | **Full RAG pipeline** | Tools like LangChain provide turnkey RAG, but add significant complexity for what's fundamentally a metadata lookup problem. Don't over-engineer. |

**Installation:**
```bash
pip install faiss-cpu sentence-transformers numpy tiktoken
```

Note: Use `faiss-cpu` not `faiss-gpu` unless teachers have CUDA GPUs (unlikely).

## Architecture Patterns

### Recommended Project Structure

Extend existing session structure to support sequences:

```
.lesson-designer/
└── sessions/
    └── {sequence_id}/                          # UUID for entire sequence
        ├── sequence_metadata.json               # NEW: Sequence-level planning
        ├── lesson_01/
        │   ├── 01_input.json                   # Existing lesson files
        │   ├── 04_lesson_final.json
        │   ├── lesson_summary.json             # NEW: Compressed essence
        │   └── materials/                       # Generated files
        ├── lesson_02/
        │   ├── 01_input.json
        │   ├── context_from_prior.json         # NEW: Retrieved context
        │   ├── 04_lesson_final.json
        │   ├── lesson_summary.json
        │   └── materials/
        ├── embeddings/                          # NEW: Vector search index
        │   ├── index.faiss                     # FAISS index file
        │   └── id_mapping.json                 # Maps vectors to lesson/section IDs
        └── sequence_summary.json                # NEW: Unit-level summary
```

### Pattern 1: Sequence Planning (Up-Front Metadata)

**What:** Capture lesson interdependencies during initial planning before generating individual lessons.

**When to use:** Always for multi-lesson sequences. Establishes the roadmap.

**Example:**
```python
# Source: Educational research on backward design + curriculum mapping
# From: https://teaching.uic.edu/cate-teaching-guides/syllabus-course-design/backward-design/
#       https://www.edglossary.org/learning-progression/

sequence_metadata = {
    "sequence_id": "uuid-v4-string",
    "title": "Analyzing Primary Sources: Civil War Unit",
    "grade_level": "8th grade",
    "total_lessons": 8,
    "competencies": [
        {
            "id": "comp-01",
            "statement": "Students will analyze primary sources to evaluate historical claims",
            "lesson_range": [1, 4],
            "target_proficiency": "Students can independently analyze unfamiliar primary sources"
        },
        {
            "id": "comp-02",
            "statement": "Students will construct evidence-based arguments using multiple primary sources",
            "lesson_range": [5, 8],
            "target_proficiency": "Students can write 3-paragraph arguments citing 3+ sources",
            "prerequisites": ["comp-01"]  # Depends on prior competency
        }
    ],
    "vocabulary_progression": {
        "lesson_01": ["primary source", "secondary source", "bias"],
        "lesson_02": ["perspective", "audience", "purpose"],
        "lesson_03": ["corroboration", "sourcing"],
        # Terms accumulate - lesson 3 assumes students know lesson 1-2 terms
    },
    "assessments": {
        "formative": [1, 2, 3, 4, 5, 6, 7],  # Lesson numbers with embedded assessment
        "summative": [8]  # Final performance task
    },
    "created_at": "2026-01-26T10:30:00Z"
}
```

**Key insight:** This metadata enables the tool to:
- Know what prior lessons taught when designing lesson N
- Track which vocabulary has been introduced
- Maintain skill progression (comp-02 builds on comp-01)
- Generate summative assessments covering the full sequence

### Pattern 2: Lesson Summarization (Progressive Compression)

**What:** After generating each lesson, create a compressed summary capturing essential information for future lesson design.

**When to use:** After Stage 7 completion for each lesson in a sequence.

**Example:**
```python
# Source: Context compression research (EDU-based decomposition)
# From: https://arxiv.org/pdf/2512.14244 (Jan 2026)

def create_lesson_summary(lesson_json: dict, lesson_number: int) -> dict:
    """
    Create compressed lesson summary for context retrieval.

    Extracts only information relevant to subsequent lesson design:
    - What competencies were addressed
    - What vocabulary was introduced with definitions
    - What prior knowledge was assumed
    - What Marzano levels were reached
    - What worked well / what struggled (from persona feedback)
    """
    return {
        "lesson_number": lesson_number,
        "title": lesson_json["title"],
        "competency": lesson_json["objective"],  # The skill practiced

        # Vocabulary introduced (future lessons can reference)
        "vocabulary_introduced": [
            {"term": term, "definition": defn, "context": ctx}
            for term, defn, ctx in extract_vocabulary(lesson_json)
        ],

        # Prior knowledge assumed (future lessons can build on)
        "assumed_knowledge": lesson_json.get("knowledge_breakdown", {}).get("already_assumed", []),

        # Skills practiced and proficiency level reached
        "skills_practiced": {
            "skill": extract_core_skill(lesson_json),
            "proficiency_target": lesson_json.get("proficiency_target", ""),
            "marzano_levels": count_marzano_levels(lesson_json["activities"])
        },

        # Persona feedback signals (what to avoid/repeat)
        "pedagogical_notes": {
            "worked_well": extract_positive_feedback(lesson_json),
            "struggled_with": extract_concerns(lesson_json),
            "differentiation_applied": extract_differentiation(lesson_json)
        },

        # Context window efficiency: ~200-300 tokens vs 2000+ for full lesson
        "token_estimate": 250
    }
```

**Key insight:** Summaries are 10-20x smaller than full lessons but retain critical context for coherence.

### Pattern 3: Selective Context Retrieval (RAG for Prior Lessons)

**What:** Use semantic search to fetch only relevant prior lesson content when designing lesson N, rather than loading all N-1 previous lessons.

**When to use:** Before Stage 3 (lesson design) for lessons 2+ in a sequence.

**Example:**
```python
# Source: Semantic search with FAISS + sentence-transformers
# From: https://huggingface.co/learn/llm-course/chapter5/6
#       https://medium.com/@smenon_85/mastering-semantic-search-in-2026-44bc012c4e41

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SequenceContextManager:
    """Manages context retrieval for multi-lesson sequences."""

    def __init__(self, sequence_id: str):
        self.sequence_id = sequence_id
        self.embeddings_dir = get_sequence_dir(sequence_id) / "embeddings"

        # Load embedding model (runs locally, no API)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, good quality

        # Load FAISS index if exists
        index_path = self.embeddings_dir / "index.faiss"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
            with open(self.embeddings_dir / "id_mapping.json") as f:
                self.id_mapping = json.load(f)
        else:
            # Initialize empty index (384 dims for all-MiniLM-L6-v2)
            self.index = faiss.IndexFlatL2(384)
            self.id_mapping = []

    def add_lesson_summary(self, lesson_num: int, summary: dict):
        """Add lesson summary to searchable index."""
        # Create searchable text chunks from summary
        chunks = [
            f"Lesson {lesson_num}: {summary['title']}",
            f"Competency: {summary['competency']}",
            f"Vocabulary: {', '.join([v['term'] for v in summary['vocabulary_introduced']])}",
            # ... more chunks
        ]

        # Generate embeddings
        embeddings = self.model.encode(chunks, convert_to_numpy=True)

        # Add to FAISS index
        self.index.add(embeddings)

        # Track IDs (which chunks belong to which lesson)
        for i, chunk in enumerate(chunks):
            self.id_mapping.append({
                "lesson_number": lesson_num,
                "chunk_type": chunk.split(":")[0],  # "Lesson", "Competency", etc.
                "content": chunk
            })

        # Persist
        self._save_index()

    def retrieve_relevant_context(self, current_lesson_goal: str, top_k: int = 5) -> list:
        """
        Retrieve most relevant prior lesson content for current lesson design.

        Args:
            current_lesson_goal: The competency statement for lesson being designed
            top_k: Number of relevant chunks to retrieve

        Returns:
            List of relevant context chunks from prior lessons
        """
        # Embed the query
        query_embedding = self.model.encode([current_lesson_goal], convert_to_numpy=True)

        # Search FAISS index
        distances, indices = self.index.search(query_embedding, top_k)

        # Retrieve matching chunks
        results = []
        for idx in indices[0]:
            if idx < len(self.id_mapping):
                results.append(self.id_mapping[idx])

        return results

    def get_full_context_for_lesson(self, lesson_num: int) -> dict:
        """
        Build context package for designing lesson N.

        Combines:
        - Sequence metadata (always included)
        - Prior lesson summaries (all of them, if small)
        - Semantically retrieved relevant chunks (if needed)
        """
        metadata = load_sequence_metadata(self.sequence_id)

        # All prior lessons
        prior_summaries = []
        for i in range(1, lesson_num):
            summary_path = get_lesson_dir(self.sequence_id, i) / "lesson_summary.json"
            if summary_path.exists():
                prior_summaries.append(load_json(summary_path))

        # Calculate token count
        total_tokens = estimate_tokens(metadata) + sum(s["token_estimate"] for s in prior_summaries)

        if total_tokens < 10000:  # Well under context limit
            # Include everything directly
            return {
                "sequence_metadata": metadata,
                "prior_lessons": prior_summaries,
                "retrieval_used": False
            }
        else:
            # Use selective retrieval
            current_goal = metadata["competencies"][lesson_num - 1]["statement"]
            relevant_chunks = self.retrieve_relevant_context(current_goal, top_k=10)

            return {
                "sequence_metadata": metadata,
                "relevant_prior_context": relevant_chunks,
                "retrieval_used": True,
                "note": "Full prior lessons available if needed"
            }
```

**Key insight:** FAISS provides <5ms search latency locally, enabling dynamic context assembly without API calls or cloud dependencies.

### Pattern 4: Vocabulary Continuity Tracking

**What:** Maintain explicit tracking of introduced terms to ensure consistency and avoid re-teaching.

**When to use:** Throughout sequence design and in Stage 3 lesson design prompts.

**Example:**
```python
# Source: Learning progressions research
# From: https://www.edglossary.org/learning-progression/

def check_vocabulary_continuity(sequence_id: str, lesson_num: int, draft_lesson: dict) -> dict:
    """
    Validate vocabulary usage for coherence across sequence.

    Returns:
        - previously_taught: Terms the lesson can use without defining
        - newly_introduced: Terms this lesson introduces (should be defined)
        - incorrectly_assumed: Terms used but not previously taught (ERROR)
    """
    # Load sequence vocabulary progression
    metadata = load_sequence_metadata(sequence_id)
    vocab_progression = metadata["vocabulary_progression"]

    # What's been taught so far
    taught_terms = set()
    for i in range(1, lesson_num):
        lesson_key = f"lesson_{i:02d}"
        if lesson_key in vocab_progression:
            taught_terms.update(vocab_progression[lesson_key])

    # What this lesson uses
    lesson_terms = extract_vocabulary_from_lesson(draft_lesson)

    # Categorize
    previously_taught = [t for t in lesson_terms if t in taught_terms]
    newly_introduced = vocab_progression.get(f"lesson_{lesson_num:02d}", [])
    incorrectly_assumed = [t for t in lesson_terms if t not in taught_terms and t not in newly_introduced]

    return {
        "previously_taught": previously_taught,  # Can reference without definition
        "newly_introduced": newly_introduced,    # Should define explicitly
        "incorrectly_assumed": incorrectly_assumed,  # VALIDATION ERROR
        "is_coherent": len(incorrectly_assumed) == 0
    }
```

**Key insight:** Explicit vocabulary tracking prevents cognitive overload and maintains progression fidelity.

### Anti-Patterns to Avoid

- **Stuffing all prior lessons into context:** Modern models have large context windows (Claude: 200K tokens), but research shows performance degradation past 32K tokens even on top models. Don't rely on raw context window size.

- **Re-generating prior lessons when adding to sequence:** Each lesson is immutable once approved. The sequence planning happens up-front, and context retrieval reads from completed lessons. Don't create circular dependencies.

- **Using LLM for summarization:** It's tempting to use Claude to "summarize lesson 1-3 for context." This doubles LLM calls and introduces latency. Use structured extraction (JSON fields) instead.

- **Over-indexing for small sequences:** For 2-3 lesson sequences, semantic search is overkill. Simple JSON loading of prior lesson summaries is sufficient. Reserve FAISS indexing for sequences of 5+ lessons.

- **Treating sequences as branching trees:** Learning progressions are linear or minimally branching (prerequisite tracking, not decision trees). Don't over-engineer with graph databases.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Vector similarity search | Custom cosine similarity loops | **FAISS** | GPU-optimized, handles millions of vectors, 1000x faster than naive implementations. Extensively tested by Facebook AI. |
| Text embeddings | Average word2vec or bag-of-words | **sentence-transformers** | Pre-trained transformers capture semantic meaning. "primary source analysis" and "analyzing historical documents" have high similarity despite different words. |
| Token counting | Split on spaces or count characters | **tiktoken** | BPE tokenizers are non-trivial. "Hello world" ≠ 2 tokens. Claude uses BPE similar to OpenAI's. |
| Context compression | Truncate text or take first N tokens | **Structured summarization** | LLMs need semantic coherence. Truncation breaks sentences and loses critical context. Extract structured fields instead. |
| Lesson prerequisite tracking | Hand-rolled topological sort | **Simple JSON with prerequisite arrays** | Don't over-engineer. Educational progressions are mostly linear with occasional prerequisites. JSON arrays are sufficient. |

**Key insight:** The complexity is in semantic understanding (embeddings) and efficient search (FAISS), not in data structures. Use battle-tested libraries for the hard parts.

## Common Pitfalls

### Pitfall 1: Context Window Overconfidence

**What goes wrong:** Assuming large context windows solve everything. "Claude has 200K tokens, so I'll just load all 10 prior lessons directly."

**Why it happens:** Marketing materials emphasize context window size. Developers assume bigger = better.

**How to avoid:**
- Read the research: [Best LLMs for Extended Context Windows in 2026](https://research.aimultiple.com/ai-context-window/) shows "sharp performance drops past 32K tokens" even on top models.
- Implement structured context management from the start (summarization + retrieval).
- Measure quality degradation empirically: test lesson 10 quality with and without context compression.

**Warning signs:**
- Lessons 7-10 feel "disconnected" from earlier lessons despite full context inclusion
- LLM starts ignoring specific instructions buried in massive context
- Vocabulary definitions repeat or contradict earlier lessons

### Pitfall 2: Sequence Planning After Lesson 1

**What goes wrong:** Teacher designs lesson 1, then asks "now design lesson 2 that builds on this." Without up-front sequence planning, progression is reactive rather than intentional.

**Why it happens:** Existing single-lesson workflow encourages incremental addition. "Just add another lesson" feels simpler than planning the full sequence.

**How to avoid:**
- Require sequence metadata BEFORE generating lesson 1 for multi-lesson requests.
- Use backward design: define end-of-sequence competency first, then decompose into lesson progression.
- Reference: [Backward Design in Education](https://teaching.uic.edu/cate-teaching-guides/syllabus-course-design/backward-design/) (University of Illinois Chicago)

**Warning signs:**
- Teacher says "I don't know how many lessons yet, let's start with one"
- Lesson 2 objective doesn't clearly build on lesson 1's proficiency target
- Sequence feels like disconnected lessons rather than coherent unit

### Pitfall 3: Embedding Model Mismatch

**What goes wrong:** Using embeddings optimized for web search (OpenAI's text-embedding-ada-002) or code search (CodeBERT) for educational content.

**Why it happens:** Developers grab the most popular embedding model without checking domain fit.

**How to avoid:**
- For educational sequences, use general-domain sentence transformers: `all-mpnet-base-v2` (high quality) or `all-MiniLM-L6-v2` (fast).
- These models are trained on semantic similarity tasks (paraphrase detection, natural language inference), which aligns with lesson coherence checking.
- Reference: [Best Embedding Models for Semantic Search](https://www.graft.com/blog/text-embeddings-for-search-semantic)

**Warning signs:**
- Semantic search returns irrelevant lessons (e.g., "analyzing primary sources" retrieves "analyzing polynomials" because both use "analyze")
- Teachers report "the tool doesn't remember what we covered last week"

### Pitfall 4: No Vocabulary Accumulation Strategy

**What goes wrong:** Later lessons either re-define terms from earlier lessons (wasting time) or use terms without definition (assuming students remember everything).

**Why it happens:** Each lesson is designed independently without explicit vocabulary tracking.

**How to avoid:**
- Maintain `vocabulary_progression` in sequence metadata (see Pattern 1).
- In Stage 3 prompts for lesson N, provide two vocabulary lists:
  - **Can reference:** Terms from lessons 1 to N-1 (no need to re-teach)
  - **Must introduce:** New terms for lesson N
- Validate lesson drafts for vocabulary coherence (see Pattern 4).

**Warning signs:**
- Lesson 5 re-defines "primary source" that was taught in lesson 1
- Lesson 6 uses "corroboration" without explanation, but it was never introduced
- Students would need perfect recall of all prior lessons to understand later lessons

### Pitfall 5: Ignoring Persona Feedback Across Sequences

**What goes wrong:** Persona feedback is isolated per lesson. If Alex (struggling learner) flagged vocabulary issues in lesson 3, lesson 4 makes the same mistake.

**Why it happens:** Existing persona feedback system (Phase 3-4) is per-lesson. Multi-lesson sequences need sequence-level feedback tracking.

**How to avoid:**
- After each lesson's persona feedback, extract **sequence-level lessons learned**.
- Store in `sequence_summary.json` → `pedagogical_patterns` field.
- Include in context for subsequent lesson design: "Previous persona feedback found vocabulary density issues in lessons 1-3. Lesson 4 should maintain current vocabulary scaffolding approach."

**Warning signs:**
- All 4 personas flag the same accessibility issue in lessons 3, 5, and 7
- Teacher comments "I thought we fixed the pacing problem"
- Persona ratings degrade over the sequence (lesson 1: 4/5, lesson 8: 2/5)

## Code Examples

Verified patterns from research and existing codebase:

### Extending Session Management for Sequences

```python
# Source: Existing parse_competency.py + sequence metadata pattern
# Location: .claude/skills/lesson-designer/scripts/parse_competency.py

def create_sequence_session(
    competencies: list[str],
    grade_level: str,
    total_lessons: int,
    lesson_duration: int
) -> str:
    """
    Create session directory for multi-lesson sequence.

    Returns:
        sequence_id (str): UUID for the entire sequence
    """
    sequence_id = generate_session_id()  # Existing function
    sequence_dir = get_sessions_dir() / sequence_id
    sequence_dir.mkdir(parents=True, exist_ok=True)

    # Create sequence metadata
    metadata = {
        "sequence_id": sequence_id,
        "grade_level": grade_level,
        "total_lessons": total_lessons,
        "lesson_duration": lesson_duration,
        "competencies": [
            {
                "id": f"comp-{i+1:02d}",
                "statement": comp,
                "lesson_range": None,  # Teacher specifies during planning
                "prerequisites": []
            }
            for i, comp in enumerate(competencies)
        ],
        "vocabulary_progression": {},
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    # Save sequence metadata
    with open(sequence_dir / "sequence_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Create lesson subdirectories
    for i in range(1, total_lessons + 1):
        (sequence_dir / f"lesson_{i:02d}").mkdir(exist_ok=True)

    # Create embeddings directory
    (sequence_dir / "embeddings").mkdir(exist_ok=True)

    return sequence_id


def get_lesson_directory(sequence_id: str, lesson_num: int) -> Path:
    """Get path to specific lesson within sequence."""
    return get_sessions_dir() / sequence_id / f"lesson_{lesson_num:02d}"
```

### Context Assembly for Lesson N

```python
# Source: RAG pattern + existing lesson design workflow
# New file: .claude/skills/lesson-designer/scripts/sequence_context.py

def build_context_for_lesson(sequence_id: str, lesson_num: int) -> dict:
    """
    Assemble context for designing lesson N in a sequence.

    Returns context package with:
    - Sequence metadata (competencies, progression)
    - Prior lesson summaries or retrieved relevant chunks
    - Vocabulary accumulation
    - Pedagogical patterns from persona feedback
    """
    sequence_dir = get_sessions_dir() / sequence_id

    # Load sequence metadata (always included)
    with open(sequence_dir / "sequence_metadata.json") as f:
        metadata = json.load(f)

    # Collect prior lesson summaries
    prior_summaries = []
    for i in range(1, lesson_num):
        summary_path = sequence_dir / f"lesson_{i:02d}" / "lesson_summary.json"
        if summary_path.exists():
            with open(summary_path) as f:
                prior_summaries.append(json.load(f))

    # Vocabulary accumulation
    vocab_taught = set()
    for i in range(1, lesson_num):
        lesson_key = f"lesson_{i:02d}"
        if lesson_key in metadata.get("vocabulary_progression", {}):
            vocab_taught.update(metadata["vocabulary_progression"][lesson_key])

    # Current lesson's competency
    current_competency = None
    for comp in metadata["competencies"]:
        lesson_range = comp.get("lesson_range", [])
        if lesson_range and lesson_range[0] <= lesson_num <= lesson_range[1]:
            current_competency = comp
            break

    # Estimate context size
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")  # Approximation for Claude

    metadata_tokens = len(enc.encode(json.dumps(metadata)))
    summaries_tokens = sum(s.get("token_estimate", 500) for s in prior_summaries)
    total_tokens = metadata_tokens + summaries_tokens

    # Build context package
    context = {
        "sequence_metadata": metadata,
        "current_lesson_number": lesson_num,
        "current_competency": current_competency,
        "vocabulary_already_taught": sorted(vocab_taught),
        "vocabulary_to_introduce": metadata.get("vocabulary_progression", {}).get(f"lesson_{lesson_num:02d}", []),
        "context_size_estimate": total_tokens
    }

    # Selective inclusion of prior lessons
    if total_tokens < 15000:
        # Include all summaries directly
        context["prior_lessons"] = prior_summaries
    else:
        # TODO Phase 5: Implement FAISS retrieval for large sequences
        # For now, include most recent 3 lessons + specific prerequisites
        context["prior_lessons"] = prior_summaries[-3:]
        context["note"] = "Limited to 3 most recent lessons. Retrieval system needed for longer sequences."

    return context
```

### Lesson Summarization After Generation

```python
# Source: Compression pattern from research
# Location: Extend existing workflow after Stage 7

def create_lesson_summary_for_sequence(
    sequence_id: str,
    lesson_num: int,
    lesson_json: dict,
    persona_feedback: list[dict]
) -> dict:
    """
    Create compressed lesson summary for future context retrieval.

    Args:
        sequence_id: The sequence this lesson belongs to
        lesson_num: Lesson number (1-based)
        lesson_json: Full lesson JSON (04_lesson_final.json)
        persona_feedback: Feedback from all 4 personas

    Returns:
        Compressed summary (~250 tokens vs 2000+ for full lesson)
    """
    # Extract vocabulary with definitions
    vocabulary = []
    for activity in lesson_json.get("activities", []):
        if "vocabulary" in activity:
            for term in activity["vocabulary"]:
                if isinstance(term, dict):
                    vocabulary.append({
                        "term": term["term"],
                        "definition": term["definition"],
                        "example": term.get("example", "")
                    })
                elif isinstance(term, str):
                    vocabulary.append({"term": term, "definition": "", "example": ""})

    # Extract Marzano level distribution
    marzano_counts = {"retrieval": 0, "comprehension": 0, "analysis": 0, "knowledge_utilization": 0}
    for activity in lesson_json.get("activities", []):
        level = activity.get("marzano_level", "")
        if level in marzano_counts:
            marzano_counts[level] += 1

    # Extract pedagogical insights from persona feedback
    concerns = []
    successes = []
    for feedback in persona_feedback:
        persona_name = feedback.get("persona_name", "unknown")
        for concern in feedback.get("concerns", []):
            if concern.get("severity") == "high":
                concerns.append(f"{persona_name}: {concern.get('issue', '')}")

        # Positive signals (rating >= 4)
        if feedback.get("accessibility_rating", 0) >= 4:
            successes.append(f"{persona_name} rated highly ({feedback['accessibility_rating']}/5)")

    summary = {
        "lesson_number": lesson_num,
        "title": lesson_json.get("title", ""),
        "objective": lesson_json.get("objective", ""),
        "lesson_type": lesson_json.get("lesson_type", ""),

        "vocabulary_introduced": vocabulary,
        "assumed_knowledge": lesson_json.get("assumed_knowledge", []),

        "marzano_distribution": marzano_counts,
        "cognitive_rigor_percent": calculate_higher_order_percent(lesson_json),

        "pedagogical_notes": {
            "concerns": concerns,
            "successes": successes
        },

        "duration": lesson_json.get("duration", 0),
        "materials_generated": list_generated_materials(sequence_id, lesson_num),

        "token_estimate": 250  # Approximate
    }

    # Save summary
    lesson_dir = get_lesson_directory(sequence_id, lesson_num)
    with open(lesson_dir / "lesson_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary


def calculate_higher_order_percent(lesson_json: dict) -> int:
    """Calculate % of activities at analysis or knowledge utilization level."""
    total = 0
    higher_order = 0

    for activity in lesson_json.get("activities", []):
        total += 1
        level = activity.get("marzano_level", "")
        if level in ["analysis", "knowledge_utilization"]:
            higher_order += 1

    return int((higher_order / total) * 100) if total > 0 else 0


def list_generated_materials(sequence_id: str, lesson_num: int) -> list[str]:
    """List file names of generated materials for this lesson."""
    materials_dir = get_lesson_directory(sequence_id, lesson_num) / "materials"
    if not materials_dir.exists():
        return []

    return [f.name for f in materials_dir.iterdir() if f.is_file()]
```

## State of the Art

Current approaches to multi-session context management in production AI systems (2025-2026):

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Prompt stuffing (load everything into context) | **Selective retrieval (RAG)** + hierarchical memory | 2024-2025 | 10-20x context reduction, stable quality across long sequences. Production AI agents (coding assistants, customer support) all use this pattern. |
| Fixed-token truncation | **Semantic summarization** with structured metadata | 2025 | Maintains coherence vs. truncation breaking mid-sentence. EDU-based compression (Jan 2026) shows 5-20x compression with faithfulness. |
| Single vector database for all content | **Hierarchical memory** (short-term + long-term) | 2025-2026 | Recent lessons in "short-term" (full summaries), older lessons in "long-term" (semantic retrieval only). Mirrors human memory. |
| Cloud vector DBs (Pinecone) for all use cases | **Local FAISS** for <1M vectors | Mature (2020+) | Zero latency, no API costs, teacher privacy. Pinecone only needed at massive scale. |

**Deprecated/outdated:**
- **Context stuffing with 100K+ token windows:** Research definitively shows quality degradation past 32K tokens even on Claude Opus 4, GPT-4o. Marketing materials mislead.
- **LLM-based summarization chains:** "Use Claude to summarize lesson 1-5 for context" doubles LLM calls and introduces 10+ seconds latency. Structured extraction is instant.
- **Graph databases for lesson prerequisites:** Over-engineered. Educational progressions are mostly linear. JSON arrays + simple traversal is sufficient.

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal compression ratio for lesson summaries**
   - What we know: Research shows 5-20x compression is achievable for general text. Educational content may compress more (structured activities, repeated fields).
   - What's unclear: The exact fields to include in summaries. Too sparse = future lessons lack context. Too detailed = defeats compression purpose.
   - Recommendation: Start with Pattern 2 structure (vocabulary, marzano distribution, pedagogical notes). Measure empirically: generate lesson 8 with different summary structures, compare quality.

2. **When to use FAISS vs. simple JSON loading**
   - What we know: FAISS adds complexity (embeddings, index management). For 2-3 lesson sequences, it's overkill.
   - What's unclear: The exact tipping point. 5 lessons? 10 lessons? Depends on summary size and quality tolerance.
   - Recommendation: Implement JSON loading first (sufficient for 80% of use cases: 2-4 lesson units). Add FAISS in a later update if teachers request 8+ lesson sequences. Include token counting logic to detect when context is approaching limits.

3. **Persona feedback accumulation strategy**
   - What we know: If Alex flags vocabulary issues in lesson 3, lesson 4 should avoid the same issue. Current system doesn't propagate feedback across sequence.
   - What's unclear: How to balance lesson-specific feedback (vocabulary for THIS lesson) vs. sequence-level patterns (vocabulary scaffolding approach).
   - Recommendation: Store lesson-specific feedback in each lesson's files (current behavior). Add `sequence_summary.json` → `pedagogical_patterns` field for cross-lesson patterns. Extract after every 2-3 lessons: "Vocabulary pacing has been consistently good (Alex 4/5 on lessons 1-3)" or "Instructions need more scaffolding (Alex 2/5 on lessons 2-3)."

4. **Sequence-level assessment design**
   - What we know: SEQN-04 requires "sequence-level assessments covering multiple lessons." This is more than combining lesson 1-8 learning objectives.
   - What's unclear: How to design coherent summative assessments (final projects, cumulative tests) that test integration of competencies, not just individual skills.
   - Recommendation: Extend generate_assessment.py with `sequence_assessment` type. Input: all lesson summaries + sequence metadata. Output: performance task or test drawing on vocabulary, skills, and knowledge from entire sequence. Use backward design: assessment measures end-of-sequence competency.

5. **Handling sequence modifications mid-flight**
   - What we know: Teacher might want to revise lesson 3 after generating lessons 1-5. Does this invalidate lessons 4-5?
   - What's unclear: Dependency tracking rigor. If lesson 3 taught "corroboration" and lesson 5 uses it, modifying lesson 3 to remove that term breaks lesson 5.
   - Recommendation: Phase 5 MVP treats lessons as immutable once approved (current behavior). Flag sequence modification as v2 feature requiring dependency analysis.

## Sources

### Primary (HIGH confidence)

**Context Management & LLM Applications:**
- [Recursive Language Models: the paradigm of 2026](https://www.primeintellect.ai/blog/rlm) - RLMs and context folding for long-horizon tasks
- [LLM Development in 2026: Hierarchical Memory](https://medium.com/@vforqa/llm-development-in-2026-transforming-ai-with-hierarchical-memory-for-deep-context-understanding-32605950fa47) - Hierarchical memory architecture
- [Context Window Management: Strategies for Long-Context AI Agents](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/) - Production patterns
- [Best LLMs for Extended Context Windows in 2026](https://research.aimultiple.com/ai-context-window/) - Performance drops past 32K tokens documented

**Context Compression:**
- [From Context to EDUs: Faithful and Structured Context Compression (Jan 2026)](https://arxiv.org/pdf/2512.14244) - EDU-based compression achieving 5-20x reduction
- [Prompt Compression Techniques: Reducing Context Window Costs](https://medium.com/@kuldeep.paul08/prompt-compression-techniques-reducing-context-window-costs-while-improving-llm-performance-afec1e8f1003) - 70-94% cost savings

**Vector Databases & Semantic Search:**
- [ChromaDB vs Pinecone vs FAISS Benchmarks (2025)](https://towardsai.net/p/l/vector-databases-performance-comparison-chromadb-vs-pinecone-vs-faiss-real-benchmarks-that-will-surprise-you) - FAISS 1000x faster than Pinecone
- [Mastering Semantic Search in 2026](https://medium.com/@smenon_85/mastering-semantic-search-in-2026-44bc012c4e41) - sentence-transformers + FAISS patterns
- [Semantic Search with FAISS - Hugging Face](https://huggingface.co/learn/llm-course/chapter5/6?fw=tf) - Implementation guide

**Educational Theory:**
- [Backward Design - University of Illinois Chicago](https://teaching.uic.edu/cate-teaching-guides/syllabus-course-design/backward-design/) - Three-stage curriculum design process
- [Learning Progressions Definition - EdGlossary](https://www.edglossary.org/learning-progression/) - Skill sequencing and interdependencies
- [Learning Progressions: Pathways for 21st Century Teaching - Brookings](https://www.brookings.edu/articles/learning-progressions-pathways-for-21st-century-teaching-and-learning/) - Sequence coherence research

### Secondary (MEDIUM confidence)

**Curriculum Mapping:**
- [Towards a Metadata Schema for Lesson Plans (ResearchGate)](https://www.researchgate.net/publication/282864068_Towards_a_Metadata_Schema_for_Characterizing_Lesson_Plans_Supported_by_Remote_and_Virtual_Labs_for_School_Science_Education) - Science education metadata
- [Curriculum Mapping Software in 2026 - Edusfere](https://edusfere.com/beyond-spreadsheets-how-to-choose-the-right-curriculum-mapping-software-for-your-school/) - Modern curriculum tools

**Vector Embeddings:**
- [Best Embedding Models for Semantic Search - Graft](https://www.graft.com/blog/text-embeddings-for-search-semantic) - all-MiniLM-L6-v2 vs all-mpnet-base-v2
- [How to Implement Semantic Search with Python - Milvus](https://milvus.io/ai-quick-reference/how-do-i-implement-semantic-search-with-python) - Implementation patterns

### Tertiary (LOW confidence)

- [AI Lesson Planning Guide 2026 - Lifehub](https://www.lifehubeducation.com/blog/ai-lesson-planning) - General overview, not implementation-focused
- WebSearch results on lesson sequencing strategies - Broad educational concepts, less technical

## Metadata

**Confidence breakdown:**
- Standard stack: **HIGH** - FAISS and sentence-transformers are mature, well-documented, and proven in production AI systems. Installation and usage patterns are stable.
- Architecture patterns: **MEDIUM** - Patterns are synthesized from multiple sources (RAG applications, educational research, existing codebase). The integration is novel for this domain.
- Context management pitfalls: **HIGH** - Research explicitly documents performance degradation past 32K tokens. This is well-established.
- Sequence metadata schema: **MEDIUM** - Adapted from curriculum mapping research but not directly tested in this codebase.
- Educational progression patterns: **HIGH** - Backward design and learning progressions are foundational educational research (decades of evidence).

**Research date:** 2026-01-26
**Valid until:** 30 days (stable domain - FAISS, educational theory change slowly. LLM context window research updates monthly but core findings are stable.)

---

**Next step:** Use this research to inform Phase 5 planning. Key decisions for planner:
1. Implement sequence metadata schema first (enables all other features)
2. Start with JSON-based context loading (sufficient for 2-4 lesson sequences in MVP)
3. Add FAISS retrieval as optional enhancement (flag in research as "needed for 5+ lessons")
4. Extend persona feedback to track sequence-level patterns
5. Build sequence-level assessment generation using backward design
