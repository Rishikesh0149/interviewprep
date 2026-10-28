export interface User {
  id: number;
  email: string;
  full_name: string;
  experience_level: 'beginner' | 'intermediate' | 'senior';
  target_role: string;
  readiness_score: number;
  current_streak: number;
  created_at: string;
}

export interface CandidateProfile {
  id: number;
  user_id: number;
  headline: string;
  summary: string;
  contact_info: {
    email?: string;
    phone?: string;
    location?: string;
    linkedin?: string;
    github?: string;
    portfolio?: string;
  };
  skills: {
    languages?: string[];
    frameworks?: string[];
    databases?: string[];
    tools?: string[];
    soft_skills?: string[];
  };
  experience: Array<{
    company: string;
    role: string;
    start: string;
    end: string;
    bullets: string[];
  }>;
  education: Array<{
    institution: string;
    degree: string;
    field: string;
    grad_year: string;
    gpa?: string;
  }>;
  projects: Array<{
    name: string;
    tech_stack: string[];
    description: string;
    metrics?: string;
    repo_url?: string;
    live_url?: string;
  }>;
  certifications: string[];
  updated_at: string;
}

export interface ResumeData {
  id: number;
  file_name: string;
  file_type: string;
  file_size_bytes: number;
  raw_text: string;
  ats_score: number;
  ats_breakdown: {
    section_completeness: number;
    keyword_alignment: number;
    quantified_impact: number;
    action_verb_diversity: number;
    formatting_clarity: number;
    readability_tone: number;
    length_density: number;
  };
  red_flags: Array<{
    type: string;
    severity: 'low' | 'medium' | 'high';
    description: string;
  }>;
  tailored_version?: string;
  created_at: string;
}

export interface TargetRoleData {
  id: number;
  role_key: string;
  title: string;
  category: string;
  description: string;
  required_skills: string[];
  nice_to_have_skills: string[];
  core_competencies: string[];
  typical_interview_rounds: Array<{
    round: string;
    focus: string;
  }>;
}

export interface SkillGapReportData {
  role_title: string;
  match_percentage: number;
  strong_skills: string[];
  partial_skills: string[];
  missing_skills: string[];
  recommendations: string[];
  created_at?: string;
}

export interface StudyTask {
  id: number;
  week_number: number;
  day_number: number;
  tier: 'BASIC' | 'INTERMEDIATE' | 'ADVANCED';
  title: string;
  description: string;
  topic: string;
  resource_type: string;
  resource_url: string;
  is_completed: boolean;
}

export interface StudyPlan {
  id: number;
  role_title: string;
  total_weeks: number;
  hours_per_day: number;
  status: string;
  progress_percentage: number;
  tasks: StudyTask[];
}

export interface InterviewTurn {
  id: number;
  turn_index: number;
  question_text: string;
  question_category: string;
  user_answer: string;
  speaking_wpm: number;
  filler_word_count: number;
  feedback?: {
    id: number;
    score_overall: number;
    score_relevance: number;
    score_star_structure: number;
    score_technical_accuracy: number;
    score_clarity: number;
    score_confidence: number;
    score_conciseness: number;
    critique: string;
    sample_ideal_answer: string;
    detected_weak_points: string[];
  };
}

export interface InterviewSession {
  id: number;
  role_title: string;
  mode: 'text' | 'voice' | 'timed_round';
  persona: string;
  round_type: string;
  level: number;
  status: 'in_progress' | 'completed';
  overall_score: number;
  total_turns: number;
  summary_feedback: string;
  strengths: string[];
  weaknesses: string[];
  suggested_topics_to_improve: string[];
  wpm_average: number;
  filler_words_total: number;
  created_at: string;
  turns: InterviewTurn[];
}

export interface Badge {
  id: number;
  badge_key: string;
  title: string;
  description: string;
  icon: string;
  tier: string;
  earned_at: string;
}

export interface CodingProblem {
  id: string;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  category: string;
  description: string;
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  constraints: string[];
  starter_code: {
    python: string;
    javascript: string;
  };
  hints: string[];
  optimal_complexity: string;
}

export interface TestCaseResult {
  input_str: string;
  expected_output: string;
  actual_output: string;
  passed: boolean;
  error?: string | null;
}

export interface CodeRunResponse {
  status: string;
  passed_cases: number;
  total_cases: number;
  runtime_ms: number;
  test_results: TestCaseResult[];
  ai_feedback?: string;
  time_complexity?: string;
  space_complexity?: string;
}

export interface QuestionItem {
  id: number;
  role_id?: number | null;
  role_title?: string;
  level: number;
  category: string;
  question_text: string;
  difficulty: string;
  expected_keywords: string[];
  ideal_star_answer: string;
  rubric_hints: string[];
}

export interface QuestionListResponse {
  total: number;
  questions: QuestionItem[];
  categories: string[];
  difficulties: string[];
}
