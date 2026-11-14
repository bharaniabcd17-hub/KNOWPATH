# KNOWPATH / PROJECT-EVOLVE — System Architecture & Technical Specifications

**Version:** 1.0 (Phase 1 Vertical Slice)  
**Domain Focus:** Python Programming Fundamentals (79 concepts, 118 prerequisite edges, 430 questions, 34 misconception traps)  
**Compliance Standard:** Age 18+ Gate, GDPR Article 20 (Data Portability) & Article 17 (Right to Erasure), Deterministic Scoring Charter  

---

## 1. Executive Summary & Core Mission

KNOWPATH (Project Evolve) is an evidence-based learner intelligence platform. Unlike conventional learning applications that rely on passive video completions, vanity streaks, or LLM-hallucinated grades, KNOWPATH continuously maintains a mathematically grounded, probabilistic model of what a learner demonstrably knows.

### Non-Negotiable Product Charter
1. **Deterministic Scoring:** AI models never calculate or adjust scores. All capability estimates are derived from closed-form Bayesian Beta distribution updates.
2. **Strict Evidence Provenance Hierarchy:** Evidence types are strictly ordered: `self_reported` (0.10) < `ai_estimated` (0.30) < `assessment_verified` (1.00). Sources are never upgraded without verified test execution.
3. **No Outcome Guarantees:** The platform strictly prohibits job placement, salary, or interview guarantees.
4. **Data Sovereignty & User Rights:** Explicit consent is required at registration. Users can export their full cognitive record (JSON) or execute hard account deletion at any time.
5. **Right of Dispute:** Any assessment item or score update can be contested, immediately reducing its weighting by 50% pending administrative audit.

---

## 2. Five Signature Innovations

### 1. Cognitive Twin
- A digital model of user mastery across all 79 Python concepts.
- Each concept state stores:
  - Posterior parameters: $\alpha$ (accumulated weighted correct evidence) and $\beta$ (accumulated weighted incorrect evidence).
  - Mastery estimate: $\mu = \frac{\alpha}{\alpha + \beta}$.
  - Confidence: Derived from sample evidence density and posterior variance.
  - 80% Credible Interval: $[\theta_{10}, \theta_{90}]$ calculated via the Beta quantile function.
  - Historical snapshots: Versioned records of twin states over time.
  - Transparent "Why This Score" audit breakdown for every concept.

### 2. Knowledge Genome
- A curated, cycle-free directed acyclic graph (DAG) mapping Python programming fundamentals:
  - 79 core concepts spanning 9 modules (Variables & Types, Control Flow, Functions, Lists & Dicts, Strings, File I/O, Exceptions, Basic OOP, Core Algorithms).
  - 118 validated prerequisite edges.
  - Foundation bonus: High-leverage nodes that unblock 2 or more downstream concepts receive a 1.25x priority multiplier in roadmap generation.

### 3. Adaptive Learning & Diagnostic
- Dynamic item selection based on uncertainty minimization (information gain) along the learner's knowledge frontier.
- 430 assessment questions covering:
  - Code reading ("What does this output?")
  - Predict-the-bug
  - Multiple choice & multi-select
- Distractor taxonomy: 34 tagged conceptual misconceptions (e.g. `MISCON_MUTABLE_DEFAULT`, `MISCON_FLOOR_DIV`, `MISCON_SHALLOW_COPY`).

### 4. FuturePath Simulator
- Simulates learner capability alignment against real technical tracks:
  - Python Backend API Engineering
  - Data Pipeline & Analytics Engineering
  - Python Automation & DevOps
- Compares real Cognitive Twin mastery against required concept clusters, highlighting missing prerequisite blockers without promising employment.

### 5. Collective Intelligence AI Orchestration
- Orchestrated agent ecosystem:
  - **Teaching Companion Agent:** Grounded tutor explaining concepts strictly from Genome curriculum notes.
  - **Quality & Safety Agent:** Automated gatekeeper that rejects hallucinated outcome guarantees and ensures strict schema validation.
  - **Audit Telemetry:** Every agent invocation is recorded in `agent_executions` with token counts, execution latency, and deterministic cost tracking.

---

## 3. Technology Stack & Directory Structure

```
e:\hackathon\
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application & router mounts
│   │   ├── config.py                   # Pydantic v2 BaseSettings
│   │   ├── database.py                 # Async SQLAlchemy engine & SQLite fallback
│   │   ├── models.py                   # 21 SQLAlchemy 2 ORM entity models
│   │   ├── schemas.py                  # Pydantic validation schemas
│   │   ├── deps.py                     # Auth & DB dependency injection
│   │   ├── scoring/
│   │   │   ├── engine.py               # Beta update, recency decay, credible interval
│   │   │   ├── gap_detector.py         # Topological DAG traversal & foundation bonus
│   │   │   ├── retention.py            # SM-2 memory retention engine
│   │   │   └── item_selector.py        # Adaptive information-gain question selection
│   │   ├── agents/
│   │   │   ├── llm_client.py           # MockLLMClient & AnthropicLLMClient
│   │   │   ├── embedding_client.py     # MockEmbeddingClient & OpenAIEmbeddingClient
│   │   │   ├── quality_safety_agent.py # Content moderation & promise filter
│   │   │   └── orchestrator.py         # Agent execution logger & router
│   │   └── routers/                    # 13 REST API domain endpoints
│   ├── tests/                          # 24 automated pytest suites (100% passing)
│   └── scripts/
│       ├── init_db.py                  # Table initialization
│       └── seed.py                     # Genome, Question & Misconception seeder
├── content/
│   └── python/
│       ├── concepts.yaml               # 79 Python concepts with study notes
│       ├── misconceptions.yaml         # 34 tagged distractor misconceptions
│       ├── questions.yaml              # 430 calibrated assessment items
│       └── validate.py                 # Cycle-free DAG validator
└── frontend/
    ├── src/
    │   ├── app/                        # Next.js 15 App Router pages
    │   ├── components/                 # Navbar, Footer, Sidebar, Header
    │   ├── lib/api.ts                  # Typed API client for FastAPI backend
    │   ├── stores/auth.ts              # Zustand authentication store
    │   ├── styles/globals.css          # Tailwind CSS styling
    │   └── types/index.ts              # TypeScript interfaces
    └── package.json
```

---

## 4. Deterministic Scoring Formulas

### 1. Evidence Weight
$$\text{Effective Weight} = W_{\text{source}} \times F_{\text{recency}} \times F_{\text{speed}} \times F_{\text{dispute}}$$
Where:
- $W_{\text{source}} \in \{0.10 \text{ (self)}, 0.30 \text{ (AI)}, 1.00 \text{ (assessment)}\}$
- $F_{\text{recency}} = 0.5^{\frac{\Delta t}{60 \text{ days}}}$
- $F_{\text{speed}} = 0.80$ if response time $< 3000\text{ms}$, else $1.00$
- $F_{\text{dispute}} = 0.50$ if under active dispute, else $1.00$

### 2. Beta Posterior Update
$$\alpha_{t} = \alpha_0 + \sum_{i \in \text{correct}} \text{Effective Weight}_i$$
$$\beta_{t} = \beta_0 + \sum_{j \in \text{incorrect}} \text{Effective Weight}_j$$
$$\text{Mastery Score} = \frac{\alpha_t}{\alpha_t + \beta_t}$$

### 3. Spaced Retention (SM-2)
$$I(1) = 1, \quad I(2) = 6, \quad I(n) = I(n-1) \times \text{EF}$$
$$\text{EF}' = \text{EF} + (0.1 - (5 - q) \times (0.08 + (5 - q) \times 0.02))$$
If $q < 3$, interval resets to 1 day.
