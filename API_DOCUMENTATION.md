# KNOWPATH / PROJECT-EVOLVE — API Documentation

**API Base URL:** `http://localhost:8000/api/v1`  
**OpenAPI Specification:** `http://localhost:8000/openapi.json`  
**Interactive Swagger UI:** `http://localhost:8000/docs`  
**Authentication:** HTTP Bearer token (JWT in `Authorization: Bearer <token>`)

---

## 1. System Endpoints

### `GET /health`
- **Description:** System health and liveness probe.
- **Auth:** None
- **Response:**
  ```json
  { "status": "ok", "version": "0.1.0", "environment": "development" }
  ```

---

## 2. Authentication (`/api/v1/auth`)

### `POST /auth/register`
- **Description:** Register a new learner account with DOB age gate (18+) and explicit consent validation.
- **Request Body:**
  ```json
  {
    "email": "learner@example.com",
    "password": "strongPassword123",
    "dob": "2000-01-15",
    "consent_version": "1.0"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user_id": "usr_abc123",
    "email": "learner@example.com",
    "role": "learner"
  }
  ```
- **Error Codes:** `400 Bad Request` (Under 18 or missing consent), `409 Conflict` (Email exists).

### `POST /auth/login`
- **Description:** Authenticate user and receive Bearer JWT.
- **Request Body:**
  ```json
  { "email": "learner@example.com", "password": "strongPassword123" }
  ```
- **Response:** `200 OK` (Token envelope)

### `POST /auth/logout`
- **Description:** Terminate active session.
- **Auth:** Bearer Token
- **Response:** `204 No Content`

### `GET /auth/me`
- **Description:** Returns currently authenticated user identity and role.
- **Auth:** Bearer Token

---

## 3. Profiles & Goals (`/api/v1/profiles`, `/api/v1/goals`)

### `GET /profiles/me`
- **Description:** Retrieve current user profile, study hours, and learning style preferences.

### `PATCH /profiles/me`
- **Description:** Update preferences: `weekly_hours`, `explanation_style` (`intuitive`, `formal`, `code_first`), `preferred_session_length`.

### `GET /goals/`
- **Description:** List available and active goals for user.

### `POST /goals/`
- **Description:** Set active goal: `python_placements`, `python_data`, or `python_basics`.

---

## 4. Knowledge Genome (`/api/v1/genome`)

### `GET /genome/concepts`
- **Description:** Retrieve all 79 Python concepts with titles, slugs, difficulties, and summaries.

### `GET /genome/concepts/{slug}`
- **Description:** Retrieve detailed Markdown curriculum notes, prerequisites list, dependents list, and question count for a concept.

### `GET /genome/graph`
- **Description:** Retrieve full DAG structure with 79 nodes and 118 prerequisite edges for graph rendering.

---

## 5. Assessments & Diagnostic (`/api/v1/assessments`)

### `POST /assessments/diagnostic/start`
- **Description:** Initialize adaptive diagnostic attempt. Returns first item chosen by information-gain uncertainty selector.
- **Request Body:**
  ```json
  { "kind": "diagnostic" }
  ```
- **Response:**
  ```json
  {
    "attempt_id": "att_01",
    "first_item": {
      "id": "q_var_01",
      "concept_id": "variables_intro",
      "stem": "What is the output of the following code?",
      "code_snippet": "x = 5\ny = x\nx = 10\nprint(y)",
      "kind": "code_reading",
      "difficulty": "beginner",
      "options": [
        { "key": "A", "text": "10" },
        { "key": "B", "text": "5" }
      ]
    }
  }
  ```

### `POST /assessments/diagnostic/submit`
- **Description:** Grade answer server-side, detect misconception distractor, compute deterministic Beta update, and return next item.
- **Request Body:**
  ```json
  {
    "attempt_id": "att_01",
    "question_id": "q_var_01",
    "answer": "B",
    "time_ms": 4200
  }
  ```
- **Response:**
  ```json
  {
    "is_correct": true,
    "explanation": "Variables in Python store object references. Assigning y = x binds y to integer object 5.",
    "misconception_detected": null,
    "updated_mastery": 0.72,
    "next_item": { ... }
  }
  ```

---

## 6. Cognitive Twin (`/api/v1/twin`)

### `GET /twin/`
- **Description:** Retrieve full Cognitive Twin state: mastery estimates, credible intervals, alpha/beta parameters, and "why this score" explanations across concepts.

### `GET /twin/snapshots`
- **Description:** Retrieve time-series snapshots of twin evolution for trend charts.

---

## 7. Roadmap & Daily Missions (`/api/v1/roadmap`, `/api/v1/missions`)

### `GET /roadmap/`
- **Description:** Retrieve topologically ordered learning roadmap of missing concepts with foundation bonuses.

### `POST /roadmap/generate`
- **Description:** Force regeneration of roadmap from current Cognitive Twin state.

### `GET /missions/today`
- **Description:** Retrieve today's 15-45 minute micro-learning mission.

### `POST /missions/{mission_id}/complete`
- **Description:** Mark mission completed and record evidence into Cognitive Twin.

---

## 8. Spaced Reviews (`/api/v1/reviews`)

### `GET /reviews/due`
- **Description:** List concepts due for memory retrieval review per the SM-2 algorithm.

### `POST /reviews/complete`
- **Description:** Record review pass/fail; calculates updated ease factor and next due date.

---

## 9. AI Teaching Companion (`/api/v1/companion`)

### `POST /companion/explain`
- **Description:** AI-assisted grounded explanation strictly citing Genome curriculum notes.
- **Request Body:**
  ```json
  {
    "concept_slug": "list_mutability",
    "question": "Why does modifying a list inside a function affect the caller?"
  }
  ```
- **Response:**
  ```json
  {
    "explanation": "In Python, arguments are passed by assignment (object reference)...",
    "sources": ["Knowledge Genome: list_mutability Core Notes"],
    "is_ai": true
  }
  ```

---

## 10. Disputes & User Rights (`/api/v1/disputes`, `/api/v1/users`)

### `POST /disputes/`
- **Description:** File formal challenge against question or score; halves evidence weight (0.5x).

### `GET /disputes/`
- **Description:** List current user's dispute history.

### `GET /users/export`
- **Description:** Download full JSON data archive per GDPR Article 20.

### `DELETE /users/me`
- **Description:** Permanently hard-delete account with confirmation string `"DELETE"`.

---

## 11. System Administration (`/api/v1/admin`)

- `GET /admin/users`: List registered learners.
- `GET /admin/disputes`: List and review pending disputes.
- `PATCH /admin/disputes/{id}/resolve`: Resolve or dismiss dispute.
- `GET /admin/agent-executions`: Audit logs of LLM agent executions.
- `GET /admin/costs`: Aggregate token spend and cost telemetry.
