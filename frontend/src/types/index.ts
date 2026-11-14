/**
 * Type definitions for KNOWPATH platform.
 */

export type UserRole = "learner" | "admin";

export interface User {
  id: string;
  email: string;
  role: UserRole;
  is_verified?: boolean;
  created_at: string;
}

export interface Profile {
  user_id?: string;
  display_name?: string;
  education_level?: string;
  weekly_hours?: number;
  explanation_style?: "intuitive" | "formal" | "code_first";
  preferences?: {
    explanation_style?: string;
    session_length?: number;
  };
}

export type GoalKey = "python_placements" | "python_data" | "python_basics";

export interface Goal {
  id: string;
  user_id: string;
  goal_key: GoalKey;
  target_concept_ids?: string[];
  active?: boolean;
}

export interface ConceptSummary {
  id?: string;
  slug: string;
  title: string;
  description: string;
  difficulty: string | number;
  domain?: string;
  mastery?: number;
  confidence?: number;
}

export interface ConceptDetail extends ConceptSummary {
  content?: string;
  content_md?: string;
  prerequisites: string[];
  dependents: string[];
  questions_count?: number;
  misconceptions?: Array<{ id: string; title: string; explanation: string }>;
}

export interface GraphNode {
  id: string;
  label?: string;
  title?: string;
  difficulty?: string | number;
  mastery?: number;
  confidence?: number;
}

export interface GraphEdge {
  from_slug?: string;
  to_slug?: string;
  source?: string;
  target?: string;
  type?: string;
  strength?: number;
}

export interface GenomeGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export type SourceType = "self_reported" | "ai_estimated" | "assessment_verified";

export interface EvidenceItem {
  id: string;
  source_type: SourceType;
  value: number;
  weight: number;
  observed_at: string;
  disputed: boolean;
}

export interface MasteryItem {
  concept_id: string;
  concept_title?: string;
  mastery_score: number;
  confidence: number;
  alpha: number;
  beta: number;
  credible_interval_low: number;
  credible_interval_high: number;
  source_type: SourceType;
  evidence_count?: number;
  why_this_score?: string;
}

export interface TwinPageData {
  user_id?: string;
  overall_mastery?: number;
  overall_confidence?: number;
  concepts_evaluated?: number;
  total_concepts?: number;
  mastery_list: MasteryItem[];
  snapshots_count?: number;
}

export interface AssessmentOption {
  key: string;
  text: string;
}

export interface AssessmentItem {
  id: string;
  question_id?: string;
  attempt_id?: string;
  item_number?: number;
  total_items?: number;
  concept_id: string;
  concept_slug?: string;
  concept_title?: string;
  stem: string;
  code_snippet?: string;
  kind: "multiple_choice" | "multi_select" | "code_reading" | "predict_bug" | string;
  type?: string;
  difficulty?: string | number;
  options: AssessmentOption[];
}

export interface SubmitAnswerResponse {
  attempt_id?: string;
  question_id?: string;
  is_correct: boolean;
  correct?: boolean;
  explanation: string;
  misconception_detected?: string;
  misconception_flagged?: { id: string; title: string; explanation: string };
  is_completed?: boolean;
  updated_mastery: number;
  next_item?: AssessmentItem;
}

export interface RoadmapItemDetail {
  id?: string;
  rank?: number;
  position?: number;
  concept_slug: string;
  concept_title?: string;
  difficulty?: string | number;
  status?: "pending" | "in_progress" | "done" | string;
  gap_type?: "gap" | "unknown" | string;
  priority?: number;
  reason?: string;
  because?: string;
  current_mastery?: number;
}

export interface RoadmapRead {
  id?: string;
  user_id?: string;
  goal_key?: string;
  items: RoadmapItemDetail[];
  created_at?: string;
  updated_at?: string;
}

export interface MissionItem {
  id: string;
  type: "explanation" | "practice" | "check" | string;
  concept_slug: string;
  concept_title: string;
  content?: any;
}

export interface MissionRead {
  id: string;
  user_id?: string;
  title?: string;
  description?: string;
  estimated_minutes?: number;
  reading_url?: string;
  completed?: boolean;
  completed_at?: string;
  status?: "pending" | "in_progress" | "completed" | string;
  focus_concept_slug?: string;
  focus_concept_title?: string;
  items?: MissionItem[];
  because?: string;
}

export interface ReviewItem {
  id?: string;
  concept_slug: string;
  concept_title?: string;
  difficulty?: string | number;
  due_at?: string;
  interval_days: number;
  ease_factor: number;
  ease?: number;
  is_overdue?: boolean;
  last_result?: string;
}

export interface Dispute {
  id: string;
  target_type: "question" | "score";
  target_id: string;
  reason: string;
  status: "open" | "resolved" | "dismissed";
  resolution_notes?: string;
  created_at?: string;
  resolved_at?: string;
}
